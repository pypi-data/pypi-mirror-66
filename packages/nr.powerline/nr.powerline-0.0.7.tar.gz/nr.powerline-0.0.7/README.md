# nr.powerline

Simple powerline implementation, only tested in Bash. It is recommended that
you use a font from [NerdFonts](https://nerdfonts.com/#downloads) in order to
have proper support for special characters (like the right triangle).

__Requirements__

- Bash
- Pipx
- Python 3.5+

__Installation__

    $ pipx install nr.powerline
    $ source <(nr-powerline --src bash)

__Roadmap__

* Pass previous status code into `nr-powerline` command.
* Breadcrumb working directory
* Truecolor and xterm-256 color support

__Configuration__

Simply pass the `--file` option when sourcing the bash code. It must point to
a Python script that makes use of the `nr.powerline` API. Example:

```py
from nr.powerline import PowerLine
powerline = PowerLine()
git = powerline.get_plugin('git')

powerline.set_pen('white', 'blue')
powerline.add_part(' {c.GIT_FOLDER} ' if git.project else ' {c.DIRECTORY} ')
powerline.add_part('{session.cwd} !{c.RIGHT_TRIANGLE}')
if git.project:
    powerline.set_pen(None, 'yellow')
    powerline.add_part(' {c.BRANCH} {git.branch} !{c.RIGHT_TRIANGLE}')
    powerline.add_part(' ')
    powerline.clear_pen()
```

---

<p align="center">Copyright &copy; 2020 Niklas Rosenstein</p>
