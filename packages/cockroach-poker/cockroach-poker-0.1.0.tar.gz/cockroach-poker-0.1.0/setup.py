from setuptools import setup

setup(
  name='cockroach-poker',
  version='0.1.0',
  description='A fun card game all about bluffing',
  url='https://gitlab.com/oldironhorse/cockroach-poker',
  author='Simon Redding',
  author_email='s1m0n.r3dd1ng@gmail.com',
  packages=['cockroachpoker'],
  install_requires=[
        'pycrypto',
        'paho-mqtt',
        'click'
      ],
  scripts=[
      'bin/cockroach-host',
      'bin/cockroach-player'],
  python_requires='>=3.4, <3.8',
  test_suite='nose.collector',
  tests_require=['nose'],
  zip_safe=False)
