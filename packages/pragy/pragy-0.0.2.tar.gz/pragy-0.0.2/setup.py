from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.2'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pragy',
    version=__version__,
    description='Pragy Agarwal - digital visiting card',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AgarwalPragy/pragy',
    download_url='https://github.com/AgarwalPragy/pragy/tarball/' + __version__,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='pragy',
    include_package_data=True,
    author='Pragy Agarwal',
    author_email='agar.pragy@gmail.com'
)
