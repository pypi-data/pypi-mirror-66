# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['four_color']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.1,<8.0.0',
 'flask>=1.1.2,<2.0.0',
 'networkx>=2.4,<3.0',
 'pulp>=2.1,<3.0']

setup_kwargs = {
    'name': 'four-color',
    'version': '0.0.6',
    'description': '`four_color` is a package for Four Color Problem.',
    'long_description': '`four_color` is a package for Four Color Problem.\n::\n\n* Download picture from https://www.dropbox.com/s/twiscp9h15so8no/sample.png?dl=1\n* `python -m four_color`\n* Open http://localhost:8000/\n* Set "sample.png" and push "send" button.\n* Download "fig.png".\n\n.. image:: https://raw.githubusercontent.com/SaitoTsutomu/four_color/master/fig.gif\n   :scale: 200%\n\nRequirements\n------------\n* Python 3, Pillow, Flask, NetworkX, PuLP\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install four_color\n\nHistory\n-------\n0.0.1 (2016-6-13)\n~~~~~~~~~~~~~~~~~~\n* first release\n',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/four_color',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
