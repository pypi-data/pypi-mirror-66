
import os


BASH_PS1_TEMPLATE = '''
function _nr_powerline_get() {
  echo "$PWD" | nc -U ~/.local/powerline/daemon.sock 2>/dev/null
  return $?
}
function _nr_powerline_alt() {
  if [ "$ALTPS1" != "" ]; then
    printf "$ALTPS1"
  else
    printf "$HOSTNAME $PWD $ "
  fi
}
function _nr_powerline_bootstrapper() {
  _nr_powerline_get
  if [ $? != 0 ]; then
    if which nr-powerline >/dev/null; then
      nr-powerline --start {{file_args}}
      if ! ( nr-powerline --status --exit-code >/dev/null ); then
        2> echo "Could not start powerline daemon."
        _nr_powerline_alt
      else
        _nr_powerline_get
      fi
    else
      _nr_powerline_alt
    fi
  fi
}
function _nr_powerline_direct() {
  nr-powerline {{file_args}} 2>/dev/null
  if [ $? != 0 ]; then
    _nr_powerline_alt
  fi
}
if [[ `uname` =~ MSYS_NT.* ]]; then
  export PS1='`_nr_powerline_direct`'
else
  export PS1='`_nr_powerline_bootstrapper`'
fi
'''


def get_bash_ps1(file):
  file = os.path.abspath(file) if file else None
  return BASH_PS1_TEMPLATE.replace('{{file_args}}',
    '--file "{}"'.format(file) if file else '')
