from setuptools import setup

setup(
  name='atlas_sdk',
  version='0.1.0',
  packages=['atlas_sdk'],
  install_requires=[
    'paho-mqtt==1.3.1',
    'python-dateutil==2.7.2',
    'semantic-version==2.6.0',
  ],
)