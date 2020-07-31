from fiji.util.gui import GenericDialogPlus
from ij.gui import GenericDialog
import os, shutil
import uuid
import sys

gdp=GenericDialogPlus("File Randomizer")
file_type = gdp.getNextString()
gdp.addStringField("File Extension ", '.tif',5)
x=gdp.addDirectoryField("Source:", " ")
gdp.addDirectoryField("Destination:", "(optional)")
gdp.addCheckbox("Copy & Move",False)
gdp.showDialog()
if gdp.wasOKed():
	file_type = gdp.getNextString().strip()
	source_path = gdp.getNextString().strip()
	dest_path = gdp.getNextString().strip()
	copymove=gdp.getNextBoolean()
	if dest_path == '(optional)':
		dest_path = source_path

else:
	exit()

##makes a new directory in the destination directory, called randomized.
key='key.csv'
r_key= os.path.join(dest_path,key)

if copymove ==True:
	randomized = 'randomized'
	path = os.path.join(dest_path,randomized)
	path = path+'/'
	try:
		os.mkdir(path)
		
	except OSError as error:
		print("Error: randomized folder is present")
		print("Rename or move folder")
		exit()
		
	for image in os.listdir(source_path):
		if image.lower().endswith(file_type):
			shutil.copy(os.path.join(source_path, image), path)
	
# creates a key where old and new filenames will be stored.		
	r_key= os.path.join(path,key)


## generates a random filename for each tif in the randomized subfolder,  outputs to the key
with open(r_key,'a') as OUT:
	if copymove == False:
		path = dest_path
	for filename in os.listdir(path):
		if filename.endswith(file_type):
			name = str(uuid.uuid4()) 
			save_stdout = sys.stdout
			sys.stdout = OUT
			print filename, ",",name + file_type
			sys.stdout = save_stdout
			dst = name + file_type
			if copymove == False:
				src = filename
				os.chdir(path)
				os.rename(src,dst)
			else:
				src = path + filename
				dst = path + dst
				os.rename(src,dst)
