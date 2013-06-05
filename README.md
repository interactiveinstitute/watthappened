watthappened
============

Analyze and interpret historical and current energy data, store time-based feedback.

Intended for use in combination with [energy-cards](https://github.com/interactiveinstitute/energy-cards) and [energy-screen](https://github.com/interactiveinstitute/energy-screen).


Installation
------------

1. [Install Pandas.](http://pandas.pydata.org/pandas-docs/stable/install.html)


Testing energykit
-----------------

1. Set the database details in `config_priv.py`. See `config_priv.example.py`.
2. Prepare your environment: `export PYTHONPATH=$PWD/python_modules:$PYTHONPATH`.
3. Run: `python -m energykit.couchm` or: `python -m energykit.fake`.
