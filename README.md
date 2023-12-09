[![Unit Tests](https://github.com/alexanderkell/battery-optimisation/actions/workflows/pytest.yaml/badge.svg)](https://github.com/alexanderkell/battery-optimisation/actions/workflows/pytest.yaml)

Battery Optimisation
==============================

This project looks at the optimisation of domestic batteries with domestic solar photovoltaics attached.

The project's aim is to use reinforcement learning to optimally dispatch a battery source.

Publication
===========
Kell, A.J., Stephen McGough, A. and Forshaw, M. (2022) ‘Optimizing a domestic battery and solar photovoltaic system with Deep Reinforcement Learning’, 2022 IEEE International Conference on Big Data (Big Data) [Preprint]. [doi:10.1109/bigdata55660.2022.10021028](https://doi.org/10.1109/bigdata55660.2022.10021028).

Abstract
========
This study introduces a state-of-the-art method for optimizing home battery and solar systems using deep reinforcement learning. It focuses on improving battery performance in solar-battery systems, significantly reducing household electricity costs. 

The deep learning algorithm adapts to changing energy needs and solar outputs, enhancing energy management. The Figures below highlight the impact of different battery sizes and the algorithm's effectiveness. 

<p float="left">
  <img src="/reports/figures/best_controller_plot.png" width="400" />
  <img src="/reports/figures/testing_barchat.png" width="400" /> 
</p>



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

Repository Structure
====================
```
├── LICENSE 
├── README.md
├── data
│   ├── interim
│   ├── models
│   ├── processed
│   ├── raw
│   └── results
├── notebooks
│   ├── data_munging
│   ├── exploration
│   ├── features
│   ├── modelling
│   └── results
├── references
│   └── Ausgrid solar home electricity data notes (Aug 2014).pdf
├── reports
│   └── figures
├── requirements.in
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── __pycache__
│   ├── data
│   └── models
└── test
    ├── __init__.py
    └── test_model.py
```

