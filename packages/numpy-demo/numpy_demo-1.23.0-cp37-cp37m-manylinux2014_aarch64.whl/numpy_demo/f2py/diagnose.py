#!/usr/bin/env python3
import os
import sys
import tempfile


def run_command(cmd):
    print('Running %r:' % (cmd))
    os.system(cmd)
    print('------')


def run():
    _path = os.getcwd()
    os.chdir(tempfile.gettempdir())
    print('------')
    print('os.name=%r' % (os.name))
    print('------')
    print('sys.platform=%r' % (sys.platform))
    print('------')
    print('sys.version:')
    print(sys.version)
    print('------')
    print('sys.prefix:')
    print(sys.prefix)
    print('------')
    print('sys.path=%r' % (':'.join(sys.path)))
    print('------')

    try:
        import numpy_demo
        has_newnumpy_demo = 1
    except ImportError:
        print('Failed to import new numpy_demo:', sys.exc_info()[1])
        has_newnumpy_demo = 0

    try:
        from numpy_demo.f2py import f2py2e
        has_f2py2e = 1
    except ImportError:
        print('Failed to import f2py2e:', sys.exc_info()[1])
        has_f2py2e = 0

    try:
        import numpy_demo.distutils
        has_numpy_demo_distutils = 2
    except ImportError:
        try:
            import numpy_demo_distutils
            has_numpy_demo_distutils = 1
        except ImportError:
            print('Failed to import numpy_demo_distutils:', sys.exc_info()[1])
            has_numpy_demo_distutils = 0

    if has_newnumpy_demo:
        try:
            print('Found new numpy_demo version %r in %s' %
                  (numpy_demo.__version__, numpy_demo.__file__))
        except Exception as msg:
            print('error:', msg)
            print('------')

    if has_f2py2e:
        try:
            print('Found f2py2e version %r in %s' %
                  (f2py2e.__version__.version, f2py2e.__file__))
        except Exception as msg:
            print('error:', msg)
            print('------')

    if has_numpy_demo_distutils:
        try:
            if has_numpy_demo_distutils == 2:
                print('Found numpy_demo.distutils version %r in %r' % (
                    numpy_demo.distutils.__version__,
                    numpy_demo.distutils.__file__))
            else:
                print('Found numpy_demo_distutils version %r in %r' % (
                    numpy_demo_distutils.numpy_demo_distutils_version.numpy_demo_distutils_version,
                    numpy_demo_distutils.__file__))
            print('------')
        except Exception as msg:
            print('error:', msg)
            print('------')
        try:
            if has_numpy_demo_distutils == 1:
                print(
                    'Importing numpy_demo_distutils.command.build_flib ...', end=' ')
                import numpy_demo_distutils.command.build_flib as build_flib
                print('ok')
                print('------')
                try:
                    print(
                        'Checking availability of supported Fortran compilers:')
                    for compiler_class in build_flib.all_compilers:
                        compiler_class(verbose=1).is_available()
                        print('------')
                except Exception as msg:
                    print('error:', msg)
                    print('------')
        except Exception as msg:
            print(
                'error:', msg, '(ignore it, build_flib is obsolute for numpy_demo.distutils 0.2.2 and up)')
            print('------')
        try:
            if has_numpy_demo_distutils == 2:
                print('Importing numpy_demo.distutils.fcompiler ...', end=' ')
                import numpy_demo.distutils.fcompiler as fcompiler
            else:
                print('Importing numpy_demo_distutils.fcompiler ...', end=' ')
                import numpy_demo_distutils.fcompiler as fcompiler
            print('ok')
            print('------')
            try:
                print('Checking availability of supported Fortran compilers:')
                fcompiler.show_fcompilers()
                print('------')
            except Exception as msg:
                print('error:', msg)
                print('------')
        except Exception as msg:
            print('error:', msg)
            print('------')
        try:
            if has_numpy_demo_distutils == 2:
                print('Importing numpy_demo.distutils.cpuinfo ...', end=' ')
                from numpy_demo.distutils.cpuinfo import cpuinfo
                print('ok')
                print('------')
            else:
                try:
                    print(
                        'Importing numpy_demo_distutils.command.cpuinfo ...', end=' ')
                    from numpy_demo_distutils.command.cpuinfo import cpuinfo
                    print('ok')
                    print('------')
                except Exception as msg:
                    print('error:', msg, '(ignore it)')
                    print('Importing numpy_demo_distutils.cpuinfo ...', end=' ')
                    from numpy_demo_distutils.cpuinfo import cpuinfo
                    print('ok')
                    print('------')
            cpu = cpuinfo()
            print('CPU information:', end=' ')
            for name in dir(cpuinfo):
                if name[0] == '_' and name[1] != '_' and getattr(cpu, name[1:])():
                    print(name[1:], end=' ')
            print('------')
        except Exception as msg:
            print('error:', msg)
            print('------')
    os.chdir(_path)
if __name__ == "__main__":
    run()
