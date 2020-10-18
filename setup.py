# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup
from setuptools.command.build_py import build_py

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
versionfile = open(os.path.join(here, "baseframe", "_version.py")).read()

mo = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", versionfile, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in baseframe/_version.py.")

requires = [
    'bleach',
    'coaster',
    'cssmin',
    'dnspython',
    'emoji',
    'Flask-Assets',
    'Flask-Babelhg',
    'Flask-Caching',
    'Flask-WTF>=0.14',
    'Flask>=1.0',
    'furl',
    'html5lib>=1.0.1',
    'mxsniff',
    'ndg-httpsclient',
    'pyasn1',
    'pycountry',
    'pyIsEmail',
    'pyOpenSSL',
    'pytz',
    'redis',
    'requests',
    'rq',
    'semantic_version',
    'sentry-sdk',
    'six>=1.13.0',
    'speaklater',
    'statsd',
    'werkzeug',
    'WTForms>=2.2',
]


class BaseframeBuildPy(build_py):
    def run(self):
        result = build_py.run(self)
        if not self._dry_run:
            curdir = os.getcwd()
            os.chdir(os.path.join(self.build_lib, 'baseframe'))
            os.system("make")
            os.chdir(curdir)
        return result


setup(
    name='baseframe',
    version=version,
    description='Baseframe for Hasgeek projects',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
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
        "https://github.com/hasgeek/flask-babelhg/archive/master.zip#egg=Flask-Babelhg-0.12.3",
    ],
)
