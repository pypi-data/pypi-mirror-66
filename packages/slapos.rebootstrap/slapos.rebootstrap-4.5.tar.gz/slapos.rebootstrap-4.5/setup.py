from setuptools import setup, find_packages
version = '4.5'
name = "slapos.rebootstrap"

long_description = open("README.rst").read() + '\n\n'
long_description += open("CHANGELOG.rst").read()

extras_require = {
    'test': [
        'zope.testing',
        'manuel',
    ]
}

setup(
  name=name,
  version=version,
  description="A zc.buildout extension to solve chicken-and-egg problem of"\
      " using python which is built by itself",
  long_description=long_description,
  classifiers=[
      "Development Status :: 4 - Beta",
      "Framework :: Buildout :: Extension",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: Zope Public License",
      "Programming Language :: Python",
      "Topic :: Software Development :: Build Tools",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ],
  entry_points={
     'zc.buildout.extension': ['extension = %s:extension' % name],
     },
  url='https://lab.nexedi.com/nexedi/slapos.rebootstrap',
  maintainer='Kazuhiko Shiozaki',
  maintainer_email='kazuhiko@nexedi.com',
  license='ZPL 2.1',
  include_package_data=True,
  namespace_packages=['slapos'],
  packages=find_packages(),
  zip_safe=True,
  dependency_links=[
    'http://www.nexedi.org/static/packages/source/slapos.buildout/',
    ],
  install_requires=[
    'setuptools',
    'zc.buildout >=2.7.1+slapos001, <2.7.2',
    ],
  extras_require=extras_require,
  tests_require=extras_require['test'],
  test_suite='%s.tests.test_suite' % name,
)
