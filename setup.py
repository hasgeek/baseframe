"""Setup Baseframe."""

import os
import re

from setuptools import setup
from setuptools.command.build_py import build_py

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as fd:
    README = fd.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as fd:
    CHANGES = fd.read()
with open(os.path.join(here, "baseframe", "_version.py"), encoding='utf-8') as fd:
    versionfile = fd.read()

mo = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", versionfile, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in baseframe/_version.py")

requires = [
    'bleach',
    'coaster',
    'cssmin',
    'dnspython',
    'emoji>=1.0.0',
    'Flask-Assets',
    'Flask-Babel>=2.0.0',
    'Flask-Caching',
    'Flask-WTF>=0.14',
    'Flask>=2.0',
    'furl',
    'grapheme>=0.6.0',
    'html5lib>=1.0.1',
    'markupsafe',
    'mxsniff',
    'ndg-httpsclient',
    'pyasn1',
    'pycountry',
    'pyIsEmail',
    'pyOpenSSL',
    'python-dateutil',
    'pytz',
    'redis',
    'requests-mock>=1.9.3',
    'requests',
    'rq',
    'semantic_version',
    'sentry-sdk',
    'statsd',
    'typing_extensions',
    'werkzeug',
    'WTForms-SQLAlchemy',
    'WTForms>=3.0',
]


class BaseframeBuildPy(build_py):
    def run(self):
        build_py.run(self)
        if not self._dry_run:
            curdir = os.getcwd()
            os.chdir(os.path.join(self.build_lib, 'baseframe'))
            os.system('make')  # nosec
            os.chdir(curdir)


setup(
    name='baseframe',
    version=version,
    description='Baseframe for Hasgeek projects',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries",
    ],
    author='Kiran Jonnalagadda',
    author_email='kiran@hasgeek.com',
    url='https://github.com/hasgeek/baseframe',
    keywords='baseframe',
    packages=['baseframe'],
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    install_requires=requires,
    tests_require=['Flask-SQLAlchemy'],
    cmdclass={'build_py': BaseframeBuildPy},
    dependency_links=[
        "https://github.com/hasgeek/coaster/archive/master.zip#egg=coaster",
    ],
)
