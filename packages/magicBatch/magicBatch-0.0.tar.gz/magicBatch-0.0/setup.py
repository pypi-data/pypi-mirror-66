import os
import sys
import shutil
from setuptools import setup
from warnings import warn

if sys.version_info.major != 3:
    raise RuntimeError('Magic requires Python 3')


setup(name='magicBatch',
      version='0.0',
      description='MAGICbatch',
      author='',
      author_email='',
      package_dir={'': 'src'},
      packages=['magicBatch'],
      install_requires=[
          'numpy>=1.10.0',
          'scipy>=0.14.0',
          'seaborn',
          'scikit-learn',
          'networkx',
          'statsmodels',
          'tables',
          'datatable'
      ],
      scripts=['src/magicBatch/MAGIC.py'],
      )


# get location of setup.py
setup_dir = os.path.dirname(os.path.realpath(__file__))
