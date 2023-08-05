from setuptools import setup

setup(
    name = 'pyessentials',
    version = '1.0.0',
    author = 'Doomhawk',
    author_email = 'admin@doomhawk.org',
    license = 'MIT',
    packages = ['pyessentials',],
    install_requires = ['flask', 'gevent',],
    zip_safe = False)