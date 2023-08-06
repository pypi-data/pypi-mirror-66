# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pomodorino']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.34,<4.0',
 'dbus-python>=1.2,<2.0',
 'notify2>=0.3.1,<0.4.0',
 'pycairo>=1.18,<2.0']

entry_points = \
{'console_scripts': ['pomodorino = pomodorino:app.main']}

setup_kwargs = {
    'name': 'pomodorino',
    'version': '0.1.0b1',
    'description': 'Simple Pomodoro Timer',
    'long_description': '# Pomodorino\n\n**WORK IN PROGRESS**\n\nPomodorino is a lightweight, simple Pomodoro timer desktop application\nwritten using Python 3 and GTK 3.\n\nWhat sets it apart is that it’s totally FOSS (licensed under GPLv3+)\nand really lightweight.  Alternative Linux apps that I could find were\neither paid and proprietrary or they used rather heavy technologies\nlike Electron.\n\nUsing Pomodorino should be rather straight-forward if you know about\nthe [Pomodoro\nTechnique®](https://en.wikipedia.org/wiki/Pomodoro_Technique) (which\nis a registered trademark of Francesco Cirillo).\n\n## Dependencies\n\n- Python 3\n- [PyGObject](https://pygobject.readthedocs.io/en/latest/)\n- [notify2](https://pypi.org/project/notify2/)\n- [dbus-python](https://pypi.org/project/dbus-python/)\n\n## Installation\n\nTBD\n\n## Contributing & Issues\n\nContributions are welcome!  This section will be expanded prior to\ninitial publication.\n\nPlease report issues at the [issue\ntracker](https://github.com/cadadr/pomodorino/issues).\n\n## Licence\n\nPomodorino is licenced under GPLv3 or later.\n\n    Pomodorino --- Simple Pomodoro timer app\n    Copyright (C) 2019, 2020  Göktuğ Kayaalp <self at gkayaalp dot com>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n',
    'author': 'Göktuğ Kayaalp',
    'author_email': 'self@gkayaalp.com',
    'url': 'https://www.gkayaalp.com/pomodorino.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
