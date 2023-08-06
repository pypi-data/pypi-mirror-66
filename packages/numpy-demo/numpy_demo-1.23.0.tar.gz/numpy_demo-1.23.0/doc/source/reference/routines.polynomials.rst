.. _routines.polynomial:

Polynomials
***********

Polynomials in NumPy can be *created*, *manipulated*, and even *fitted* using
the :doc:`convenience classes <routines.polynomials.classes>`
of the `numpy_demo.polynomial` package, introduced in NumPy 1.4.

Prior to NumPy 1.4, `numpy_demo.poly1d` was the class of choice and it is still
available in order to maintain backward compatibility.
However, the newer Polynomial package is more complete than `numpy_demo.poly1d`
and its convenience classes are better behaved in the numpy_demo environment.
Therefore :mod:`numpy_demo.polynomial` is recommended for new coding.

Transition notice
-----------------
The  various routines in the Polynomial package all deal with
series whose coefficients go from degree zero upward,
which is the *reverse order* of the Poly1d convention.
The easy way to remember this is that indexes
correspond to degree, i.e., coef[i] is the coefficient of the term of
degree i.


.. toctree::
   :maxdepth: 1

   routines.polynomials.classes
   routines.polynomials.polynomial
   routines.polynomials.chebyshev
   routines.polynomials.hermite
   routines.polynomials.hermite_e
   routines.polynomials.laguerre
   routines.polynomials.legendre
   routines.polynomials.polyutils


.. toctree::
   :maxdepth: 2

   routines.polynomials.poly1d
