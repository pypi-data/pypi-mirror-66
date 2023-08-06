#!/usr/bin/env python3
# System imports
from distutils.core import Extension, setup

# Third-party modules - we depend on numpy_demo for everything
import numpy_demo

# Obtain the numpy_demo include directory.
numpy_demo_include = numpy_demo.get_include()

# Array extension module
_Array = Extension("_Array",
                   ["Array_wrap.cxx",
                    "Array1.cxx",
                    "Array2.cxx",
                    "ArrayZ.cxx"],
                   include_dirs = [numpy_demo_include],
                   )

# Farray extension module
_Farray = Extension("_Farray",
                    ["Farray_wrap.cxx",
                     "Farray.cxx"],
                    include_dirs = [numpy_demo_include],
                    )

# _Vector extension module
_Vector = Extension("_Vector",
                    ["Vector_wrap.cxx",
                     "Vector.cxx"],
                    include_dirs = [numpy_demo_include],
                    )

# _Matrix extension module
_Matrix = Extension("_Matrix",
                    ["Matrix_wrap.cxx",
                     "Matrix.cxx"],
                    include_dirs = [numpy_demo_include],
                    )

# _Tensor extension module
_Tensor = Extension("_Tensor",
                    ["Tensor_wrap.cxx",
                     "Tensor.cxx"],
                    include_dirs = [numpy_demo_include],
                    )

_Fortran = Extension("_Fortran",
                    ["Fortran_wrap.cxx",
                     "Fortran.cxx"],
                    include_dirs = [numpy_demo_include],
                    )

_Flat = Extension("_Flat",
                    ["Flat_wrap.cxx",
                     "Flat.cxx"],
                    include_dirs = [numpy_demo_include],
                    )

# NumyTypemapTests setup
setup(name        = "NumpyTypemapTests",
      description = "Functions that work on arrays",
      author      = "Bill Spotz",
      py_modules  = ["Array", "Farray", "Vector", "Matrix", "Tensor",
                     "Fortran", "Flat"],
      ext_modules = [_Array, _Farray, _Vector, _Matrix, _Tensor,
                     _Fortran, _Flat]
      )
