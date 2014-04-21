require 'set'

class AndroidFile
	JAVA = "java"
	XML = "xml"
	PNG = "png"

	attr_accessor :path, :file_name

	def initialize(path, file_name)
		@path = path
		@file_name = file_name
	end


	def get_full_path()
		return File.join(@path, @file_name)
	end
end

class AndroidResource < AndroidFile
	DRAWABLE = "drawable"
	LAYOUT = "layout"
	ANIM = "anim"
	COLOR = "color"
	MENU = "menu"
	VALUES = "values"

	attr_accessor :resource_name, :used, :type

	def initialize(android_file, res_type)
		super(android_file.path, android_file.file_name)
		init(res_type)
	end

	def init(res_type)
		@type = res_type
		@folder_type = @path.split("/")[-1].split("-")[0]
		@resource_name = @file_name.split(".")[0]
		@used = false
	end

end

class ResourceGroup
	attr_accessor :resources

	def initialize()
		@resources = Hash.new
		@used_resources = Set.new
	end

	def insert(resource)
		if @resources.has_key?(resource.type) == false
			@resources[resource.type] = Array.new
		end
		@resources[resource.type].push(resource)
	end

	def set_used(resource_type, resource_name)
		if @resources.has_key?(resource_type)
			for resource in @resources[resource_type]
				if resource.resource_name == resource_name
					resource.used = true
				end
			end
		end
	end

	def get_contain_types()
		return @resources.keys()
	end

	def get_resources(resource_type)
		if @resources.has_key?(resource_type)
			return @resources[resource_type]
		else
			return Array.new
		end
	end

	def size()
		return @resources.length
	end

	def size(resource_type)
		if @resources.has_key?(resource_type)
			return @resources[resource_type].length
		else 
			return 0
		end
	end
end

class ResourceFinder
	# REGEX_PACKAGE_IN_MANIFEST = "\Wpackage\W+\""
	ANDROID_MANIFEST ="AndroidManifest.xml"

	def get_manifest_path()
		return File.join(@project_path, ANDROID_MANIFEST)
	end

	def get_package_in_manifest()
		#TODO find with regex
		return "com.vingle.android"
	end

	def initialize(project_path)
		@project_path = project_path
		@files = Hash.new
		@resources = ResourceGroup.new

		Dir.chdir(@project_path)
	end

	def find_base_env()
		@manifest = AndroidFile.new(@project_path, ANDROID_MANIFEST)
		@package = get_package_in_manifest()
	end

	def find_files_in(path, ext)
		file_filter = File.join(path, "**", "*.#{ext}")
		file_list = Array.new
		Dir.glob(file_filter) do |file|
			android_file = AndroidFile.new(File.dirname(file), File.basename(file))
			file_list.push(android_file)
		end
		return file_list
	end

	def find_files()
		@files[AndroidFile::JAVA] = find_files_in("src", AndroidFile::JAVA)
		@files[AndroidFile::XML] = find_files_in("res", AndroidFile::XML)
		@files[AndroidFile::PNG] = find_files_in("res", AndroidFile::PNG)
	end

	def find_exist_resources()
		@files[AndroidFile::PNG].each do |png_file|
			@resources.insert(AndroidResource.new(png_file, AndroidResource::DRAWABLE))
		end

		@files[AndroidFile::XML].each do |xml_file|
			type = xml_file.path.split("/")[-1].split("-")[0]
			unless type == AndroidResource::VALUES
				@resources.insert(AndroidResource.new(xml_file, type))
			end
		end
	end

	def find_used_resources()
		@files[AndroidFile::JAVA].each do |java_file|
			find_resources_in_java(java_file)
		end

		@files[AndroidFile::XML].each do |xml_file|
			find_resources_in_xml(xml_file)
		end
		find_resources_in_xml(@manifest)
	end

	def find_resources_in_java(java_file)
		regex_code = /#{@package}\.R\.\w+\.\w+/
		regex_find_code = /\W+#{regex_code}/
		regex_import = /import\W+#{@package}\.R/

		file = File.open(java_file.get_full_path)

		# find import R 
		file.each do |line|
			if line =~ regex_import
				regex_code = /R\.\w+\.\w+/
				regex_find_code = /\W+#{regex_code}/
				break
			end
		end

		file.rewind

		#find resource
		file.each do |line|
			if line =~ regex_find_code
				line.scan(regex_code).each do |resource_code|
					tokens = resource_code.split(".")
					resource_type = tokens[-2]
					resource_name = tokens[-1]
					@resources.set_used(resource_type, resource_name)
				end
			end
		end
	end

	def find_resources_in_xml(xml_file)
		regex_code = /\@\w+\/\w+/

		File.open(xml_file.get_full_path).each do |line|
			if line =~ regex_code
				line.scan(regex_code).each do |resource_code|
					tokens = resource_code.split("/")
					resource_type = tokens[-2][1..-1]
					resource_name = tokens[-1]
					@resources.set_used(resource_type, resource_name)
				end
			end
		end
	end

	def print_unused_resources()
		@resources.resources.each do |type, resources|
			unused_items = Set.new
			resources.each do |resource|
				if resource.used == false
					unused_items.add(resource.resource_name)
				end
			end
			if unused_items.length > 0
				unused_items.each do |name|
					puts name
				end
			end
		end
	end
end






finder = ResourceFinder.new("/Users/kai/vingle/vingle-android")
puts finder.get_manifest_path

finder.find_base_env
finder.find_files
finder.find_exist_resources
finder.find_used_resources
finder.print_unused_resources