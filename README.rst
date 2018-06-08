atlas-sdk
=========

.. image:: https://travis-ci.org/atlassistant/atlas-sdk.svg?branch=next
    :target: https://travis-ci.org/atlassistant/atlas-sdk


Python SDK to interact with `atlas <https://github.com/atlassistant/atlas>`_. It also serves as a base for the **core** since it defines a lot of shared components.

Installation
------------

pip
~~~

.. code-block:: bash

  $ pip install atlas-sdk

source
~~~~~~

.. code-block:: bash

  $ git clone https://github.com/atlassistant/atlas-sdk.git
  $ cd atlas-sdk
  $ python setup.py install

Testing
-------

.. code-block:: bash

  $ cd tests/
  $ python -m unittest -v