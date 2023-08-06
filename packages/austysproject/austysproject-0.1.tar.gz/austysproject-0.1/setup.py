try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Austin',
    'author_email': 'austinngo38@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['austy_project'],
    'scripts': ['bin/scri1'],
    'name': 'austysproject'
}

setup(**config)
