from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='asterism',
      version='0.5.2',
      description='Helpers for Project Electron infrastructure',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/RockefellerArchiveCenter/asterism',
      author='Rockefeller Archive Center',
      author_email='archive@rockarch.org',
      install_requires=[
          'bagit',
          'django',
          'djangorestframework',
          'psycopg2-binary',
          'odin'],
      license='MIT',
      packages=['asterism', 'asterism.resources'],
      test_suite='nose.collector',
      tests_require=[
          'nose',
          'bagit',
          'django',
          'djangorestframework',
          'psycopg2-binary'],
      zip_safe=False)
