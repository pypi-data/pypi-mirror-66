###########
Development
###########


Installation
============

The Python package manager is `PIP`_.

We strongly suggest that you use `pyenv`_.

The following steps have been tested on Ubuntu 18.04.

Install `PIP`_ and `VirtualEnv`_:

.. prompt:: bash

    sudo apt install -y python3-pip python3-venv

Install `pyenv`_:

.. prompt:: bash

    curl https://pyenv.run | bash

Clone the repository:

.. prompt:: bash

    git clone https://gitlab.com/ddidier/python-ndd-test4p.git
    cd python-ndd-test4p

Install the Python versions specified in the ``.python-version`` file,
and if the Python compilation fails because of an unmet dependency,
have a look at https://github.com/pyenv/pyenv/wiki/common-build-problems:

.. prompt:: bash

    pyenv install 3.6.10
    pyenv install 3.7.7
    pyenv install 3.8.2

Create and activate the environments specified in the ``.python-version`` file:

.. prompt:: bash

    # for example:
    pyenv virtualenv 3.6.10 ndd-test4p_3.6.10
    pyenv virtualenv 3.7.7  ndd-test4p_3.7.7
    pyenv virtualenv 3.8.2  ndd-test4p_3.8.2

Upgrade PIP for each environment:

.. prompt:: bash

    pip install --upgrade pip

Install all the required dependencies:

.. prompt:: bash

    pip install -e .
    pip install -e .[testing]
    pip install -e .[documenting]
    pip install -e .[distributing]


Development & Test
==================

Test the library within your current environment:

.. prompt:: bash

    python setup.py test

Test the library within all the supported environments:

.. prompt:: bash

    tox --parallel auto

Run the Python linters for the sources:

.. prompt:: bash

    pylint src/
    flake8 src/

Run the Python linters for the tests:

.. prompt:: bash

    pylint --rcfile=.pylintrc-tests tests/**/*.py
    flake8 --config=.flake8-tests tests/

Test the documentation examples:

.. prompt:: bash

    python setup.py doctest


Documentation
=============

Generate the documentation:

.. prompt:: bash

    python setup.py docs


Distribution
============

Generate the Wheels package:

.. prompt:: bash

    python setup.py bdist_wheel sdist


Notes
=====

This project has been set up using PyScaffold 3.2.1.
For details and usage information on PyScaffold see https://pyscaffold.org/.


References
==========

.. _PIP: https://en.wikipedia.org/wiki/Pip_(package_manager)
.. _pyenv: https://github.com/pyenv/pyenv
.. _VirtualEnv: https://virtualenv.pypa.io/
.. _VirtualEnvWrapper: https://virtualenvwrapper.readthedocs.io/

- `PIP`_
- `pyenv`_
- `VirtualEnv`_
- `VirtualEnvWrapper`_
