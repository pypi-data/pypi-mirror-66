
from __future__ import print_function
from . import daemon
from .shells import get_bash_ps1
from nr.utils.process import process_exists, process_terminate, replace_stdio, spawn_daemon
import argparse
import os
import signal
import sys


def default_powerline():
  from nr.powerline import PowerLine
  p = PowerLine()
  git = p.get_plugin('git')

  p.set_pen('white', 'blue')
  p.add_part(' {c.GIT_FOLDER} ' if git.project else ' {c.DIRECTORY} ')
  p.add_part('{session.cwd} !{c.RIGHT_TRIANGLE}')
  if git.project:
    p.set_pen(None, 'yellow')
    p.add_part(' {c.BRANCH} {git.branch} !{c.RIGHT_TRIANGLE}')
  p.add_part(' ')
  p.clear_pen()
  return p


def powerline_supplier(filename):
  if filename:
    with open(filename) as fp:
      code = compile(fp.read(), filename, 'exec')
    def func():
      scope = {}
      exec(code, scope)
      return scope['powerline']
  else:
    func = default_powerline
  return func


def main(argv=None, prog=None):
  parser = argparse.ArgumentParser(prog=prog)
  parser.add_argument('-f', '--file')
  parser.add_argument('--run-dir', default=None)
  parser.add_argument('--start', action='store_true')
  parser.add_argument('--stop', action='store_true')
  parser.add_argument('--status', action='store_true')
  parser.add_argument('--exit-code', action='store_true')
  parser.add_argument('--src', choices=('bash',))
  args = parser.parse_args(argv)

  if args.src == 'bash':
    print(get_bash_ps1(args.file))
    sys.exit(0)
  elif args.src:
    parser.error('unexpected argument for --src: {!r}'.format(args.src))

  if not args.start and not args.stop and not args.status:
    powerline_supplier(args.file)().print_()
    return

  run_dir = args.run_dir or os.path.expanduser('~/.local/powerline')
  log_file = os.path.join(run_dir, 'daemon.log')
  pid_file = os.path.join(run_dir, 'daemon.pid')
  socket_file = os.path.join(run_dir, 'daemon.sock')

  if os.path.isfile(pid_file):
    with open(pid_file) as fp:
      daemon_pid = int(fp.read().strip())
  else:
    daemon_pid = None

  if args.stop and daemon_pid:
    print('Stopping', daemon_pid)
    process_terminate(daemon_pid)
  if args.start:
    def run(powerline, stdout):
      with open(pid_file, 'w') as fp:
        fp.write(str(os.getpid()))
      print('Started', os.getpid())
      signal.signal(signal.SIGTERM, lambda: os.remove(pid_file))
      replace_stdio(None, stdout, stdout)
      conf = daemon.SocketConf.UnixFile(socket_file)
      daemon.PowerlineDaemon(conf, powerline).run_forever()

    powerline = powerline_supplier(args.file)
    os.makedirs(run_dir, exist_ok=True)
    stdout = open(log_file, 'a')
    spawn_daemon(lambda: run(powerline, stdout))
  if args.status:
    if not daemon_pid or not process_exists(daemon_pid):
      if args.exit_code:
        sys.exit(7)
      print('stopped')
    else:
      if args.exit_code:
        sys.exit(0)
      print('running')
