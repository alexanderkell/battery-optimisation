[![Build Status](https://travis-ci.org/alexanderkell/battery-optimisation.svg?branch=main)](https://travis-ci.org/alexanderkell/battery-optimisation)

battery_optimisation
==============================

This project looks at the optimisation of domestic batteries with domestic solar photovoltaics attached.

The project's aim is to use reinforcement learning to dispatch a battery source optimally.

Installation
============

Pre-requisite: A virtual environment
------------------------------------

Although not strictly necessary, creating a [conda](https://www.anaconda.com/what-is-anaconda/)
virtual environment is highly recommended: it will isolate users and developers from changes
occuring on their operating system, and from conflicts between python packages. It ensures
reproducibility from day to day.

Create a virtual env including python with:

```bash
> conda create -n battery-optimisation python=3.7
```

Activate the environment with:

```bash
> conda activate battery-optimisation
```

Later, to recover the system-wide "normal" python, deactivate the environment with:

```bash
> conda deactivate
```

Installation of packages
------------------------

Next, to install the required python packages, run:

```bash
> pip install -r requirements.txt
```

Usage
-----

To run the reinforcement learning algorithm, you must run a single file, such as the following:

```bash
> python3 src/models/run_model.py   
```



Important features?
-------------------

- Weather
- Historical load
- Historical weather irradiance
- Generator capacity


Reward
------

- Inverse of electricity price 

Observations
------------

- State of battery charge
- Battery size
- Previous data points
- Time
- Day




