
import os
import platform

from nr.powerline.plugins import Plugin, cached_property


class SessionPlugin(Plugin):

  _cwd = None

  @cached_property
  def hostname(self):
    return platform.node()

  @property
  def cwd(self):
    user_home = os.path.expanduser('~')
    cwd = self._cwd or os.getcwd()
    try:
      relpath = os.path.relpath(cwd, user_home)
      if relpath.startswith(os.pardir):
        raise ValueError
      if relpath == os.curdir:
        return '~'
      return os.path.join('~', relpath)
    except ValueError:
      return cwd
    assert False
