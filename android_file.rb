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