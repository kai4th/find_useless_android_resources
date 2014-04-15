#!/usr/bin/env python3.3
import sys
import os
import re

from resource_finder import ResourceFinder


project_path = input("input project root dir : ")
# project_path = """/Users/kai/vingle/vingle-android"""

finder = ResourceFinder(project_path)

finder.find_base_env()
finder.find_files()
finder.find_exist_resources()
finder.find_used_resources()

finder.print_unused_resources()