import os

class AndroidFile(object):
	JAVA = "java"
	XML = "xml"
	PNG = "png"

	def __init__(self, path, file_name):
		self.path = path
		self.file_name = file_name

	def get_full_path(self):
		return os.path.join(self.path, self.file_name)


class AndroidResource(AndroidFile):
	DRAWABLE = "drawable"
	LAYOUT = "layout"
	ANIM = "anim"
	COLOR = "color"
	MENU = "menu"
	VALUES = "values"

	def __init__(self, android_file, res_type):
		AndroidFile.__init__(self, android_file.path, android_file.file_name)
		self.init(res_type)

	def init(self, res_type):
		self.type = res_type
		self.folder_type = self.path.split("/")[-1].split("-")[0]
		self.resource_name = self.file_name.split(".")[0]
		self.used = False

	def set_used(self, used = True):
		self.used = used

class ResourceGroup(object):
	def __init__(self):
		self.resources = {}
		self.used_resources = set()
	def __repr__(self):
		ret_dict = {}
		for key in self.resources:
			ret_dict[key] = len(self.resources[key])
		return str(ret_dict)
	
	def insert(self, resource):
		if resource.type not in self.resources.keys():
			self.resources[resource.type] = []

		self.resources[resource.type].append(resource)

	def set_used(self, resource_type, resource_name):
		used_resource = (resource_type, resource_name);
		if used_resource not in self.used_resources:
			self.used_resources.add(used_resource)
			if resource_type in self.resources.keys():
				for resource in self.resources[resource_type]:
					if resource.resource_name == resource_name:
						resource.set_used()

	def get_contain_types(self):
		return self.resources.keys()

	def get_resources(self, resource_type):
		if resource_type not in self.resources.keys():
			return []
		return self.resources[resource_type]

	def size(self):
		return len(self.resources)

	def size(self, resource_type):
		return len(self.resources[resource_type])

