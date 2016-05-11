import sys
from setuptools import setup, find_packages


install_requires = ['SQLALchemy', 'bottle', 'bottle-sqlalchemy',
                    'WTForms-Alchemy', 'passlib', 'Pillow',
                    'beaker', 'mailer']


setup(name='acr-trombi',
      version="0.1",
      packages=find_packages(),
      description="Trombi ACR",
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires)
