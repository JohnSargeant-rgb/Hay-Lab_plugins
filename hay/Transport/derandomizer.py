import csv
from ij.gui import Roi, PolygonRoi, GenericDialog, TextRoi, NonBlockingGenericDialog
import os
from fiji.util.gui import GenericDialogPlus
import re

gdp=GenericDialogPlus("File Derandomizer")
gdp.addFileField("'Key' path :", " ")
gdp.addFileField("Data file :", " ")
gdp.addDirectoryField("Derandomized path", "(optional)")
gdp.addDirectoryField("Processed Image Folder", " ")
gdp.addCheckbox("Derandomize Data File", True)
gdp.addCheckbox("Derandomize Image Folder", False)

gdp.showDialog()
if gdp.wasOKed():
	key_path = gdp.getNextString().strip()
	data_path = gdp.getNextString().strip()
	deR_path = gdp.getNextString().strip()
	pi_path= gdp.getNextString().strip()
	ddf=gdp.getNextBoolean()
	dif=gdp.getNextBoolean()
	if deR_path == "(optional)":
		deR_path = os.path.dirname(data_path) 
else:
	exit()


# function to return key for any value
def get_key(val):
    for key, value in random.items():
         if val == value:
             return key

def replace(text,dic):
	"""Replaces values with keys"""
	for k,v in random.items():
		text=text.replace(v,k)
	return text
	
##opens an empty dictionary called random and populates it with key vales pairs from our key. 
random ={}
with open(key_path, 'r') as csv_file:
	csv_reader =csv.reader(csv_file, delimiter=',')
	for k,v in csv_reader:
		random.update({k.strip():v.strip()})

if dif is True:
	add_string ='.tif'
	for filename in os.listdir(pi_path):
		name= re.search("(\#\d+\_)(\w+\-\w+\-\w+\-\w+\-\w+)",filename)
		if name:
			search_name=str(name.group(2)) +str(add_string)
			new_name= str(name.group(1))+get_key(search_name)
			os.chdir(pi_path)
			os.rename(filename.strip(),new_name.strip())

if ddf is True:
##reads randomized data file and replaces values with keys using the replace function. 
	with open(data_path,'r') as data:
		text = data.read()
		text =replace(text,random)
	

	data_path = data_path[:-4]
	path = data_path +'_derandomized.csv'


## takes all lines from now unrandomized data file and writes it to a new csv.
	with open(path,'w') as sorted_csv:
		sorted_csv.write(text)
