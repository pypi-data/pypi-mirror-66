
from __future__ import print_function
import argparse
import os


def default_powerline():
  from nr.powerline import PowerLine
  p = PowerLine()
  p.set_pen('white', 'magenta')
  p.add_part(' {session.cwd} !{c.RIGHT_TRIANGLE} ')
  git = p.get_plugin('git')
  if git.project:
    p.set_pen(None, 'blue')
    p.add_part(' {c.BRANCH} {git.branch} !{c.RIGHT_TRIANGLE}')
  p.clear_pen()
  p.add_part(' ')
  p.print_()


def main(argv=None, prog=None):
  parser = argparse.ArgumentParser(prog=prog)
  parser.parse_args(argv)

  filename = os.getenv('NR_POWERLINE_SCRIPT', '')
  code = os.getenv('NR_POWERLINE_CODE', '')

  if code:
    exec(code)
  elif filename:
    with open(filename) as fp:
      exec(fp.read())
  else:
    default_powerline()
  return 0
