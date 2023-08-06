from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy_demo

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("alloc_hook", ["alloc_hook.pyx"],
                             include_dirs=[numpy_demo.get_include()])])
