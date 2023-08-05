from setuptools import setup
setup(
	name='sparsebinarydistance',
	version='0.01',
	author='Buys de Barbanson',
	author_email='code@buysdb.nl',
	description='Calculate a distance matrix based on a binary feature matrix with missing data ',
	url='https://github.com/BuysDB/SparseBinaryDistance',
	packages=['sparsebinarydistance'],
	install_requires=['pandas','numpy']
)
