attgen
======

.. contents:: **Table of Contents**
    :backlinks: none

Description
-----------

attgen is a tool to generate a french certificate during the COVID-19 confinment.
I give it not for the real usage you may have with it but for given the code I use
to play with pdfrw and reportlab libraries.


Installation
------------

attgen is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 2.7/3.5+ and PyPy.

.. code-block:: bash

    $ pip install attgen

Usage
-----

.. code-block:: bash

    $ attgen --help
    usage: attgen [-h] [--verbose] [--conf CONF] [--time TIME] [--out OUT]

    optional arguments:
    -h, --help            show this help message and exit
    --verbose, -v         increase output verbosity
    --conf CONF, -c CONF  Add a configuration file
    --time TIME, -t TIME  Set begin time (eg. 15h12)
    --out OUT, -o OUT     Set the output filename

The configuration file is a yaml file:

.. code-block:: yaml

    global_data:
      adresse: '1 rue de la place, 75000 Paris'
      ville: "Paris"

    reasons: sport
    # reasons: "travail courses sante famille sport judiciaire missions"

    data:
      - lastname: 'Jean'
        firstname: 'Michel'
        birthday: '01/01/1970'
        town: "Amiens"
      - lastname: 'Jean'
        firstname: 'Marie'
        birthday: '01/01/1970'
        town: "Amiens"

    inputs: /tmp/certificate.pdf

This Config file can be also put in the Home directory under ${HOME}/.attgen
and will be read at the beginning of the execution.

Examples of usage:

.. code-block:: bash

    attgen
    attgen -t 15:00
    attgen -o /tmp/my_certificate.pdf
    attgen -c my_config_file.yaml
    attgen -c my_config_file.yaml -o /tmp/my_certificate.pdf -t 15:00

License
-------

attgen is distributed under the terms of

- `Apache License, Version 2.0 <https://choosealicense.com/licenses/apache-2.0>`_
