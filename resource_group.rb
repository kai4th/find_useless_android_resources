require 'set'

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
