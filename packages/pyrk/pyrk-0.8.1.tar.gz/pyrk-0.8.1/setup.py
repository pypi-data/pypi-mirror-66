# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrk']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

setup_kwargs = {
    'name': 'pyrk',
    'version': '0.8.1',
    'description': 'ode integration rk4 rk runge kutta',
    'long_description': '![Header pic](https://github.com/walchko/pyrk/raw/master/pics/math2.jpg)\n\n# Runge-Kutta 4\n\n[![Actions Status](https://github.com/walchko/pyrk/workflows/pytest/badge.svg)](https://github.com/walchko/pyrk/actions)\n![PyPI - License](https://img.shields.io/pypi/l/pyrk.svg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyrk.svg)\n![PyPI - Format](https://img.shields.io/pypi/format/pyrk.svg)\n![PyPI](https://img.shields.io/pypi/v/pyrk.svg)\n\nA simple implementation of\n[Runge-Kutta](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods)\nfor python. This supports both python 2 and python 3.\n\n## Setup\n\n### Install\n\nThe preferred method of installation is: `pip install pyrk`\n\n### Develop\n\n```\ngit clone https://github.com/walchko/pyrk\ncd pyrk\npoetry build\npoetry install\n```\n\n## Usage\n\nSee the examples in the\n[docs](https://github.com/walchko/pyrk/blob/master/doc/runge-kutta.ipynb)\nfolder or a simple one:\n\n``` python\nfrom __future__ import division, print_function\nfrom pyrk import RK4\nimport numpy as np\nimport matplotlib.pyplot as plt\n\ndef vanderpol(t, xi, u):\n    dx, x = xi\n    mu = 4.0 # damping\n\n    ddx = mu*(1-x**2)*dx-x\n    dx = dx\n\n    return np.array([ddx, dx])\n\nrk = RK4(vanderpol)\nt, y = rk.solve(np.array([0, 1]), .01, 200)\n\ny1 = []\ny2 = []\nfor v in y:\n    y1.append(v[0])\n    y2.append(v[1])\n\nplt.plot(y1, y2)\nplt.ylabel(\'velocity\')\nplt.xlabel(\'position\')\nplt.grid(True)\nplt.show()\n```\n\n# MIT License\n\n**Copyright (c) 2015 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a\ncopy of this software and associated documentation files (the\n"Software"), to deal in the Software without restriction, including\nwithout limitation the rights to use, copy, modify, merge, publish,\ndistribute, sublicense, and/or sell copies of the Software, and to\npermit persons to whom the Software is furnished to do so, subject to\nthe following conditions:\n\nThe above copyright notice and this permission notice shall be included\nin all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS\nOR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\nIN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY\nCLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,\nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE\nSOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pyrk/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
