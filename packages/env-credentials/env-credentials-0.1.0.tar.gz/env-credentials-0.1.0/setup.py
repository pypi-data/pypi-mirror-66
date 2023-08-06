# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_credentials',
 'django_credentials.management',
 'django_credentials.management.commands',
 'env_credentials']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.9,<3.0', 'python-dotenv>=0.13.0,<0.14.0']

extras_require = \
{'django': ['django>=3.0,<4.0']}

setup_kwargs = {
    'name': 'env-credentials',
    'version': '0.1.0',
    'description': 'A library to maintain and use encrypted .env files.',
    'long_description': "# Env Credentials\n\nManage environment variables use the dotenv pattern with encrypted files.\n\nThis project is an attempted port of the [credentials pattern](https://edgeguides.rubyonrails.org/security.html#custom-credentials)\nfound in Ruby on Rails.\n\n## Installation\n\nUsing pip:\n\n```bash\npip install env-credentials[django]\n```\n\nUsing poetry:\n\n```bash\npoetry add env-credentials[django]\n```\n\n## Usage\n\nInitializing and editing the encrypted credentials file is only supported with Django at this time. Additional CLI\ntooling can be built for framework-less projects or projects using other frameworks.\n\n### Django\n\nAfter adding the dependency to your project, add the Django app\n\n```python\nINSTALLED_APPS = [\n    # ...\n    'django_credentials',\n    # ...\n]\n```\n\nYou can then initialize the credentials files with\n\n```bash\n./manage.py init_credentials\n```\n\nThis will create a two new files called `master.key` and `credentials.env.enc` in your root folder. If a `.gitignore`\nfile exists in the same directory, it will also add `master.key` to it.\n\n**Be sure to ignore your master.key file if the gitignore file cannot be automatically updated.**\n\nYou can then edit the values in the file using\n\n```bash\n./manage.py edit_credentials\n```\n\nBe sure that your `$EDITOR` environment variable is set, as that is what the decrypted file will be opened with.\n\nFinally, to load the values into your environment, you should add the following code to your `wsgi.py` and `manage.py`\nfiles\n\n```python\nfrom env_credentials.credentials import Credentials\n\nCredentials().load()\n```\n",
    'author': 'Chris Muthig',
    'author_email': 'camuthig@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/camuthig/python-env-credentials',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
