import os
from setuptools import setup, find_packages
from shell import __author__, __version__

def __read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='shell',
    author=__author__,
    author_email='andreykus@gmail.com',
    version=__version__,
    description='Системный монитор',
    platforms=('Windows'),
    packages=find_packages(),
    install_requires=required,  
    keywords='bivgroup,diasoft,monitor'.split(),
    include_package_data=True,
    license='BSD License',
    package_dir={'shell': 'shell'},
    url='/pythont/ShellApi/shell/',
    service=[{"script":'shell/monitor.py'}],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Windows',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts':
            ['monitor = shell.monitor']
        }
)