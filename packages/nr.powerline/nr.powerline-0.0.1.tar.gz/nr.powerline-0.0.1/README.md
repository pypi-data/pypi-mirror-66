# nr.powerline

Simple powerline implementation, only tested in Bash. It is recommended that
you use a font from [NerdFonts](https://nerdfonts.com/#downloads) in order to
have proper support for special characters (like the right triangle).

__Setup__

    $ pipx install nr.powerline
    $ PS1='`nr powerline` '

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
