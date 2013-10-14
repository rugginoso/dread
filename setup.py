"""
DREAD
=====

DREAD is a web microframework based on Werkzeug explicitely
wrote to implement REST services.
It support high level resources actions definition and nested resources.
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def dependencies():
    try:
        with open('requirements.txt', 'rt') as reqs:
            return reqs.read().splitlines()
    except IOError:
        return []


setup(name='dread',
      version='0.2.0',
      description='REST microframework',
      long_description=__doc__,
      platforms = 'any',
      license = 'BSD',
      author = 'Lorenzo Masini',
      author_email = 'rugginoso@develer.com',
      url='https://github.com/rugginoso/dread/',
      packages=[ 'dread' ],
      install_requires=dependencies(),
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      test_suite='tests')
