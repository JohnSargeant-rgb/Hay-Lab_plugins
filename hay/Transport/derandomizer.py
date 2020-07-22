import csv
from ij.gui import Roi, PolygonRoi, GenericDialog, TextRoi, NonBlockingGenericDialog
import os
from fiji.util.gui import GenericDialogPlus


gdp=GenericDialogPlus("File Derandomizer")
gdp.addFileField("'Key' path :", " ")
gdp.addFileField("Data file :", " ")
gdp.addDirectoryField("Derandomized path", "(optional)")
gdp.showDialog()
if gdp.wasOKed():
	key_path = gdp.getNextString().strip()
	data_path = gdp.getNextString().strip()
	deR_path = gdp.getNextString().strip()
	if deR_path == "(optional)":
		deR_path = os.path.dirname(data_path) 
else:
	exit()

##opens an empty dictionary called random and populates it with key vales pairs from our key. 

random ={}

with open(key_path, 'r') as csv_file:
	csv_reader =csv.reader(csv_file, delimiter=',')
	for k,v in csv_reader:
		random.update({k.strip():v.strip()})

 
def replace(text,dic):
	"""Replaces values with keys"""
	for k,v in random.items():
		text=text.replace(v,k)
	return text
	
##reads randomized data file and replaces values with keys using the replace function. 
with open(data_path,'r') as data:
	text = data.read()
	text =replace(text,random)
	

data_path = data_path[:-4]
path = data_path +'_derandomized.csv'


## takes all lines from now unrandomized data file and writes it to a new csv.
with open(path,'w') as sorted_csv:
	sorted_csv.write(text)
