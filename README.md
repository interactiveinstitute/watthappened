watthappened
============

Analyze and interpret historical and current energy data, store time-based feedback.

Intended for use in combination with [energy-cards](https://github.com/interactiveinstitute/energy-cards) and [energy-screen](https://github.com/interactiveinstitute/energy-screen).

Contains EnergyKit, a backend-agnostic library for working with energy measurements.


Installation
------------

1. [Install Pandas.](http://pandas.pydata.org/pandas-docs/stable/install.html)
2. Set the database details in `config_priv.py`. See `config_priv.example.py`.


Documentation
-------------

Start at `docs/_build/html/index.html`.


Running the drivers
-------------------

1. Prepare your environment: `export PYTHONPATH=$PWD/python_modules:$PYTHONPATH`.
2. Run: `tools/runner.py`.


Testing EnergyKit
-----------------

1. Prepare your environment: `export PYTHONPATH=$PWD/python_modules:$PYTHONPATH`.
2. Run: `python -m energykit.couchm` or: `python -m energykit.fake`.
