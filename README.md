Battery Optimisation
==============================

This project looks at the optimisation of domestic batteries with domestic solar photovoltaics attached.

The project's aim is to use reinforcement learning to optimally dispatch a battery source.

Publications
------------
- [Optimizing a domestic battery and solar photovoltaic system with deep reinforcement learning](https://ieeexplore.ieee.org/abstract/document/10021028)
- [Open access version](https://arxiv.org/pdf/2109.05024.pdf)

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
> pip install -r requirements.in
```

Usage
-----

To run the reinforcement learning algorithm, you must run a single file, such as the following:

```bash
> python3 src/models/run_model.py   
```

Training
--------

To visualise the training in real-time, it is possible to use tensorboard. To start tensorboard, you must find your `ray_results/` folder. This is usually in `~/ray_results/`. The following code should work to get tensorboard started:

```bash
> tensorboard --logdir=~/ray_results/
```

You can then view the training by navigating to `http://localhost:6007/` in a browser.


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




