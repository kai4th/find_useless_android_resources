#!/usr/bin/env python3.3
import os

from resource_finder import ResourceFinder


os.system("clear")
project_path = input("input project root dir : ")
# project_path = """/Users/kai/vingle/vingle-android"""

finder = ResourceFinder(project_path)

finder.find_base_env()
finder.find_files()
finder.find_exist_resources()
finder.find_used_resources()

finder.print_unused_resources()

input_str = input("delete file right now? (Y/n/all) : ")

os.system("clear")

if input_str == "all":
	finder.delete_unused_resources(True)
elif input_str == "n":
	pass
else:
	finder.delete_unused_resources()