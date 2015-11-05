from distutils.core import setup
from setuptools import find_packages
import os
from os.path import splitext
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from glob import glob
from distutils.core import Extension

setup(
  name = 'pytest-fits',
  packages=find_packages('src'),
  package_dir={'': 'src'},
  py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
  include_package_data=True,
  zip_safe=False,
  version = '0.1',
  description = 'pytest-fits description',
  author = 'Pica4x6',
  author_email = 'papicazo@ucm.es',
  url = 'https://github.com/{user_name}/{repo}', # use the URL to the github repo
  download_url = 'https://github.com/{user_name}/{repo}/tarball/0.1',
  keywords = ['FITS', 'plugin', 'pytest'],
  classifiers = [],
  install_requires=[
      'pytest>=2.6.0',
  ],
  entry_points = {
        'pytest11': [
            'pytest_fits = pytest_fits.plugin',
        ]
  },
  ext_modules=[
        Extension(
            splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
            sources=[path],
            include_dirs=[dirname(path)]
        )
        for root, _, _ in os.walk('src')
        for path in glob(join(root, '*.c'))
    ]
)