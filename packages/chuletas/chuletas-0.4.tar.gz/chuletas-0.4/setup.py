from distutils.core import setup
setup(
  name = 'chuletas',
  packages = ['chuletas'], # this must be the same as the name above
  version = '0.4',
  description = 'command info',
  author = 'waltermas-gitter',
  author_email = 'waltermas@hotmail.com',
  url = 'https://github.com/waltermas-gitter/chuletas}', # use the URL to the github repo
  download_url = 'https://github.com/waltermas-gitter/chuletas/tarball/0.4',
  keywords = ['testing', 'logging', 'example'],
  classifiers = [],
  install_requires=['requests', 'bs4'],
  scripts=['bin/chuletas', 'bin/nanodrive', 'bin/filedrive']
)
