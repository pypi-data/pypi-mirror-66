def main():

	from cpacman.packagemanager import PackageManager
	from argparse import ArgumentParser

	parser = ArgumentParser()

	parser.add_argument('-i' , '--install'           , type = str)
	parser.add_argument('-r' , '--requirements'      , type = str)
	parser.add_argument('-c' , '--clean'             , action = 'store_true', default = False)
	parser.add_argument('-ri', '--recursive_install' , action = 'store_true', default = False)
	args = parser.parse_args()

	manager = PackageManager(clean_files = args.clean)

	if args.requirements:
		manager.load_packages_from_requirements_file(args.requirements)

	elif args.install:
		manager.install(args.install)

	elif args.recursive_install:
		manager.recursive_install()

if __name__ == '__main__':
	main()