# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openbd']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['openbd = openbd:main']}

setup_kwargs = {
    'name': 'openbd',
    'version': '0.0.3',
    'description': '`openbd` is a package for openBD( https://openbd.jp/ ).',
    'long_description': "`openbd` is a package for openBD( https://openbd.jp/ ).\n::\n\n   from openbd import book_info\n   print(book_info('4764905809'))\n   >>>\n   BookInfo(isbn='9784764905801', title='データ分析ライブラリーを用いた最適化モデルの作り方',\n   subtitle=None, series='Pythonによる 問題解決シリーズ', authors='斉藤 努／著、久保 幹雄／監修',\n   publish='近代科学社', date='2018/12/13', price='3200円', page='224', size='B5変形',\n   content='各種ライブラリを組み合わせることで、シンプルで分かりやすい最適化モデルの作成方法を学ぶ',\n   image='https://cover.openbd.jp/9784764905801.jpg', data=None)\n\nRequirements\n------------\n* Python 3\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install openbd\n\nHistory\n-------\n0.0.1 (2020-3-23)\n~~~~~~~~~~~~~~~~~~\n* first release\n",
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/openbd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
