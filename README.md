# ReadMe

## Description
The GreenPlum Export tool is to carry out data transfer from any GreenPlum Database to its corresponding servers.
Parameters it takes in are:
* database: gp_adw/gp_edw
* host:	  CSRI4GPM01/CSIA4GPM01/CSOR2GPM01/CSIA2GPM01
* server: Name of the GPL server 
* username: useraccount
* source_table: Contents of the table to be exported
* destination:  Destination path should be only be a directory on the linux servers where data is to be stored.
	Currently supported servers for the following hosts are:
	* CSRI4GPM01: CSRI4GPL07,
	* CSIA4GPM01: 
	* CSOR2GPM01: 
	* CSIA2GPM01:
* optional args:
		* delimiter: Specify a custom delimiter. Default is '\t'
		* filename: Specify the flat file name, if the output is desired to be a single flat file. Eg: flatfile.txt
		* compression: Specify the compression on data. Default is no compression and currently only GZ compression is suppported.
		* ports: Specify an integer between 1-8, default value is 6. This is to choose the number of ports to be used for export.
		* parts_per_port: Specify the number of instances each port gets while doing the export. Default is 10. Max shouldn't be more than 45
	
## Description of Packages and classes:
* Packages:					
	* gp_access_util: This class uses the psycopg2 module to open, execute a query and close the connection on a database.					
	* gp_file_util:
	This class is to create the destination path (throws an exception if destination path already exists) and
	a temp directory under the destination path with empty part files that will have data written into them by
	the gp_access_util class. It has additional step that concatenates all the part files
	if the destination path ends with the extension .txt, assuming the user wants one single flat file. It also 
	is responsible to get the location path of all the temp part files which is parsed to gp_access_utils class
	as the value for location parameter.
						
* Export Driver:
    This pyhton script is reponsible to collect the arguments parsed by the user and exceute the following steps:
    1. Try to open a connection on GreenPlum
	2. Create destination path and temp empty part files
	3. Create external table and write data from source_table to destination/temp/part-*
	4. Close connection on greenPlum
	5. Move file from destination/temp/part-* to destination/part-*
		* Concatenate the part files if destiantion path ends as .txt

	
						
	
						