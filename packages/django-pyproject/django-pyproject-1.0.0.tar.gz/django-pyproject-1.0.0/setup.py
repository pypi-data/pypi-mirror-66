# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djpp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-pyproject',
    'version': '1.0.0',
    'description': 'A package for storing Django settings in pyproject.toml.',
    'long_description': '# django-pyproject\n\n## Description\n\nThis package allows you to store some/all of your settings in your pyproject.toml file (or any toml file in general).\n\n## Installation\n\nYou can add django-pyproject to your poetry project with:\n\n    poetry add django-pyproject\n\nOr through pip:\n\n    pip install django-pyproject\n\nNeither Django nor Poetry are **not** required to use this package.\n\n## Usage\n\nYou can use django-pyproject to import any settings specified in your pyproject file under [tool.django].\n\n### Settings file\n\nTo import django settings from your pyproject file, use this in your settings file:\n\n    from djpp import pyproject\n    pyproject.load()\n\nThis will work only if you have a standard django project structure.  \nIf your pyproject file is located somewhere else or has a different name, you can specify it:\n\n    pyproject.load(\'path-to-your-pyproject-file\')\n\n### PyProject file\n\nAll django settings in pyproject.toml file should be stored under [tool.django] key, like this:\n\n    [tool.django]\n    ALLOWED_HOSTS = []\n\nYou don\'t have to use uppercase letters for the variable names, django-pyproject will automatically convert them all. This does **not** work for dict key names:\n\n    [tool.django]\n    allowed_hosts = []\n\n    [tool.django.databases.default]\n    engine = \'django.db.backends.sqlite3\'\n    HOST = \'127.0.0.1\'\n    PORT = \'5432\'\n\nWill convert into:\n\n    ALLOWED_HOSTS = []\n    DATABASES = {\n        \'default\': {\n            \'engine\': \'django.db.backends.sqlite3\',\n            \'HOST\': \'127.0.0.1\',\n            \'PORT\': \'5432\',\n        }\n    }\n\nBut what to do about relative filepaths, that you had to construct with os.path?  \nYou can specify filepaths separating them with \'/\' in inline dict under key \'path\'.  \nUsing \'..\' will make django-pyproject go up a level.\nStarting with \'.\' will make a path relative:\n\n    base_dir = { path = "." }\n    project_dir = { path = "./your_project_folder" }\n    repo_dir = { path = "./.." }\n\nThis will have the same effect as the following code in settings.py:\n\n    import os\n    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))\n    REPO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n\n> This is assuming you have a standard django project structure.\n\nIf a value needs to be taken from an environment, use inline dict with key \'path\' and optional key \'default\':\n\n    email_host_password = { env = \'SECRET_PASSWORD\' }\n    secret_key = { env = \'SECRET_KEY\', default = \'hello\' }\n\n### Docker & Production\n\nIf some of you settings have an alternative value for when DEBUG is off, specify them in [tool.django.production]. They will override regular settings if DEBUG is off.\n\nBy default, django-pyproject applies production settings and sets DEBUG to False, if current evironment has a DJANGO_ENV variable, set to \'production\'.  \nYou can override it with your own key and value like this:\n\n    pyproject.load(production_env=(\'YOUR_KEY\', \'your_value\'))\n\nIf some of you settings have an alternative value for when the app is in container, specify them in [tool.django.docker]. They will override regular settings and will be overriden by production settings.\n\nBy default, django-pyproject applies docker settings, if current evironment has a DJANGO_ENV variable.  \nYou can override it with your own key like this:\n\n    pyproject.load(docker_env=\'YOUR_KEY\')\n\n### Apps\n\nYou can group settings that belong to an external app together for easier access.  \nTo do that, you can list them under [tool.django.apps.your_app].  \nYou can also modify variables like INSTALLED_APPS from here with \'insert\' key.\n\nHere\'s an example for corsheaders:\n\n    [tool.django.apps.cors]\n    CORS_ORIGIN_WHITELIST = [\'http://localhost:3000\',]\n    CORS_ALLOW_CREDENTIALS = true\n    CSRF_COOKIE_NAME = "XCSRF-Token"\n    INSTALLED_APPS = { insert = \'corsheaders\' }\n    MIDDLEWARE = { insert = \'corsheaders.middleware.CorsMiddleware\', pos = 3 }\n\nThis is similar to the following python code:\n\n    CORS_ORIGIN_WHITELIST = (\'http://localhost:3000\',)\n    CORS_ALLOW_CREDENTIALS = True\n    CSRF_COOKIE_NAME = "XCSRF-Token"\n    INSTALLED_APPS.append(\'corsheaders\')\n    MIDDLEWARE.insert(3, \'corsheaders.middleware.CorsMiddleware\')\n\n### Full import\n\nYou also can simply import pyproject file (or any toml file) contents as a dict with load_all().\n',
    'author': 'Ceterai',
    'author_email': 'ceterai@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
