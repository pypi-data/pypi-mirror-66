from numpy_demo.testing import assert_raises, assert_, assert_equal
from numpy_demo.compat import pickle

from importlib import reload

def test_numpy_demo_reloading():
    # gh-7844. Also check that relevant globals retain their identity.
    import numpy_demo as np
    import numpy_demo._globals

    _NoValue = np._NoValue
    VisibleDeprecationWarning = np.VisibleDeprecationWarning
    ModuleDeprecationWarning = np.ModuleDeprecationWarning

    reload(np)
    assert_(_NoValue is np._NoValue)
    assert_(ModuleDeprecationWarning is np.ModuleDeprecationWarning)
    assert_(VisibleDeprecationWarning is np.VisibleDeprecationWarning)

    assert_raises(RuntimeError, reload, numpy_demo._globals)
    reload(np)
    assert_(_NoValue is np._NoValue)
    assert_(ModuleDeprecationWarning is np.ModuleDeprecationWarning)
    assert_(VisibleDeprecationWarning is np.VisibleDeprecationWarning)

def test_novalue():
    import numpy_demo as np
    for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
        assert_equal(repr(np._NoValue), '<no value>')
        assert_(pickle.loads(pickle.dumps(np._NoValue,
                                          protocol=proto)) is np._NoValue)
