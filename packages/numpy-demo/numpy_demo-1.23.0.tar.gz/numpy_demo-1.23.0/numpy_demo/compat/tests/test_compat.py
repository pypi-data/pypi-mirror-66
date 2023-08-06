from os.path import join

from numpy_demo.compat import isfileobj
from numpy_demo.testing import assert_
from numpy_demo.testing import tempdir


def test_isfileobj():
    with tempdir(prefix="numpy_demo_test_compat_") as folder:
        filename = join(folder, 'a.bin')

        with open(filename, 'wb') as f:
            assert_(isfileobj(f))

        with open(filename, 'ab') as f:
            assert_(isfileobj(f))

        with open(filename, 'rb') as f:
            assert_(isfileobj(f))
