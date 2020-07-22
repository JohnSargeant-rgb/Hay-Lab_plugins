from ij.gui import GenericDialog
from fiji.util.gui import GenericDialogPlus
import os, shutil

gdp=GenericDialogPlus("File Mover")
file_type = gdp.getNextString()
gdp.addStringField("File Extension ", '.tif',5)
x=gdp.addDirectoryField("Source: ", " ")
gdp.addDirectoryField("Destination: ", " ")
gdp.showDialog()
if gdp.wasOKed():
	file_type = gdp.getNextString().strip()
	source_path = gdp.getNextString()
	dest_path = gdp.getNextString()
	print(file_type)
	print("source " +source_path)
	print("dest " +dest_path)	
else:
	exit()

moved ='Moved Images'
path =os.path.join(dest_path, moved)
try:
	dest=os.mkdir(path)
except OSError as error:
	print("Error: Moved Images is already present")
	exit()

def move(): 
	for root, dirs, files in os.walk((os.path.normpath(source_path)), topdown=False):
        	for name in files:
            		if name.endswith(file_type):
                		SourceFolder = os.path.join(root,name)
                		shutil.copy2(SourceFolder, path) #copies .tif to new folder

move()