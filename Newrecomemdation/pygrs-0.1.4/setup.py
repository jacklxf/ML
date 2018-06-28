from setuptools import setup

packages = [
		"pygrs"
		]
setup(name='pygrs',
      version='0.1.4',
      description='Python library for GRS project',
      classifiers=['Development Status :: 2 - Pre-Alpha', 'Programming Language :: Python :: 3'],
      author='aft',
      author_email='aft@afution.com',
      url='https://www.python.org',
	  packages=['pygrs'],
	  package_dir={'pygrs': 'grs'},
	  install_requires=['pyspark', 'pandas', 'waitress', 'falcon', 'pymssql', 'cx_Oracle']
     )