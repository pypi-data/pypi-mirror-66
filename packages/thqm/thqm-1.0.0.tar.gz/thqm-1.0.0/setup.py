# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thqm']

package_data = \
{'': ['*'],
 'thqm': ['static/favicon.png',
          'static/favicon.png',
          'static/index.css',
          'static/index.css',
          'templates/*']}

install_requires = \
['flask>=1.1.1,<2.0.0', 'pyqrcode>=1.2.1,<2.0.0', 'waitress>=1.4.3,<2.0.0']

entry_points = \
{'console_scripts': ['thqm = thqm.__main__:main']}

setup_kwargs = {
    'name': 'thqm',
    'version': '1.0.0',
    'description': 'thqm, WSGI server providing simple remote hotkey and command execution on host.',
    'long_description': '# thqm\n> Control your desktop from your phone\n\n\n<p align="center">\n <img src="./images/logo.svg" width="200">\n</p>\n\n`thqm` (pronounced tahakoom from the arabic \xd8\xaa\xd8\xad\xd9\x83\xd9\x85  meaning control).\n\n`thqm` starts a `waitress` WSGI server on the host machine and allows the client to run pre-configured commands\n& hotkeys on the host machine. This allows for simple remote command & hotkey execution.\n\nA few nice use cases are:\n  * Media playback control\n  * Volume control\n  * Download/torrent control\n  * Control other web applications e.g. Jupyter notebook server\n\n# Installation\n```shell\npip install thqm\n```\n`thqm` is compatible with linux & MacOS (maybe windows ?, though probably not the hotkeys).\n\n# Dependencies\n\n  * `python3`\n  * `flask`\n  * `pyqrcode`\n  * `waitress`\n\nFor hotkey execution:\n  * linux: `xdotool`\n  * MacOS: `osascript`\n\n# Usage\n\nTo start the `thqm` server, on the host machine, simply run:\n```shell\nthqm\n```\nThe help:\n```\nusage: thqm [-h] [-c CONFIG] [-p PORT] [-q] [-v]\n\nRemote command and hotkey execution server.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG, --config CONFIG\n                        Path to config file. (default:\n                        /home/lcoyle/.config/thqm/config)\n  -p PORT, --port PORT  Port number. (default: 8800)\n  -q, --qrcode          Show the qrcode. (default: False)\n  -v, --verbosity       Verbosity of the waitress server. -v will print\n                        events. -vv will print server messages. (default: 0)\n```\n\nThe `-q` flag will print a qr-code in the terminal, this qr-code will bypass the `thqm-auth` authentication, the same is true for the in browser qr-code, this makes it particularly easy to share access with others.\n<p align="center">\n <img src="./images/thqm_phone_portrait.png" width="200" />\n</p>\n\n# Configuration\n\n`thqm` reads a configuration file located at `$XDG_CONFIG_HOME/thqm/config` (or `$HOME/.config/thqm/config` if `$XDG_CONFIG_HOME` if not defined). This `ini` format file contains the pre-configured commands & hotkeys.\n\nEach `ini` block can have the following structure:\n```ini\n[event name]        # name of the event\nexec_cmd=...        # command to execute\nexec_hotkey=...     # hotkey to execute (on linux use xdotool key names, on macos use osascript key names)\nicon_path=...       # (optional) icon of the the event\n```\nif the event has both an `exec_cmd` and an `exec_hotkey` the command is run prior to running the hotkey.\n\nHere would be the contents for media playback and audio control:\n```ini\n# requires pactl\n[Raise volume]\nexec_cmd=pactl set-sink-volume @DEFAULT_SINK@ +10%\n\n[Lower volume]\nexec_cmd=pactl set-sink-volume @DEFAULT_SINK@ -10%\n\n[Toggle mute]\nexec_cmd=pactl set-sink-mute @DEFAULT_SINK@ toggle\n\n# using media keys\n[Media previous]\nexec_hotkey=XF86AudioPrev\n\n[Media next]\nexec_hotkey=XF86AudioNext\n\n[Media play]\nexec_hotkey=XF86AudioPlay\n\n[Media pause]\nexec_hotkey=XF86AudioPause\n\n# browser control\n[play/pause]\nexec_hotkey=space\n\n[scrub back]\nexec_hotkey=Left\n\n[scrub forward]\nexec_hotkey=Right\n```\n\nIf you want rudimentary authentication, add the `thqm-auth` block, with the `password` key, **don\'t use a real password, the encryption isn\'t secure**:\n```ini\n[thqm-auth]\npassword=super_secret_password\n```\n\n',
    'author': 'Loic Coyle',
    'author_email': 'loic.coyle@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/loiccoyle/thqm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
