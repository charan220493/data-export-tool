import argparse
import random
import os
import sys
import shutil
import re
import glob
import string
import time

sys.path.append("/data/incoming/cpuladas/bin")
import psycopg2
import psycopg2.extensions
from psycopg2.extensions import AsIs

class gp_access_util:
	
	def __init__(self):
		self.conn = None
		self.cursor = None

	def create_connection_string(self, db, host, user):
		return "dbname = " + str(db) + " host = " + str(host) + " user = " + str(user) + " password = changeme"

	def create_temp_table(self):
		size = 6
		chars = string.ascii_uppercase + string.digits
		random_string = ''.join(random.choice(chars) for _ in range(size))
		table_name = "EXT_TEMP_TABLE_" + random_string
		return table_name

	def open_connection(self, connection_string):
		self.conn = psycopg2.connect(connection_string)
		self.cursor = self.conn.cursor()
		return True

	def execute_export(self, location_string, source_table, exteral_table_name, delimiter):
		success = False
		try:
			parameter_dict = dict()
			parameter_dict["location"] = AsIs(location_string)
			parameter_dict["src_table"] = AsIs(source_table)
			parameter_dict["ext_temp_table"] = AsIs(exteral_table_name)
			delimiter = r"'" + str(delimiter) + r"'"
			parameter_dict["delimiter"] = AsIs(delimiter)
			start_time = time.time()
			self.cursor.execute("""DROP TABLE IF EXISTS %(ext_temp_table)s;CREATE WRITABLE EXTERNAL TEMP TABLE %(ext_temp_table)s(LIKE %(src_table)s)LOCATION (%(location)s)FORMAT 'TEXT' (DELIMITER E%(delimiter)s NULL '' ESCAPE 'off');INSERT INTO %(ext_temp_table)s SELECT * FROM %(src_table)s;""",parameter_dict)
			end_time = time.time()
			execute_time = end_time - start_time
			print("Time taken by export: " + str(execute_time))
			sys.stdout.flush()
		except Exception as e:
			print("Exception is thrown trying to execute export is: " + str(e))
		else:
			success = True
		finally:
			self.close_connection()
			return success


	def close_connection(self):
		if (self.cursor):
			self.cursor.close()
		if (self.conn):
			self.conn.close()