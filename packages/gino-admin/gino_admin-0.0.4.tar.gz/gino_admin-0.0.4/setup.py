# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gino_admin']

package_data = \
{'': ['*'], 'gino_admin': ['templates/*']}

install_requires = \
['Sanic-Jinja2>=0.7.5,<0.8.0',
 'Sanic>=19.12.2,<20.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'expiring_dict>=1.1.0,<2.0.0',
 'gino>=0.8.7,<0.9.0',
 'passlib>=1.7.2,<2.0.0',
 'sanic-auth>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'gino-admin',
    'version': '0.0.4',
    'description': 'Admin Panel for DB with Gino ORM and Sanic (inspired by Flask-Admin)',
    'long_description': 'gino_admin\n----------\nAdmin Panel for DB with Gino ORM and Sanic (inspired by Flask-Admin)\n\nWork in progress\n\nIf you have time and want to fix:\nPlease open issues with that you want to add\nor write to me in Telegram: @xnuinside or mail: xnuinside@gmail.com\n\n\nVersion 0.0.4 Updates:\n----------------------\n\n1. Upload from CSV - works, added example to `examples/` files. You can upload data from \'.csv\' tables.\n2. Edit per row - now exist button \'edit\'.\n3. Fixed delete for ALL rows of the model\n4. Fixed delete per element.\n5. Now works full \'CRUD\'.\n6. Fixed auth, now it sets \'cookie\' and compare user-agent (for multiple users per login)\n\n\n\nLimitations\n-----------\n\nFor correct work of Admin Panel all models MUST contain unique \'id\' field.\n\'id\' used to identify row (one element) for Edit & Delete operations.\n\nso if you define model, for example, User:\n\n.. code-block:: python\n\n    class User(db.Model):\n\n        __tablename__ = "users"\n\n        id = db.Column(db.String(), unique=True, primary_key=True)\n\n\nSupported operations\n--------------------\n\n- One user auth\n- Create item by one for the Model\n- Delete all rows\n- Delete one item\n- Edit existed data\n- Upload data from csv\n\n\nTODO:\n\n- Select multiple for delete\n- Edit multiple\n- Multiple users\n- Set up data presets (drop table for some data state, defined from csv)\n- Filters in columns\n- Actions history\n\n\nScreens:\n--------\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/auth.png\n  :width: 250\n  :alt: Simple auth\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/add_item.png\n  :width: 250\n  :alt: Add item\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/table_view.png\n  :width: 250\n  :alt: Table view\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/csv_upload.png\n  :width: 250\n  :alt: Add rows from CSV upload\n\n\nContributions\n---------------\n\nContributions and feature requests are very welcome!\n\n\nDeveloper guide\n_______________\n\nProject use pre-commit hooks, so you need setup them\n\nJust run:\n\n.. code-block:: python\n\n    pre-commit install\n\nto install git hooks in your .git/ directory.\n',
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
