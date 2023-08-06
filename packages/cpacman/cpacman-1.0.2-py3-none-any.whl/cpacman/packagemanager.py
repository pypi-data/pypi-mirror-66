import os
import requests
import pathlib
from urllib.parse import urlparse
from typing import Generator, List
from cpacman.package import Package

class PackageManager():
	def __init__(self, clean_files:bool = False, *args, **kwargs) -> None:
		self.clean_files:bool = clean_files

	def __parse_requirements_line__(self, line:str, requirements_file:pathlib.Path) -> dict:
		# result is a dict of arguments
		# which will be givent to create new Package object
		result:dict = dict()

		# Splitting line into two parts
		# left part is a path where we will store a pacage
		# Right part sets url for downloading package
		#   author/packagename
		#   https://github.com/author/packagename
		#   https://github.com/author/packagename.git
		#   git@github.com:author/packagename.git
		#   git@github.com:author/packagename
		line:List[str] = line.split('>')

		if len(line) == 2:
			short_packagepath, link = line

			# Here we take info from a link
			# keys are:
			#   author       - author of the package
			#   projecktlink - link to github repo
			#   loadlink     - link to download repo in zip
			#   projecktname - name of the package
			link:dict = self.__parse_link__(link)
			reqfile_directory:pathlib.Path = pathlib.Path(requirements_file.resolve().parent)
			long_packagepath :pathlib.Path = reqfile_directory.joinpath(short_packagepath)

			# If boths varibles are not empty lines
			if link and long_packagepath:
				result['packagepath'] = long_packagepath
				result['loadlink'   ] = link['loadlink'   ]
				result['projectlink'] = link['projectlink']
				result['projectname'] = link['projectname']
		return result

	def __parse_link__(self, link:str) -> dict:
		# Here we take info from a link
		# keys are:
		#   author       - author of the package
		#   projecktlink - link to github repo
		#   loadlink     - link to download repo in zip
		#   projecktname - name of the package
		result:dict = dict()

		if link:
			url_path:str   = urlparse(link).path
			info:List[str] = url_path.split('/')

			# Left part is an author
			# Right part is project name
			if len(info) == 2:

				# Strip author and project
				info = list(map(lambda x: x.strip(), info))
				
				author, project = info

				if author and project:

					result['projectlink'] = f'https://github.com/{author}/{project}.git'
					result['loadlink'   ] = f'https://github.com/{author}/{project}/archive/master.zip'
					result['projectname'] = project
					result['author'     ] = author

		return result

	def read_requirements_file(self, requirements_file:pathlib.Path) -> Generator[Package, None, None]:
		with open(requirements_file, encoding="utf-8") as opened_requirements_file:
			for line in opened_requirements_file:
				info:Dict = self.__parse_requirements_line__(line, requirements_file)
				if info:
					yield Package(**info)
				else:
					print(f"Line was ignored due to incorrect schema!")
					print(f"    {line}")

	def load_packages_from_requirements_file(self, requirements_file:pathlib.Path):
		requirements_file:pathlib.Path = pathlib.Path(requirements_file)
		for package in self.read_requirements_file(requirements_file):
			package.load()
			package.unpack()
			if self.clean_files:
				package.clean()

	def install(self, line) -> None:
		info:dict = self.__parse_requirements_line__(line)
		if info:
			package:Package = Package(**info)
			package.load()
			package.unpack()
			if self.clean_files:
				package.clean()
		else:
			print(f"Line was ignored due to incorrect schema!")
			print(f"    {line}")

	def find_requirements_files(self):
		for filename in pathlib.Path.cwd().rglob("**/*"):
			if filename.is_file() and filename.suffix == '.cpacman':
				yield filename

	def recursive_install(self):
		for req_file in self.find_requirements_files():
			self.load_packages_from_requirements_file(req_file)
			
