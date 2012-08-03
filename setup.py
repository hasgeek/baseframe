import os
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

here = os.path.abspath(os.path.dirname(__file__))
README = unicode(open(os.path.join(here, 'README.rst')).read(), 'utf-8')
CHANGES = unicode(open(os.path.join(here, 'CHANGES.rst')).read(), 'utf-8')

requires = [
    'Flask',
    'coaster',
    'jsmin',
    'cssmin',
    'Flask-Assets',
    'Flask-WTF',
    'wtforms',
    'bleach',
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
      version='0.2.11',
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
      author_email='kiran@hasgeek.in',
      url='http://github.com/hasgeek/baseframe',
      keywords='baseframe',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='tests',
      install_requires=requires,
      cmdclass={'build_py': BaseframeBuildPy},
      dependency_links=[
          "https://github.com/hasgeek/coaster/tarball/master#egg=coaster",
          ]
      )
