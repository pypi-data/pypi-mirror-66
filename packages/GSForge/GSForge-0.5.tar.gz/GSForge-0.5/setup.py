"""
Installation script for GSForge.

This script checks if the ``GSFORGE_INSTALL_CORE`` environment variable exists,
if so the requirements installed are a reduced set, so as to make containers
made this way smaller.

This means that each workflow script made in this way should have its own
requirements.txt file containing any packages used (if you wish to make a
docker image for your script).
"""

import os
from setuptools import setup, find_packages

# These are the packages used by the classes in ''GSForge.models''.
requirements = """
numpy
pandas
xarray
param
""".split()

full_requirements = """
Boruta
bokeh
click
datashader
h5py
holoviews
matplotlib
jupyterlab
graphviz
methodtools
netcdf4
panel
scikit-learn
scipy
seaborn
statsmodels
umap_learn
""".split()


# An optional environment variable can be set to install this package without
# many of its visualization dependencies.
env_install_hook = os.environ.get("GSFORGE_INSTALL_CORE")

if not env_install_hook:
    requirements += full_requirements


setup(
    name='GSForge',
    version='0.5',
    packages=find_packages(),
    url='https://systemsgenetics.github.io/GSForge/',
    license='LICENSE.txt',
    author='Tyler Biggs',
    author_email='tyler.biggs@wsu.edu',
    description='Feature (gene) selection package for gene expression data.',
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require={
        'docs': [
            'nbsite',
            'nbsphinx',
            'selenium',
            'sphinx_ioam_theme',
        ],
        'R_support': [
            'rpy2'
        ]
    }
)
