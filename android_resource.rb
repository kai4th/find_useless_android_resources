
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