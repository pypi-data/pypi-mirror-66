# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gino_admin']

package_data = \
{'': ['*'], 'gino_admin': ['templates/*']}

install_requires = \
['Sanic-Jinja2>=0.7.5,<0.8.0',
 'Sanic>=19.12.2,<20.0.0',
 'gino>=0.8.7,<0.9.0',
 'passlib>=1.7.2,<2.0.0',
 'sanic-auth>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'gino-admin',
    'version': '0.0.1',
    'description': 'Admin Panel for DB with Gino ORM and Sanic (inspired by Flask-Admin)',
    'long_description': 'gino_admin\n----------\nAdmin Panel for DB with Gino ORM and Sanic (inspired by Flask-Admin)\n\nWork in progress\n\n\nSupported operations\n--------------------\n\n- Simple auth\n- Create item by one for the Model\n- Delete all rows\n\n\nIn process:\n\n- Upload rows from csv\n- Delete item\n- Edit item\n- Select multiple for delete\n- Edit multiple\n\n\nScreens:\n--------\n\n.. image:: docs/img/auth.png\n  :width: 250\n  :alt: Simple auth\n\n.. image:: docs/img/add_item.png\n  :width: 250\n  :alt: Add item\n\n.. image:: docs/img/table_view.png\n  :width: 250\n  :alt: Table view\n\n\nContributions\n---------------\n\nContributions and feature requests are very welcome!\n\n',
    'author': 'xnuinside',
    'author_email': 'xnuinside@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xnuinside/gino_admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
