# -*- coding: utf8 -*-
# Copyright (c) 2020 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from . import PowerLine
import socket as _socket
import nr.sumtype
import os
import traceback
from typing import Callable


class SocketConf(nr.sumtype.Sumtype):
  Ipv4 = nr.sumtype.Constructor('host,port')
  UnixFile = nr.sumtype.Constructor('filename')

  @Ipv4.member
  def type(self) -> int:
    return _socket.AF_INET

  @UnixFile.member
  def type(self) -> int:
    return _socket.AF_UNIX

  @Ipv4.member
  def bind(self, socket: _socket.socket):
    socket.bind((self.host, self.port))

  @Ipv4.member
  def connect(self, socket: _socket.socket):
    socket.connect((self.host, self.port))

  @UnixFile.member
  def bind(self, socket: _socket.socket):
    socket.bind(self.filename)

  @UnixFile.member
  def connect(self, socket: _socket.socket):
    socket.connect(self.filename)


class PowerlineDaemon:

  def __init__(self, conf: SocketConf, powerline: Callable[[], PowerLine]) -> None:
    self._conf = conf
    self._powerline = powerline

  def run_forever(self):
    socket = _socket.socket(self._conf.type())
    self._conf.bind(socket)
    socket.listen(5)
    socket.settimeout(0.1)
    try:
      while True:
        try:
          conn, address = socket.accept()
        except _socket.timeout:
          continue
        path = conn.makefile().readline().strip()
        try:
          os.chdir(path)
          result = str(self._powerline())
        except Exception as exc:
          result = traceback.format_exc()
        conn.makefile('w').write(result)
        conn.close()
    finally:
      socket.close()
      if isinstance(self._conf, SocketConf.UnixFile):
        os.remove(self._conf.filename)


class PowerlineClient:

  def __init__(self, conf: SocketConf):
    self._conf = conf

  def request(self, path: str) -> str:
    socket = _socket.socket(self._conf.type())
    self._conf.connect(socket)
    path = os.path.abspath(path)
    try:
      socket.makefile('w').write(path + '\n')
      return socket.makefile().read()
    finally:
      socket.close()
