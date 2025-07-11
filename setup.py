"""Setup Baseframe."""

import os

from setuptools import setup
from setuptools.command.build_py import build_py


# This is invoked from ``pyproject.toml``
class BaseframeBuildPy(build_py):
    def run(self) -> None:
        build_py.run(self)
        if not self._dry_run:
            curdir = os.getcwd()
            os.chdir(os.path.join(self.build_lib, 'baseframe'))
            os.system('make')  # nosec B605 B607  # noqa: S605,S607
            os.chdir(curdir)


setup(cmdclass={'build_py': BaseframeBuildPy})
