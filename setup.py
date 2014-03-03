import os
import re
from setuptools import setup
from setuptools.command.build_py import build_py

here = os.path.abspath(os.path.dirname(__file__))
README = unicode(open(os.path.join(here, 'README.rst')).read(), 'utf-8')
CHANGES = unicode(open(os.path.join(here, 'CHANGES.rst')).read(), 'utf-8')
versionfile = open(os.path.join(here, "baseframe", "_version.py")).read()

mo = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", versionfile, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in baseframe/_version.py.")

requires = [
    'semantic_version',
    'bleach',
    'pytz',
    'requests',
    'dnspython',
    'wtforms',
    'Flask',
    'Flask-Assets',
    'Flask-WTF',
    'Flask-Cache',
    'Flask-BabelEx',
    'Flask-MustacheJS',
    'closure>=20121212',
    'cssmin',
    'coaster',
    'lxml',
    'erequests'
    ]


class BaseframeBuildPy(build_py):
    def run(self):
        result = build_py.run(self)
        if not self._dry_run:
            curdir = os.getcwd()
            os.chdir(os.path.join(self.build_lib, 'baseframe'))
            os.system("make tinymce")
            os.chdir(curdir)
        return result


setup(name='baseframe',
    version=version,
    description='Baseframe for HasGeek projects',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
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
        "https://github.com/hasgeek/coaster/archive/master.zip#egg=coaster-dev",
        "https://github.com/mrjoes/flask-babelex/archive/master.zip#egg=Flask-BabelEx-0.8.2",
        "https://github.com/iamsudip/erequests/archive/master.zip#egg=erequests-dev"
        ]
    )
