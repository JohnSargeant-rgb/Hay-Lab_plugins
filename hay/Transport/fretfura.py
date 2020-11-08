from __future__ import division
from ij import IJ, ImagePlus, ImageStack
from ij.process import FloatProcessor, ImageProcessor
from ij.gui import Roi, PolygonRoi, GenericDialog, TextRoi, NonBlockingGenericDialog, PointRoi, OvalRoi, Overlay
import re
from java.awt import Color, Font
import sys
import os
import csv
from fiji.util.gui import GenericDialogPlus
from loci.formats import ChannelSeparator
from ij.io import Opener
import json
import time


boldFont = Font("SansSerif", Font.BOLD, 13)
fret_fura = []
fret_fura.append("C1/C2 (FURA)")
fret_fura.append("C2/C1 (FRET)")
dest = IJ.getDirectory("image")
gdp = GenericDialogPlus("FRET Assay, Version 3.1")
gdp.addDirectoryField("Output Location:", dest, 40)
gdp.addStringField("Processed Folder:", 'Processed_FRET', 40)
gdp.addStringField("FRET Outfile:", 'FRET_Outfile.csv', 40)
gdp.addStringField("Selection Radius:", '3', 10)
gdp.addStringField("Acquisition delay (sec):", '4', 10)

gdp.addRadioButtonGroup("", fret_fura, 1, 2, "C1/C2 (FURA)")
gdp.addCheckbox("Set Background to value:", False)
gdp.addToSameRow()
gdp.addStringField("", '0', 5)

gdp.addCheckbox("Blur Image? Input sigma value:", False)
gdp.addToSameRow()
gdp.addStringField("", '4', 5)
gdp.addMessage(" ")
gdp.addMessage("Set R0 range (timepoint position x to y):", boldFont)
gdp.addStringField("x:", '2', 3)
gdp.addToSameRow()
gdp.addStringField(" y:", '8', 3)
gdp.addMessage("Set output file headers:", boldFont)
gdp.addStringField("Channel 1:", 'A', 8)
gdp.addToSameRow()
gdp.addStringField("Channel 2:", 'B', 8)
gdp.addStringField("Channel Z/Channel W:", 'C', 8)
gdp.addToSameRow()
gdp.addStringField("R/R0:", 'D', 8)
gdp.showDialog()
if gdp.wasOKed():
    dest = gdp.getNextString().strip()
    ProFolder = gdp.getNextString().strip()
    Procsv = gdp.getNextString().strip()
    radius = int(gdp.getNextString().strip())
    interval = int(gdp.getNextString().strip())
    f_f = gdp.getNextRadioButton()
    back_state = gdp.getNextBoolean()
    back_val = int(gdp.getNextString().strip())
    blur_state = gdp.getNextBoolean()
    blur_val = int(gdp.getNextString().strip())
    r_start = int(gdp.getNextString().strip())
    r_end = int(gdp.getNextString().strip())
    ch1_str = gdp.getNextString().strip()
    ch2_str = gdp.getNextString().strip()
    ch12_str = gdp.getNextString().strip()
    rr0_str = gdp.getNextString().strip()


imp_save = IJ.getImage()
Save_Title = imp_save.getTitle()


###
def selection(region):
    nbgd = NonBlockingGenericDialog(region)
    nbgd.setCancelLabel('Return')
    nbgd.enableYesNoCancel('ROI OK', 'Redraw')
    nbgd.showDialog()
    if nbgd.wasOKed():
        imp = IJ.getImage()
        roi = imp.getRoi()
        roi_check(roi)
        return
    if nbgd.wasCanceled():
        exit_assay()
    else:
        repeat_measure()


def roi_check(roi):
    if roi == None:
        repeat_measure()


def selection_mean():
    ###for a selected ROI, gets the sum of all pixels/divided by the number of pixels###
    imp_s = IJ.getImage()
    roi = imp_s.getRoi()
    mask = roi.getMask()
    ip = imp_s.getProcessor()
    r = roi.getBounds()
    total = sum_pixels = 0
    for y in range(r.height):
        for x in range(r.width):
            if mask.get(x, y) != 0:
                total += 1
                sum_pixels += ip.getf(r.x+x, r.y+y)
    average = sum_pixels/total
    return average


imp = IJ.getImage()
imp.setT(1)
imp.setC(1)

imp = IJ.getImage()
current_title = imp.getTitle()


IJ.run("Remove Overlay")
# gets the current image & finds the number of channels and timepoints
imp = IJ.getImage()
timepoint = imp.getT()
slic = imp.getNChannels()
all_time = imp.getNFrames()

# creates a list of the number of channels and the number of timepoints.
channel_list = []
for i in range(1, slic+1):
    channel_list.append(i)
# print(channel_list)

timepoint_list = []
for i in range(1, all_time+1):
    timepoint_list.append(i)
# print(timepoint_list)


def background_assay():
    for channel in channel_list:
        imp.setC(channel)
        for time in timepoint_list:
            imp.setT(time)
            if channel == 1:
                background = selection_mean()
                background_c1.append(background)
            if channel == 2:
                background = selection_mean()
                background_c2.append(background)
    return background_c1, background_c2


background_c1 = []
background_c2 = []
if back_state == False:
    IJ.setTool("oval")
    region = "Select Background"
    selection(region)
    background_c1, background_c2 = background_assay()
if back_state == True:
    # sets background to value
    zero_bck = []
    for i in range(1, all_time+1):
        zero_bck.append(back_val)
    background_c1 = zero_bck
    background_c2 = zero_bck


# ok we can now access these variables.


# resets image
imp = IJ.getImage()
imp.setT(1)
imp.setC(1)

