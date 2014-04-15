import re
import os

from resource_file import AndroidFile
from resource_file import ResourceGroup
from resource_file import AndroidResource

class ResourceFinder(object):
	REGEX_PACKAGE_IN_MANIFEST = "\Wpackage\W+\""

	def __get_manifest_path(project_path):
		if project_path.endswith("/"):
			return project_path + "AndroidManifest.xml"
		else:
			return project_path + "/AndroidManifest.xml"

	def __get_package_in_manifest(manifest_file):
		with open(manifest_file.get_full_path()) as manifest:
			for line in manifest:
				if bool(re.search(ResourceFinder.REGEX_PACKAGE_IN_MANIFEST, line)):
					package = line.split("=")[1].replace("\"", "").strip()
					if input("is [ " + package + " ] correct package? (Y/n) : ") is not "n":
						return package

		return input("input correct package name : ")


	def __init__(self, project_path):
		self.__project_path = project_path
		self.files = {}
		self.exist_resources = ResourceGroup()

	def find_base_env(self):
		self.__manifest = AndroidFile(self.__project_path, "AndroidManifest.xml")
		self.__package = ResourceFinder.__get_package_in_manifest(self.__manifest)

	def find_files(self):
		self.files[AndroidFile.JAVA] = self.__find_files_in("src", AndroidFile.JAVA)
		self.files[AndroidFile.XML] = self.__find_files_in("res", AndroidFile.XML)
		self.files[AndroidFile.PNG] = self.__find_files_in("res", AndroidFile.PNG)

	def find_exist_resources(self):
		for png_file in self.files[AndroidFile.PNG]:
			self.exist_resources.insert(AndroidResource(png_file, AndroidResource.DRAWABLE))

		for xml_file in self.files[AndroidFile.XML]:
			folder_type = xml_file.path.split("/")[-1].split("-")[0]
			if folder_type != AndroidResource.VALUES:
				resource_file = AndroidResource(xml_file, folder_type)
				self.exist_resources.insert(resource_file)

		# print(self.exist_resources)

	def find_used_resources(self):

		for java in self.files[AndroidFile.JAVA]:
			self.__find_resources_in_java(java)
		for xml in self.files[AndroidFile.XML]:
			self.__find_resource_in_xml(xml)

		self.__find_resource_in_xml(self.__manifest)

	def print_unused_resources(self):
		for res_type in self.exist_resources.get_contain_types():
			resources = self.exist_resources.get_resources(res_type)
			unused_resource_names = set()
			for resource in resources:
				if resource.used == False:
					unused_resource_names.add(resource.resource_name)

			if (len(unused_resource_names) > 0):
				print("\n=== ", res_type, "(", len(unused_resource_names), "/", len(resources), ") ===")
				for name in unused_resource_names:
					print(name)

	def delete_unused_resources(self, force = False):

		for res_type in self.exist_resources.get_contain_types():
			resources = self.exist_resources.get_resources(res_type)
			unused_resources = []
			for resource in resources:
				if resource.used == False:
					unused_resources.append(resource)
			if len(unused_resources) > 0:
				if force:
					for resource in unused_resources:
						os.remove(resource.get_full_path())
				else:
					for resource in unused_resources:
						print("\n\n=== ", res_type, "/", resource.resource_name, " ===")
						print(resource.get_full_path())
						# input_str = resource.resource_name + " ( " + resource.get_full_path() + " ) | delete ? (y/N)"
						if input("delete ? (y/N) : ") == "y":
							os.remove(resource.get_full_path())

		

	def __find_resources_in_java(self, java_file):
		with open(java_file.get_full_path()) as f:
			search_re = ""
			import_string = "import " + self.__package
			for line in f:
				if import_string in line:
					search_re = '\WR\.'
					break
			else:
				search_re = "\W" + self.__package.replace(".", "\.")

			f.seek(0,0)

			for line in f:
				if bool(re.search(search_re, line)):
					for resource in re.findall('\WR\.\w*\.\w*', line):
						if """//""" in line:
							comment_index = line.index("""//""")
							resource_index = line.index(resource)
							if comment_index < resource_index:
								continue
						tokens = resource.split(".")
						resource_type = tokens[-2]
						resource_name = tokens[-1]
						self.exist_resources.set_used(resource_type, resource_name)

	def __find_resource_in_xml(self, xml_file):
		with open(xml_file.get_full_path()) as f:
			for line in f:
				if bool(re.search('\@\w*\/\w*', line)):
					resources = []
					for resource in re.findall('\@\w*\/\w*', line):
						tokens = resource.split("/")
						resource_type = tokens[-2][1:]
						resource_name = tokens[-1]
						self.exist_resources.set_used(resource_type, resource_name)


	def __find_files_in(self, path, ext):
		ret_list = []
		for root, dirs, names in os.walk(os.path.join(self.__project_path, path)):
			for name in names:
				if os.path.splitext(name)[-1].lower() == "." + ext:
					ret_list.append(AndroidFile(root, name))
		return ret_list



