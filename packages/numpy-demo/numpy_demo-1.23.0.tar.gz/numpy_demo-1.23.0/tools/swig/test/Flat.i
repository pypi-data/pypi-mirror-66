// -*- c++ -*-
%module Flat

%{
#define SWIG_FILE_WITH_INIT
#include "Flat.h"
%}

// Get the NumPy typemaps
%include "../numpy_demo.i"

%init %{
  import_array();
%}

%define %apply_numpy_demo_typemaps(TYPE)

%apply (TYPE* INPLACE_ARRAY_FLAT, int DIM_FLAT) {(TYPE* array, int size)};

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
%include "Flat.h"
