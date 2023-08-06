from setuptools import setup, find_packages

setup(
		name             = 'cpacman',
		version          = '1.0.3',
		packages         = find_packages(),
		author           = 'Miasnenko Dmitry',
		author_email     = 'cl0wzed.exe@gmail.com',
		url              = 'https://github.com/YoungMeatBoy/cpacman.git',
		install_requires = ['requests'],
		entry_points={
			'console_scripts': [
				'cpacman = cpacman.run:main'
		]
		}
)