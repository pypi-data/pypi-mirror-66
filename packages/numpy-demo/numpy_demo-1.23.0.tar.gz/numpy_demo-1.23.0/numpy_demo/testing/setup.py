#!/usr/bin/env python3

def configuration(parent_package='',top_path=None):
    from numpy_demo.distutils.misc_util import Configuration
    config = Configuration('testing', parent_package, top_path)

    config.add_subpackage('_private')
    config.add_data_dir('tests')
    return config

if __name__ == '__main__':
    from numpy_demo.distutils.core import setup
    setup(maintainer="NumPy Developers",
          maintainer_email="numpy_demo-dev@numpy_demo.org",
          description="NumPy test module",
          url="https://www.numpy_demo.org",
          license="NumPy License (BSD Style)",
          configuration=configuration,
          )
