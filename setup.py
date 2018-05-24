from setuptools import setup
import os

with open('README.md', encoding='utf8') as f:
  readme = f.read()

setup(
  name='atlas_sdk',
  description='Python SDK to interact with atlas',
  long_description=readme,
  long_description_content_type='text/markdown',
  url='https://github.com/atlassistant/atlas-sdk',
  author='Julien LEICHER',
  license='GPL-3.0',
  version='1.1.3',
  packages=['atlas_sdk'],
  include_package_data=True,
  install_requires=[
    'paho-mqtt==1.3.1',
    'python-dateutil==2.7.2',
    'semantic-version==2.6.0',
  ],
)