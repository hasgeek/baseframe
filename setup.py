"""Setup Baseframe."""

import os

from setuptools import setup
from setuptools.command.build_py import build_py


# This is invoked from ``pyproject.toml``
class BaseframeBuildPy(build_py):
    def run(self):
        build_py.run(self)
        if not self._dry_run:
            curdir = os.getcwd()
            os.chdir(os.path.join(self.build_lib, 'baseframe'))
            os.system('make')  # nosec
            os.chdir(curdir)


setup(cmdclass={'build_py': BaseframeBuildPy})
