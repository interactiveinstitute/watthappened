watthappened
============

Analyze and interpret historical and current energy data, store time-based feedback.

Intended for use in combination with [energy-cards](https://github.com/interactiveinstitute/energy-cards) and [energy-screen](https://github.com/interactiveinstitute/energy-screen).

Currently only interprets individuals’ absence and prints to stdout. Usage:

1. Set the database details in `config_priv.py`. See `config_priv.example.py`.
2. Run: `python drivers/last_absence.py`