# sets the tools to be used
IJ.run("Point Tool...", "type=Cross color=Yellow size=Tiny label counter=0 add_to")
IJ.setTool("point")
# Asks you to select cells, hitting cancel if you made a mistake
nbgd = NonBlockingGenericDialog("Select Cells")
nbgd.showDialog()
if nbgd.wasCanceled():
    IJ.run("Remove Overlay")
# turns the overlay into an object.
imp = IJ.getImage()
overlay = Overlay()
overlay = imp.getOverlay()
# asks if you have selected anything
try:
    roi_points = overlay.toArray()
except AttributeError as error:
    nbgd = NonBlockingGenericDialog("Select some cells boi")
    nbgd.showDialog()
if blur_state == True:

    set_sigma = "sigma="+str(blur_val)+" stack"
    IJ.run("Gaussian Blur...", set_sigma)
path = os.chdir(dest)
if not os.path.exists(ProFolder):
    os.mkdir(ProFolder)
    os.chdir(ProFolder)
    Path = (os.getcwd())
    IJ.run("Copy to System")
    IJ.saveAs('Tiff', os.path.join(Path, Save_Title))
else:
    os.chdir(ProFolder)
    Path = (os.getcwd())
    IJ.run("Copy to System")
    IJ.saveAs('Tiff', os.path.join(Path, Save_Title))

fret_csv = Path+'/'+Procsv


all_x = []
all_y = []
for i in range(overlay.size()):
    roi = overlay.get(i)
    p = roi_points[i].getPolygon()
    all_x.append(p.xpoints[0])
    all_y.append(p.ypoints[0])

x_y = list(zip(all_x, all_y))


cell = []

bckc1 = background_c1[0:r_end]
bckc2 = background_c2[0:r_end]


cell_channel_1 = []

cell_channel_2 = []
r0 = []
for x, y in x_y:
    x = int(x)
    y = int(y)
    new_x = int(x) - radius
    new_y = int(y) - radius
    cell_channel_1 = []
    cell_channel_2 = []
    for channel in channel_list:
        imp.setC(channel)
        for j in range(timepoint_list[0], timepoint_list[r_end]):
            imp.setT(j)
            imp = IJ.getImage()
            roi = OvalRoi(new_x, new_y, radius*2, radius*2)
            imp.setRoi(roi)
            cell_mean = (selection_mean())
            if channel == 1:
                cell_channel_1.append(cell_mean)
            if channel == 2:
                cell_channel_2.append(cell_mean)
            if len(cell_channel_1) == r_end:
                Tch1_8 = [cell_channel_1[i] - bckc1[i] for i in range(len(cell_channel_1))]
                cell_channel_1 = []
            if len(cell_channel_2) == r_end:
                Tch2_8 = [cell_channel_2[i] - bckc2[i] for i in range(len(cell_channel_2))]
                cell_channel_2 = []
                if f_f == "C1/C2 (FRET)":
                    c2_c1 = [Tch1_8[i] / Tch2_8[i] for i in range(len(Tch2_8))]
                if f_f == "C2/C1 (FURA)":
                    c2_c1 = [Tch2_8[i] / Tch1_8[i] for i in range(len(Tch2_8))]
                x = sum(c2_c1[r_start:r_end])/len(c2_c1[r_start:r_end])
                r0.append(x)


# resets image
imp = IJ.getImage()
imp.setT(1)
imp.setC(1)


header_list = []


header_list.append("Image_Title")
header_list.append("Time_min")
header_list.append("ch1_bck")
header_list.append("ch2_bck")
for i in range(1, len(x_y)+1):
    header_list.append(ch1_str + '_' + str(i))
    header_list.append(ch2_str + '_' + str(i))
    header_list.append(ch12_str + '_' + str(i))
    header_list.append(rr0_str + '_' + str(i))


bck_count = 0
cell = []
for j in timepoint_list:
    imp.setT(j)
    count = 0
    for x, y in x_y:
        count += 1
        x = int(x)
        y = int(y)
        new_x = int(x) - radius
        new_y = int(y) - radius
        imp = IJ.getImage()
        roi = OvalRoi(new_x, new_y, radius*2, radius*2)
        imp.setRoi(roi)
        cell_mean_c1 = (selection_mean())
        cell_mean_c1 = cell_mean_c1 - background_c1[j-1]
        cell.append(cell_mean_c1)
        IJ.run(imp, "Draw", "slice")
        imp.setC(2)
        imp.setRoi(roi)
        cell_mean_c2 = (selection_mean())
        cell_mean_c2 = cell_mean_c2 - background_c2[j-1]
        cell.append(cell_mean_c2)
        if f_f == "C1/C2 (FRET)":
            c1overc2 = cell_mean_c1/cell_mean_c2
        if f_f == "C2/C1 (FURA)":
            c1overc2 = cell_mean_c2/cell_mean_c1
        r_r0 = c1overc2/r0[count-1]
        cell.append(c1overc2)
        cell.append(r_r0)
        imp.setC(1)
    with open(fret_csv, 'ab') as myfile:
        cell.insert(0, background_c2[bck_count])
        cell.insert(0, background_c1[bck_count])
        time_minutes = round((j*interval)/60, 2)
        cell.insert(0, time_minutes)
        cell.insert(0, current_title)
        csv_output = csv.DictWriter(myfile, fieldnames=header_list)
        myfile.seek(0, 2)
        if myfile.tell() == 0:
            csv_output.writeheader()
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(cell)
        cell = []
        bck_count += 1


IJ.run("Remove Overlay")

imp.setT(1)
imp.setC(1)
