import numpy_demo as np
import numpy_demo.matlib
from numpy_demo.testing import assert_array_equal, assert_

def test_empty():
    x = numpy_demo.matlib.empty((2,))
    assert_(isinstance(x, np.matrix))
    assert_(x.shape, (1, 2))

def test_ones():
    assert_array_equal(numpy_demo.matlib.ones((2, 3)),
                       np.matrix([[ 1.,  1.,  1.],
                                 [ 1.,  1.,  1.]]))

    assert_array_equal(numpy_demo.matlib.ones(2), np.matrix([[ 1.,  1.]]))

def test_zeros():
    assert_array_equal(numpy_demo.matlib.zeros((2, 3)),
                       np.matrix([[ 0.,  0.,  0.],
                                 [ 0.,  0.,  0.]]))

    assert_array_equal(numpy_demo.matlib.zeros(2), np.matrix([[ 0.,  0.]]))

def test_identity():
    x = numpy_demo.matlib.identity(2, dtype=int)
    assert_array_equal(x, np.matrix([[1, 0], [0, 1]]))

def test_eye():
    xc = numpy_demo.matlib.eye(3, k=1, dtype=int)
    assert_array_equal(xc, np.matrix([[ 0,  1,  0],
                                      [ 0,  0,  1],
                                      [ 0,  0,  0]]))
    assert xc.flags.c_contiguous
    assert not xc.flags.f_contiguous

    xf = numpy_demo.matlib.eye(3, 4, dtype=int, order='F')
    assert_array_equal(xf, np.matrix([[ 1,  0,  0,  0],
                                      [ 0,  1,  0,  0],
                                      [ 0,  0,  1,  0]]))
    assert not xf.flags.c_contiguous
    assert xf.flags.f_contiguous

def test_rand():
    x = numpy_demo.matlib.rand(3)
    # check matrix type, array would have shape (3,)
    assert_(x.ndim == 2)

def test_randn():
    x = np.matlib.randn(3)
    # check matrix type, array would have shape (3,)
    assert_(x.ndim == 2)

def test_repmat():
    a1 = np.arange(4)
    x = numpy_demo.matlib.repmat(a1, 2, 2)
    y = np.array([[0, 1, 2, 3, 0, 1, 2, 3],
                  [0, 1, 2, 3, 0, 1, 2, 3]])
    assert_array_equal(x, y)
