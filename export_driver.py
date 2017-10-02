import argparse
import random
import os
import sys
import shutil
import re
from export_helper import gp_access_util, gp_file_util

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("database", help="specify database as: gp_adw/gp_edw")
	parser.add_argument("host", help="specify host as: CSRI4GPM01/CSIA4GPM01/CSOR2GPM01/CSIA2GPM01")
	parser.add_argument("server", help="specify server as: CS[RI4/IA4/IA2/OR2]GPL0[1-8]. This has to be same as the server on which this code is running on")
	parser.add_argument("username", help="specify username as: gpuser_name")
	parser.add_argument("source_table", help="specify the table to export")
	parser.add_argument("destination", help="specify destination directory on GP client server",type = str)
	parser.add_argument("--delimiter", help="specify a delimiter to use when exporting data. Default is TAB delimiter",type=str, default = "\t")
	parser.add_argument("--filename", help="specify flat file name if the data is desired to be in one flat file", type = str, default = None)
	parser.add_argument("--compression", help="specify the compression need by its extension", type = str, default = None)
	parser.add_argument("--ports", help="specify number of ports to be used, max is 8, min is 1", type = int, choices = list(range(9)), default = 6)
	parser.add_argument("-ppm","--parts_per_port", help="try to limit this to 45", type = int, default = 20)
	args = parser.parse_args()

	if (args.filename):
		is_flat_file = True
	else:
		is_flat_file = False

	gp_file_obj = gp_file_util()
	gp_connect_obj = gp_access_util()
	connection_args_string = gp_connect_obj.create_connection_string(args.database, args.host, args.username)
	
	try:
		if (args.compression):
			gp_file_obj.set_compression(args.compression)

		if (gp_connect_obj.open_connection(connection_args_string)):
			create_files = gp_file_obj.create_files(args.server, args.destination, args.ports, args.parts_per_port)
			print("Empty temp part files have been created")
			sys.stdout.flush()
			if (create_files):
				export_success = gp_connect_obj.execute_export(gp_file_obj.get_gpf_file_loc(), args.source_table, gp_connect_obj.create_temp_table(), args.delimiter)
				if (export_success):
					print("Export successful")
					sys.stdout.flush()
				else:
					shutil.rmtree(args.destination)
					raise Exception("Export unsucessful! If you see the error: External table has more URLs then available primary segments, then decrease -ppm value to 40 or less")

				moved_files = gp_file_obj.mv_files(args.destination, args.filename, is_flat_file)
				if (moved_files):
					print("Moved data from temp location to destination path")
					sys.stdout.flush()
				else:
					raise Exception("Some error when trying to move files from temp location to destination path")
			else:
				raise Exception("check if destination path exists or file permission allow to create files")
		else:
			gp_connect_obj.close_connection()
			raise Exception("Couldn't open connection error")

	except Exception as e:
		print("Exception thrown is: " + str(e))
		sys.stdout.flush()
		sys.exit(1)

	else:
		sys.exit(0)


if __name__ == '__main__':
	main()