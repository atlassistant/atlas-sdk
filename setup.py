from setuptools import setup
import os

with open('README.rst', encoding='utf8') as f:
  readme = f.read()

with open('atlas_sdk/version.py') as f:
  version = f.readline().strip()[15:-1]

setup(
  name='atlas_sdk',
  description='Python SDK to interact with atlas',
  long_description=readme,
  url='https://github.com/atlassistant/atlas-sdk',
  author='Julien LEICHER',
  license='GPL-3.0',
  version=version,
  packages=['atlas_sdk', 'atlas_sdk.pubsubs', 'atlas_sdk.facades'],
  include_package_data=True,
  install_requires=[
    'paho-mqtt==1.3.1',
    'python-dateutil==2.7.2',
    'semantic-version==2.6.0',
    'PyYAML==3.12'
  ],
)