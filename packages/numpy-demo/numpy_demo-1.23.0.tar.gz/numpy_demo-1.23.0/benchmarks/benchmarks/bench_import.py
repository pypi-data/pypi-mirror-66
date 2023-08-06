from subprocess import call
from sys import executable
from timeit import default_timer

from .common import Benchmark


class Import(Benchmark):
    timer = default_timer

    def execute(self, command):
        call((executable, '-c', command))

    def time_numpy_demo(self):
        self.execute('import numpy_demo')

    def time_numpy_demo_inspect(self):
        # What are the savings from avoiding to import the inspect module?
        self.execute('import numpy_demo, inspect')

    def time_fft(self):
        self.execute('from numpy_demo import fft')

    def time_linalg(self):
        self.execute('from numpy_demo import linalg')

    def time_ma(self):
        self.execute('from numpy_demo import ma')

    def time_matlib(self):
        self.execute('from numpy_demo import matlib')

    def time_random(self):
        self.execute('from numpy_demo import random')
