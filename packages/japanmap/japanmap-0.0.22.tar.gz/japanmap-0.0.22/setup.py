# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['japanmap']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.1.1,<8.0.0', 'numpy>=1.18.2,<2.0.0', 'opencv-python>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'japanmap',
    'version': '0.0.22',
    'description': '`japanmap` is a package for Japanese map.',
    'long_description': "`japanmap` is a package for Japanese map.\n::\n\n   import matplotlib.pyplot as plt\n   from japanmap import picture, get_data, pref_map\n   pct = picture({'北海道': 'blue'})  # numpy.ndarray\n   # pct = picture({1: 'blue'})  # same to above\n   plt.imshow(pct)  # show graphics\n   plt.savefig('map.png')  # save to PNG file\n   svg = pref_map(range(1,48), qpqo=get_data())  # IPython.display.SVG\n   print(svg.data)  # SVG source\n\nRequirements\n------------\n* Python 3, Numpy\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install japanmap\n\nHistory\n-------\n0.0.1 (2016-6-7)\n~~~~~~~~~~~~~~~~~~\n* first release\n",
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/japanmap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
