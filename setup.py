"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# parent_dir = path.abspath(path.join(here, 'src'))
# sys.path.append(parent_dir)

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    version = f.read().strip()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='case',
    version=version,
    keywords='archive database flask',
    description='Cases for archive',
    long_description=long_description,
    url='https://github.com/garhivelg/case',

    author='Dmitry Kutsenko',
    author_email='d2emon@gmail.com',

    license='GPL-3.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],

    # package_dir={'': 'src'},
    packages=find_packages(exclude=['tests']),
    # py_modules=[]
    install_requires=requirements,
)
