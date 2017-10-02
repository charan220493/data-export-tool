import argparse
import random
import os
import sys
import shutil
import re
import glob
import string

class gp_file_util:

	def __init__(self):
		self.gpf_file_path = ""
		self.compression_ext = ""

	def set_compression(self,compression_string):
		# try:
		clean_string = compression_string.strip(". ").lower()
		if (clean_string == 'gz'):
			self.compression_ext = "." + clean_string
		else:
			raise ValueError("No support for the compression type: " + str(clean_string))
		# except ValueError as e:
		# 	print("Error is: " + str(e))
		# 	sys.stdout.flush()
		# except Exception as e:
		# 	print("Exception is: " + str(e))
		# 	sys.stdout.flush()

		
	def create_files(self, server, path, num_ports, parts_per_port):
		ret_val = False
		cap_ports = num_ports
		available_ports = [8081,8082,8083,8084,8085,8086,8087,8088]
		path = path.rstrip("/")
		temp_path = str(path) + "/temp"
		self.global_temp_path = temp_path
		try:
			os.mkdir(path)
			os.mkdir(temp_path)
			for i in range(0,cap_ports):
				for j in range(0,parts_per_port):
					part_num = 10000 * (i+1) + j
					file_name = str(temp_path) + "/part-g-" + str(part_num) + self.compression_ext
					open(file_name,"a")
					os.chmod(file_name,0777)
					file_name = str(available_ports[i]) + file_name
					if i == cap_ports-1 and j == parts_per_port-1:
						self.append_gpf_file_path(server, file_name, True)
					else:
						self.append_gpf_file_path(server, file_name, False)
		except Exception as e:
			print("Error occured: " + str(e))
			sys.stdout.flush()
		else:
			ret_val = True
			return ret_val


	def mv_files(self, des_path, flat_file_name, is_flat_file):
		try:
			return_code = False
			part_file_path = self.global_temp_path + "/part*"

			if is_flat_file:
				concat_file_path = self.global_temp_path + "/" + flat_file_name.strip("/")
				with open(concat_file_path, "wb") as wfd:
					os.chmod(concat_file_path, 0777)
					for f in glob.iglob(part_file_path):
						with open(f,"rb") as fd:
							shutil.copyfileobj(fd, wfd, 1024*1024*10)
				shutil.move(concat_file_path, des_path)
			else:
				for temporary_path in glob.iglob(part_file_path):
					shutil.move(temporary_path, des_path)

			shutil.rmtree(self.global_temp_path)

		except IOError as e:
			print("Cannot create flat file: " + str(concat_file_path) + "as this error occured: \n" + str(e))
			sys.stdout.flush()

		except Exception as e:
			print("Something failed while concatenating!!!..... Error is: " + str(e))
			sys.stdout.flush()
		else:
			return_code = True
			return return_code

	def append_gpf_file_path(self, server, path, is_last):
		file_name = str(path)
		gpf_dist_1 = "gpfdist://" + str(server) + "-1:"
		gpf_dist_2 = "gpfdist://" + str(server) + "-2:"
		new_file_name = re.sub("/data/incoming","",file_name)
		if (is_last):
			self.gpf_file_path += r"'" + gpf_dist_1 + new_file_name + r"'" + ", " + r"'" + gpf_dist_2 + new_file_name + r"'"
		else:
			self.gpf_file_path += r"'" + gpf_dist_1 + new_file_name + r"'" + ", " + r"'" +  gpf_dist_2 + new_file_name + r"'" + ", \n"

	def get_gpf_file_loc(self):
		return self.gpf_file_path