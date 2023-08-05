from distutils.core import setup

#Upload Library
#    Install it via pip install twine
#    Make sure your .pypirc file has the correct credentials for test.pypi.org because that is a separate database from production pypi.
#    Build your sdist python3 setup.py sdist
#    Use twine upload --repository pypitest dist/* for your test upload.
#    Use twine upload --repository pypi dist/* for your production upload.

setup(
  name = 'libcorepy',
  packages = ['utility'], 
  license='MIT',
  version = '0.0.2',
  description = 'Library based on the gocore libcore library',
  author = 'Rafael Antonio Hidalgo',
  author_email = 'rafael180496@gmail.com',
  url = 'https://github.com/rafael180496/LIBCOREPY', # use the URL to the github repo
  download_url = 'https://github.com/rafael180496/LIBCOREPY/tarball/v0.0.1',
  keywords = 'test example develop',
  classifiers = ['Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7']
)