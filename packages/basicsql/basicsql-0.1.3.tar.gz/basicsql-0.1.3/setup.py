# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basicsql']

package_data = \
{'': ['*']}

install_requires = \
['jinjasql>=0.1.7,<0.2.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.0.1,<2.0.0',
 'sqlalchemy>=1.3.13,<2.0.0']

setup_kwargs = {
    'name': 'basicsql',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Basic SQL\n\nThis is a small package intended to help with executing (mainly) raw SQL queries for different databases.\n\n## Additional requirements\n\nThe package is using SQLAlchemy and depending on what database you want to connect to the installation of additional packages is required. Below are the instructions for the databases that are currently supported:\n\n### Oracle\n```\npip install cx_Oracle\n```\n### PostgreSQL\n```\npip install psycopg2\n```\n\n### SQL Server (MSSQL)\n```\npip install pyodbc\n```\n\nOn Linux first follow the [Microsoft instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15) to install the required drivers.\n\n### MySQL\n```\npip install pymysql\n```',
    'author': 'Ramon Brandt',
    'author_email': 'devramon22@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
