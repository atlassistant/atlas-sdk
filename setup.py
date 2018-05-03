from setuptools import setup

setup(
  name='atlas_sdk',
  description='Python SDK to interact with atlas ',
  author='Julien LEICHER',
  license='GPL-3.0',
  version='1.0.0',
  packages=['atlas_sdk'],
  install_requires=[
    'paho-mqtt==1.3.1',
    'python-dateutil==2.7.2',
    'semantic-version==2.6.0',
  ],
)