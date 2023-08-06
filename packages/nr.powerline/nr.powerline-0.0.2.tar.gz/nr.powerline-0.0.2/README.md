# nr.powerline

Simple powerline implementation, only tested in Bash. It is recommended that
you use a font from [NerdFonts](https://nerdfonts.com/#downloads) in order to
have proper support for special characters (like the right triangle).

__Simple Setup__

    $ pipx install nr.powerline
    $ PS1='`nr powerline` '

The above get's you started quickly, but you will notice a delay in rendering
the powerline. This is mostly because of the overhead of kickstarting the
Python process. To improve performance, Powerline can be started in the
background and communicated with over a Unix socket.

```sh
function _powerline_get() {
  echo "$PWD" | nc -U ~/.local/powerline/daemon.sock 2>/dev/null
  return $?
}
function _powerline() {
  _powerline_get
  if [ $? != 0 ]; then
    if which nr-powerline >/dev/null; then
      nr-powerline --start
      if ! ( nr-powerline --status --exit-code >/dev/null ); then
        echo "Could not start powerline daemon."
      else
        _powerline_get
      fi
    else
      printf "$HOSTNAME $PWD $ "
    fi
  fi
}
export PS1='`_powerline`'
```

__Roadmap__

* Daemon to run in the background to speed up powerline rendering.
* Pass previous status code into `nr-powerline` command.
* Breadcrumb working directory
* Truecolor and xterm-256 color support

### Plugins

The entry point for powerline plugins is `nr.powerline.plugins`. Entry points
must inherit from the `nr.powerline.plugins.Plugin` class.

### Configuration

The powerline can be configured with environment variables.

| Variable | Description |
| -------- | ----------- |
| `NR_POWERLINE_SCRIPT` | Path to a Python script that uses the `nr.powerline` API to render a powerline to stdout. |
| `NR_POWERLINE_CODE` | Actual Python code that uses the `nr.powerline` API to render a powerline to stdout. |

Check the default configuration in `src/nr/powerline/main.py` for an example script.

---

<p align="center">Copyright &copy; 2020 Niklas Rosenstein</p>
