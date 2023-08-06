import os
import shutil
import pathlib
import zipfile
import requests
from typing import List, Generator

class Package():
	def __init__(self,	packagepath:str, loadlink:str, projectlink:str, projectname:str, *args , **kwargs) -> None:
		# path to the place where it will be unpacked
		self.packagepath :pathlib.Path = pathlib.Path(packagepath)
		self.loadlink    :str          = loadlink
		self.projectlink :str          = projectlink
		self.zipfile_path:str          = pathlib.Path(str(packagepath).strip() + '.zip')
		self.projectname :str          = projectname
		self.packagepath :str          = self.patch_path(self.packagepath)
		self.is_loaded   :bool         = False
		self.is_unpacked :bool         = False
		self.is_cleaned  :bool         = False
		

	def load(self):
		print(f"Loading package: {self.projectlink}")
		response:requests.Response = requests.get(self.loadlink, stream=True)
		
		if response.status_code == 200:
			
			# Path where user wants to store the package: (self.packagepath)
			#	./path/to/package                                   (1)
			# We create directory:
			#	./path/to                                           (2)
			# Then we load zip file to this directory:    (self.zipfile_path)
			#	./path/to/package.zip                               (3)
			# Then we unpack zip file to this directory and get folder:
			#	./path/to/package-master/....(files of the package) (4)
			# Then we rename:
			#	./path/to/package-master -> ./path/to/package		(5, 6)

			# (2)
			zipparent:pathlib.Path = pathlib.Path(self.zipfile_path.parent)
			zipparent.mkdir(parents=True, exist_ok=True)

			# (3)
			with open(self.zipfile_path, 'wb') as package_zip_file:
				for chunk in response.iter_content(chunk_size=1024):
					if chunk:
						package_zip_file.write(chunk)
			self.is_loaded = True
		else:
			print(f"Server returned bad status code: {response.status_code}")

	def unpack(self):
		if self.is_loaded:
			print(f"Unpacking: {self.zipfile_path}")
			# Move one step back
			outdir = self.packagepath.parent

			# (4)
			# Extract zip
			with zipfile.ZipFile(self.zipfile_path) as zip_ref:
				zip_ref.extractall(outdir)

				# Removing loaded zip file
			self.zipfile_path.unlink()
		
			# (5, 6)
			# Now it is saved in ./path/given/projectname-master
			# We rename to       self.packagepath
			previous_path = outdir.joinpath(f"{self.projectname}-master")
			
			if self.packagepath.exists():
				shutil.rmtree(self.packagepath)

			previous_path.rename(self.packagepath)
			
			self.is_unpacked = True
		else:
			print("Package was not loaded correctly!")
		
			
	def clean(self):
		if self.packagepath.exists() and self.is_loaded and self.is_unpacked:
			print(f"Cleaning directory: {self.unpatch_path(self.packagepath)}")
			extensions = ('.c', '.cpp', '.h', '.hpp', '.cpacman')
			for filename in self.packagepath.rglob('./**/*'):
				if filename.is_file() and not filename.suffix in extensions:
					print(f"	{self.unpatch_path(filename)}")
					filename.unlink()

	#	Sometimes search fails
	#	as system cannot find path
	#	This is a solution from StackOverflow
	#		https://stackoverflow.com/a/57502760
	@staticmethod
	def patch_path(path):
		normalized = os.fspath(path.resolve())
		if not normalized.startswith('\\\\?\\'):
			normalized = '\\\\?\\' + normalized.strip()
		return pathlib.Path(normalized)

	def unpatch_path(self, path):
		normalized = os.fspath(path.resolve())
		if normalized.startswith('\\\\?\\'):
			normalized = normalized.strip('\\\\?\\')
		return pathlib.Path(normalized)