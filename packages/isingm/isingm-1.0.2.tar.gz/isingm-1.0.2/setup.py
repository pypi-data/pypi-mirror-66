# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isingm']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'numpy>=1.18.2,<2.0.0']

setup_kwargs = {
    'name': 'isingm',
    'version': '1.0.2',
    'description': 'A pythonic Ising model simulation',
    'long_description': "![wheel](https://img.shields.io/pypi/wheel/isingm?style=plastic)\n![implementation](https://img.shields.io/pypi/implementation/isingm)\n![python](https://img.shields.io/pypi/pyversions/isingm)\n![downloads](https://img.shields.io/pypi/dm/isingm)\n\n# Ising\nA pythonic implementation of the Ising model.\n\nCheck the example for more.\n\n\n## Lattice\nThis is the main place of the Ising model,\nwe have to initialize it with a tuple of the lattice shape that can be of any dimension or size.\nThe lattice can be initialized with a random state (you can choose the state ratio up) or all in a state 1 or -1.\n\n### arguments:\n\n- ##### shape:\n\n>   type: **tuple(int)**\n>\n>   The shape of the lattice is tested for 1 to 4 dimension.\n>   Every values of shape must be > 0 \n\n#### Optionnal:\n\n- ##### all:\n\n>    type: **int** == 1 or -1\n>\n>    Set the state at all 1 or -1 it overpass the r parrameter.\n\n- ##### r: \n\n>   type: **float** in [0, ..., 1]\n>\n>  Set a random state with a ratio r of 1 in the lattice (default r = 0.5).\n\n- ##### adj: \n\n>   type: **numpy.array**\n>\n>   A vector of vector: is the representation of the spin interaction.\n>\n>   |  0  |  J  |  0  |\n>   | --- | --- | --- |\n>   |**J**|**#**|**J**| \n>   |**0**|**J**|**0**| \n>\n>   Will be written as [[1,0],[-1,0],[0,1],[0,-1]]\n>   \n>   As default it's the left right up down direct neighbor matrix will be genereted (whatever this mean in 4 or more dimensions).\n\n- ##### J:\n\n>   type: **numpy.array** or **float**\n>\n>   Is the interraction between spins, \n>   if J is an array he as to be the same length than adj.\n>\n>   (you can choose to make anisotropic iteractions !!)\n\n- ##### B:\n\n>   type: **numpy.array** or **float**\n>\n>   Is the magnetic field imposed on the lattice,\n>   if B is an array he as to have the same shape of the lattice\n\n- ##### beta:\n\n>   type: **float**\n>\n>   Beta is 1/(Kb * T) with T the absolute temp,\n>   and Kb is the Boltzmann constant.\n\n\n## Methods\n\n### randomize(self, ratio=0.5):\n\nRandomize th lattice state with a given ratio of up state.\n\n### arguments:\n\n#### Optionnal:\n\n- ##### ratio:\n\n>   type: **float** in [0, ..., 1]\n>\n>   The ratio of up state. \n\n### all(self, state):\n\nSet all the lattice to the same state.\n\n### arguments:\n\n- ##### state:\n\n>   type: **int** == -1 or 1\n>\n>   Value of the spin site.\n\n### mag(self):\n\nCompute the magnetization of the lattice.\n\n### returns:\n\n- ##### Magnetization\n\n>   type: **float** \n>\n>   Magnetization of the lattice.\n\n### hamiltonian(self):\n\nCompute the Halmitonian of each spin.\n\n### returns:\n\n- ##### local_Hamiltonian:\n\n>   type: **numpy array** \n>\n>   The Hamiltonian calculated for each spin.\n\n### H(self):\n\nCompute the Hamiltonian of the lattice.\n\n### returns:\n\n- ##### Hamiltonian\n\n>   type: **float** \n>\n>   Hamiltonian of the lattice.\n\n### mH(self):\n\nCompute the mean value of the Hamiltonian.\n\n### returns:\n\n- ##### <H>\n\n>   type: **float** \n>\n>   Mean value of the Hamiltonian.\n\n### get_state(self):\n\nMethod to get the state of the lattice.\n\n### returns:\n\n- ##### state:\n\n>   type: **numpy array** \n>\n>   Return the copy of the state.\n\n### set_state(self, state):\n\nMethod to set the state of the lattice.\n\n### arguments:\n\n- ##### state:\n\n>   type: **numpy array** \n>\n>   The new state.\n\n\n## Metropolis.algorithm\nIs the class who solve the Ising model with the **Metropolis algorithm**\n\nImplementation of the Metropolis algorithm\n\n### arguments:\n    \n-   **for the arguments look the lattice class.**\n\n## Methods\n\n### step(self, n=0):\n\n    ### arguments:\n    \n    -   **for the arguments look the lattice class.**\n\n## Methods\n\nstep(self, n=0):\n\nstep apply the metropolis algorithm on n spin once\n\n### arguments:\n\n#### Optional:\n\n- ##### n:\n\n>   type: **int**\n>\n>   n must be strictly positive is the size of the sample \n",
    'author': 'pacidus',
    'author_email': 'pacidus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Pacidus/isingm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
