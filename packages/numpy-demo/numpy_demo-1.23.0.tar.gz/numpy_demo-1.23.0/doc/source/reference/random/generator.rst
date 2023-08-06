.. currentmodule:: numpy_demo.random

Random Generator
----------------
The `~Generator` provides access to
a wide range of distributions, and served as a replacement for
:class:`~numpy_demo.random.RandomState`.  The main difference between
the two is that ``Generator`` relies on an additional BitGenerator to
manage state and generate the random bits, which are then transformed into
random values from useful distributions. The default BitGenerator used by
``Generator`` is `~PCG64`.  The BitGenerator
can be changed by passing an instantized BitGenerator to ``Generator``.


.. autofunction:: default_rng

.. autoclass:: Generator
	:exclude-members:

Accessing the BitGenerator
==========================
.. autosummary::
   :toctree: generated/

   ~numpy_demo.random.Generator.bit_generator

Simple random data
==================
.. autosummary::
   :toctree: generated/

   ~numpy_demo.random.Generator.integers
   ~numpy_demo.random.Generator.random
   ~numpy_demo.random.Generator.choice
   ~numpy_demo.random.Generator.bytes

Permutations
============
.. autosummary::
   :toctree: generated/

   ~numpy_demo.random.Generator.shuffle
   ~numpy_demo.random.Generator.permutation

Distributions
=============
.. autosummary::
   :toctree: generated/

   ~numpy_demo.random.Generator.beta
   ~numpy_demo.random.Generator.binomial
   ~numpy_demo.random.Generator.chisquare
   ~numpy_demo.random.Generator.dirichlet
   ~numpy_demo.random.Generator.exponential
   ~numpy_demo.random.Generator.f
   ~numpy_demo.random.Generator.gamma
   ~numpy_demo.random.Generator.geometric
   ~numpy_demo.random.Generator.gumbel
   ~numpy_demo.random.Generator.hypergeometric
   ~numpy_demo.random.Generator.laplace
   ~numpy_demo.random.Generator.logistic
   ~numpy_demo.random.Generator.lognormal
   ~numpy_demo.random.Generator.logseries
   ~numpy_demo.random.Generator.multinomial
   ~numpy_demo.random.Generator.multivariate_hypergeometric
   ~numpy_demo.random.Generator.multivariate_normal
   ~numpy_demo.random.Generator.negative_binomial
   ~numpy_demo.random.Generator.noncentral_chisquare
   ~numpy_demo.random.Generator.noncentral_f
   ~numpy_demo.random.Generator.normal
   ~numpy_demo.random.Generator.pareto
   ~numpy_demo.random.Generator.poisson
   ~numpy_demo.random.Generator.power
   ~numpy_demo.random.Generator.rayleigh
   ~numpy_demo.random.Generator.standard_cauchy
   ~numpy_demo.random.Generator.standard_exponential
   ~numpy_demo.random.Generator.standard_gamma
   ~numpy_demo.random.Generator.standard_normal
   ~numpy_demo.random.Generator.standard_t
   ~numpy_demo.random.Generator.triangular
   ~numpy_demo.random.Generator.uniform
   ~numpy_demo.random.Generator.vonmises
   ~numpy_demo.random.Generator.wald
   ~numpy_demo.random.Generator.weibull
   ~numpy_demo.random.Generator.zipf
