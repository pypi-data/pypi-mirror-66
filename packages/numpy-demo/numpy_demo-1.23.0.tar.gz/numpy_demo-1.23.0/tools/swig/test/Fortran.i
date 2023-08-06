// -*- c++ -*-
%module Fortran

%{
#define SWIG_FILE_WITH_INIT
#include "Fortran.h"
%}

// Get the NumPy typemaps
%include "../numpy_demo.i"

%init %{
  import_array();
%}

%define %apply_numpy_demo_typemaps(TYPE)

%apply (TYPE* IN_FARRAY2, int DIM1, int DIM2) {(TYPE* matrix, int rows, int cols)};

%enddef    /* %apply_numpy_demo_typemaps() macro */

%apply_numpy_demo_typemaps(signed char       )
%apply_numpy_demo_typemaps(unsigned char     )
%apply_numpy_demo_typemaps(short             )
%apply_numpy_demo_typemaps(unsigned short    )
%apply_numpy_demo_typemaps(int               )
%apply_numpy_demo_typemaps(unsigned int      )
%apply_numpy_demo_typemaps(long              )
%apply_numpy_demo_typemaps(unsigned long     )
%apply_numpy_demo_typemaps(long long         )
%apply_numpy_demo_typemaps(unsigned long long)
%apply_numpy_demo_typemaps(float             )
%apply_numpy_demo_typemaps(double            )

// Include the header file to be wrapped
%include "Fortran.h"
