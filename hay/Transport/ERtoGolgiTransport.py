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


json_selected = "json_selected.json"

# switches to a grayscale viewing mode
imp = IJ.getImage()
imp.setDisplayMode(IJ.GRAYSCALE)


def file_opener(current_title, extension):
    for filename in os.listdir(dest):
        i = 0
        if filename.endswith(file_type):
            pass
            if filename != current_title:
                pass
                if not filename.startswith(extension) and i == 0:
                    O = Opener()
                    path = os.path.join(dest, filename)
                    O.open(path)
                    i += 1
                    break


def renamer(dest, current_title, extension):
    for filename in os.listdir(dest):
        if filename == current_title:
            current_title_path = os.path.join(dest, current_title)
            processed_title = (extension + current_title)
            processed_title_path = os.path.join(dest, processed_title)
            os.rename(current_title_path, processed_title_path)


def current_channels():
    ### gets the number of channels in a stack and creates a list of channels available  ###
    imp = IJ.getImage()
    stack = imp.getImageStackSize()
    channels_available = []
    for i in range(stack+1):
        if i != 0:
            channels_available.append(str(i))
    channels_available.append("-")
    return channels_available


def mean_max_channels():
    imp = IJ.getImage()
    stack = imp.getImageStackSize()
    mean_max_channels = []
    for i in range(stack+1):
        if i != 0:
            mean_max_channels.append(str(i))
# Locate already define channels
    for channel in mean_max_channels:
        if channel == transport_c:
            mean_max_channels.remove(channel)
    for channel in mean_max_channels:
        if channel == golgi_c:
            mean_max_channels.remove(channel)
    return(mean_max_channels)


def images_processed(dest):
    list_dir = os.listdir(dest)
    total_images = 0
    processed = 0
    for image in list_dir:
        if image.endswith(file_def):
            total_images += 1
            if image.startswith(ext_def):
                processed += 1
    percent_complete = round((processed/total_images)*100)
    return percent_complete, total_images, processed


# sets up a list of avaialble channels in a stack and viewing options
channels_available = current_channels()
channel_iterator = channels_available[:-1]
color_options = ['Color', 'Gray', 'HiLo', 'Cyan Hot', 'Magenta Hot', 'mpl-viridis', 'mpl-plasma']
zoom = ['-4', '-3', '-2', '-1', '  0', '1', '2', '3', '4']
italicFont = Font("SansSerif", Font.BOLD, 15)


try:
    # Reading from json file
    dest = IJ.getDirectory('Image')
    os.chdir(dest)
    json_selected = os.path.join(dest, json_selected)
    json_selected = json_selected+'/'

    with open(json_selected, 'r') as openfile:
        json_object = json.load(openfile)
    ProFolder_def = json_object['ProFolder_def']
    Quant_def = json_object['Quant_def']
    Quant_MM_def = json_object['Quant_MM_def']
    tran_def = json_object['tran_def']
    golgi_def = json_object['golgi_def']
    ext_def = json_object['ext_def']
    zoom_def = json_object['zoom_def']
    radius_def = json_object['radius_def']
    color_def = json_object['color_def']
    golgi_select_def = json_object['golgi_select_def']
    auto_golgi_def = json_object['auto_golgi_def']
    mean_max_def = json_object['mean_max_def']
    file_def = json_object['file_def']


except:
    ## sets default values ##
    default_values = {
        "ProFolder_def": 'Processed_RENAME',
        "Quant_def": 'Quant_RENAME.csv',
        "Quant_MM_def": 'Mean_Max_Quant_RENAME.csv',
        "tran_def": "-",
        "golgi_def": "-",
        "ext_def": '*',
        "zoom_def": '2',
        "radius_def": "2",
        'color_def': 'Gray',
        'golgi_select_def': False,
        'auto_golgi_def': False,
        'mean_max_def': False,
        'file_def': '.tif'
    }
    ProFolder_def = default_values['ProFolder_def']
    Quant_def = default_values['Quant_def']
    Quant_MM_def = default_values['Quant_MM_def']
    tran_def = default_values['tran_def']
    golgi_def = default_values['golgi_def']
    ext_def = default_values['ext_def']
    zoom_def = default_values['zoom_def']
    radius_def = default_values['radius_def']
    color_def = default_values['color_def']
    golgi_select_def = default_values['golgi_select_def']
    auto_golgi_def = default_values['auto_golgi_def']
    mean_max_def = default_values['mean_max_def']
    file_def = default_values['file_def']
    # Dumps values into a dictionary
    json_object = json.dumps(default_values, indent=4)
    dest = IJ.getDirectory("image")
    os.chdir(dest)
    json_selected = os.path.join(dest, json_selected)
    json_selected = json_selected+'/'
    # Writing to sample.json
    with open(json_selected, "w") as outfile:
        outfile.write(json_object)


# sets up a generic dialog box to start the script.
dest = IJ.getDirectory("image")
gdp = GenericDialogPlus("Transport Assay")
gdp.addDirectoryField("Image Folder:", dest, 40)
gdp.addStringField("Processed Image Folder:", ProFolder_def, 40)
gdp.addStringField("Transport Output:", Quant_def, 40)
gdp.addStringField("Mean_Max Output:", Quant_MM_def, 40)
gdp.addMessage("    ", italicFont)
gdp.addChoice("Transport Channel:", channels_available, tran_def)
gdp.addToSameRow()
gdp.addStringField("File Type: ", file_def, 5)
gdp.addChoice("  Golgi Channel:", channels_available, golgi_def)
gdp.addToSameRow()
gdp.addStringField("Processed File Extension: ", ext_def, 5)
gdp.addMessage("    ", italicFont)
gdp.addToSameRow()
gdp.addMessage("    ", italicFont)
gdp.addChoice(" Zoom: ", zoom, zoom_def)
gdp.addToSameRow()
gdp.addStringField("ER Selection Radius: ", radius_def, 5)
gdp.addChoice("View Mode:", color_options, color_def)
gdp.addMessage("    ", italicFont)
gdp.addMessage("  Advanced: ", italicFont)
gdp.addCheckbox("Always Select Golgi", golgi_select_def)
gdp.addToSameRow()
gdp.addCheckbox("Always Auto-Detect Golgi", auto_golgi_def)
gdp.addCheckbox("Mean_Max Detection", mean_max_def)
gdp.addMessage("    ", italicFont)
progress = images_processed(dest)
gdp.addMessage(str(progress[0])+'% Images Assayed' + ' ' +
               '(' + str(progress[2]) + '/' + str(progress[1]) + ')', italicFont)
gdp.addHelp("https://github.com/JohnSargeant-rbg?tab=projects")
gdp.showDialog()
if gdp.wasOKed():
    dest = gdp.getNextString().strip()
    ProFolder = gdp.getNextString().strip()
    Quant = gdp.getNextString().strip()
    Quant_MM = gdp.getNextString().strip()
    transport_c = gdp.getNextChoice()
    file_type = gdp.getNextString().strip()
    golgi_c = gdp.getNextChoice()
    extension = gdp.getNextString().strip()
    zoom_to = int(gdp.getNextChoice())
    radius = gdp.getNextString().strip()
    color_scale = gdp.getNextChoice()
    always_select = gdp.getNextBoolean()
    always_auto = gdp.getNextBoolean()
    mean_max_det = gdp.getNextBoolean()

    new_selected_values = {
        "ProFolder_def": ProFolder,
        "Quant_def": Quant,
        "Quant_MM_def": Quant_MM,
        "tran_def": transport_c,
        "file_def": file_type,
        "golgi_def": golgi_c,
        "ext_def": extension,
        "zoom_def": str(zoom_to),
        "radius_def": radius,
        "color_def": color_scale,
        "golgi_select_def": always_select,
        "auto_golgi_def": always_auto,
        "mean_max_def": mean_max_det

    }
    # save selected values as defaults.
    json_object = json.dumps(new_selected_values, indent=4)
    with open(json_selected, "w") as outfile:
        outfile.write(json_object)

    os.chdir(dest)
    Quant = os.path.join(dest, Quant)
    Quant = Quant+'/'
    Quant_MM = os.path.join(dest, Quant_MM)
    Quant_MM = Quant_MM+'/'

    firstpass = True
else:
    exit()


###Variables Collected:##
# file_type
# dest
# radius
# transport_c
# golgi_c
# zoom_to
# extension


def getOptions(dest):
    ###function that allows the user to choose their next course of action###
    # colorscale()
    gd = NonBlockingGenericDialog("Continue?")
    gd.setCancelLabel("Quit")
    gd.enableYesNoCancel("Remain on Image", "Open Next")
    gd.showDialog()
    if gd.wasCanceled():  # quits
        imp = IJ.getImage()
        current_title = imp.getTitle()
        imp.close()
        renamer(dest, current_title, extension)
        exit()
    elif gd.wasOKed():  # remains on image
        count_options = 0

        return
    else:  # opens the next image in a directory.
        count_options = 1
        imp = IJ.getImage()
        current_title = imp.getTitle()
        imp.close()
        renamer(dest, current_title, extension)
        file_opener(current_title, extension)
        imp = IJ.getImage()
        imp.setDisplayMode(IJ.GRAYSCALE)
        colorscale()
        getOptions(dest)


def high(bit_depth):
        ## extracts a few maximum intensity pixels from an image or ROI then averages them. ##
    imp = IJ.getImage()
    roi = imp.getRoi()
    try:
        mask = roi.getMask()
        ip = imp.getProcessor()
        r = roi.getBounds()
        PIXELS = []
        for y in range(r.height):
            for x in range(r.width):
                if mask.get(x, y) != 0:
                    PIXEL = (ip.getf(r.x+x, r.y+y))
                    PIXELS.append(PIXEL)
        PIXELS2 = sorted(PIXELS)
    except:
        ip = imp.getProcessor().convertToFloat()
        PIXELS = ip.getPixels()
        PIXELS2 = PIXELS.tolist()
        PIXELS2 = sorted(PIXELS)
    # getting an image, saving the array as PIXELS
    # convert the array to a list (PIXELS2) and order it from low to high
    counter = 0
    total_intensity = 0
    threshold_start = .0001
    while threshold_start * float(len(PIXELS)) <= 3:
        threshold_start += .0002
    threshold = threshold_start * float(len(PIXELS))
    # setting the threshold as .01% of the number of pixels in the image
    # it is smaller than the background, so I'm using a lower threshold to calculate the max
    Flag = True
    for i in range(len(PIXELS2)-int(threshold)-1, len(PIXELS2), 1):
        if PIXELS2[i] == bit_depth:
            print "WARNING: PIXEL VALUES SATURATED"
            Flag = False
            #gd =GenericDialog("PIXEL VALUES SATURATED")
            # gd.hideCancelButton()
            # gd.showDialog()
            # quit()
            # when the pixel value is saturated, it prints a warning and doesnt use it in calculations
        else:
            counter = counter + 1
            if counter <= int(threshold):
                d = PIXELS2[i]
                total_intensity = total_intensity + d
                # variable d is set to the last value that went through the loop
                # total intenstiy adds every pixel value that falls under the threshold
                # the loop goes to the next element in the list
    if Flag == True:
        average_max = total_intensity / int(threshold)
    else:
        average_max = " PIXEL VALUES SATURATED"

    # takes the average intensity for the top values in the cell not including a saturated value
    return average_max


def low():
    ##establishes a background value ##
    imp = IJ.getImage()
    ip = imp.getProcessor().convertToFloat()
    PIXELS = ip.getPixels()
    PIXELS2 = PIXELS.tolist()
    PIXELS2 = sorted(PIXELS)
    # getting an image, saving the array as PIXELS
    # convert the array to a list (PIXELS2) which happens to order it from low to high
    i = 0
    counter = 0
    threshold = .001 * float(len(PIXELS))
    # setting the threshold as .1% of the number of pixels in the image
    for i in xrange(len(PIXELS2)):
        if PIXELS2[i] == 0:
            i = i+1
            # when the pixel value is zero, the loop does nothing exept go to the next element in list
        else:
            counter = counter + 1
            if counter < int(threshold):
                d = PIXELS2[i]
                i = i+1
                # when the pixel value is not zero the counter increases by one until the threshold
                # variable d is set to the last value that went through the loop
                # the loop goes to the next element in the list
    return d
# prints the last value that was met before hitting the threshold


def bit_tester(image_name):
    ## gets the number of bits for an image, error if not 8 or 16 bit. ##
    dest = IJ.getDirectory("image")
    filepath = dest + image_name
    fr = ChannelSeparator()
    fr.setId(filepath)
    bitDepth = fr.getBitsPerPixel()
    if int(bitDepth) in (8, 16):
        if int(bitDepth) == 8:
            bit_depth = 2**(bitDepth)-1
        if int(bitDepth) == 16:
            bit_depth = 2**(bitDepth)-1
        return bit_depth
    elif int(bitDepth) not in (8, 16):
        print("Error image is not 8 or 16 bit")
        quit()


def roi_check(roi):
    if roi == None:
        repeat_measure()


def repeat_measure():
    IJ.run("Select None")
    gd = NonBlockingGenericDialog("Redraw ROI?")
    gd.showDialog()
    if gd.wasOKed():
        selection(region)
    if gd.wasCanceled():
        exit_assay()


def exit_assay():
    gd = NonBlockingGenericDialog("Exit Assay")
    gd.setCancelLabel("Quit & Save")
    gd.setOKLabel("Quit")
    gd.showDialog()
    if gd.wasCanceled():  # quits
        imp = IJ.getImage()
        current_title = imp.getTitle()
        imp.close()
        renamer(dest, current_title, extension)
        exit()
    elif gd.wasOKed():
        exit()


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


def ER_points(all_x, all_y, overlay, ER_measurements):
    imp = IJ.getImage()
    overlay = Overlay()
    overlay = imp.getOverlay()
    ## gets points added to overlay, and extracts a list of x & y values. list length must be three ###
    try:
        roi_points = overlay.toArray()
    except AttributeError as error:
        nbgd = NonBlockingGenericDialog("Select three Roi's")
        nbgd.hideCancelButton()
        nbgd.showDialog()
        overlay = imp.getOverlay()
        roi_points = overlay.toArray()
        pass

    for i in range(overlay.size()):
        roi = overlay.get(i)
        p = roi_points[i].getPolygon()
        all_x.append(p.xpoints[0])
        all_y.append(p.ypoints[0])
    while len(all_x) != 3:
        if len(all_x) < 3:
            nbgd = NonBlockingGenericDialog("Must Select three Roi's")
            nbgd.setCancelLabel("Roi Reset")
            nbgd.showDialog()
            if nbgd.wasCanceled():
                IJ.run("Remove Overlay", "")
            ER_points(all_x, all_y, overlay, ER_measurements)
        if len(all_x) > 3:
            all_x.pop(0)
            all_y.pop(0)
    overlay.clear()


def to_transport_channel():
    if transport_c != "-":
        IJ.setSlice(int(transport_c))
    else:
        pass


def to_golgi_channel():
    if golgi_c != "-":
        IJ.setSlice(int(golgi_c))
    else:
        pass


def zoom():
    if zoom_to > 0:
        for i in range(0, zoom_to):
            IJ.run("In [+]")
    if zoom_to < 0:
        for i in range(0, zoom_to, -1):
            IJ.run("Out [-]")
    if zoom == 0:
        pass


def colorscale():
    imp = IJ.getImage()
    if color_scale == 'Gray':
        imp.setDisplayMode(IJ.GRAYSCALE)
    elif color_scale == 'Color':
        imp.setDisplayMode(IJ.COLOR)
    elif color_scale == 'HiLo':
        IJ.run('HiLo')
    elif color_scale == 'Cyan Hot':
        IJ.run('Cyan Hot')
    elif color_scale == 'Magenta Hot':
        IJ.run('Magenta Hot')
    elif color_scale == 'mpl-viridis':
        IJ.run('mpl-viridis')
    elif color_scale == 'mpl-plasma':
        IJ.run('mpl-plasma')


exit_loop = 0

while exit_loop == 0:
    if firstpass is True:
        current_image = "first_image"
        getOptions(dest)
    else:
        pass

    firstpass = False

    imp = IJ.getImage()
    image_name = imp.title

    bit_depth = bit_tester(image_name)
    colorscale()

    #set a manual background value#
    if current_image != image_name:
        IJ.setTool("oval")
        region = "Select Background"
        selection(region)
        to_transport_channel()
        background = selection_mean()

    if mean_max_det is True:
        IJ.setTool("polygon")
    else:
        IJ.setTool("rectangle")
    count_options = 0
    if count_options == 1:  # asks if we are looking at a new image
        getOptions(dest)

    region = "select cell"
    selection(region)
    IJ.run("Duplicate...", "duplicate")
    zoom()
    background_auto = 0

    # defines the golgi and background at this point.
    try:
        background
    except NameError:
        background = low()
    else:
        background_auto = low()

    if mean_max_det is True:
        cell_area = IJ.getValue(imp, "Area")
        bck_int = []
        mean_int = []
        maximum_int = []
        for channel in channel_iterator:
            channel_first = int(channel)
            IJ.setSlice(channel_first)
            # Data Collection
            bck_int.append(low())  # background
            mean_int.append(selection_mean())
            maximum_int.append(high(bit_depth))
        IJ.run("Select None")
        to_transport_channel()

    if always_select is True:
        to_golgi_channel()
        IJ.setTool("polygon")
        region = 'Select Golgi'
        selection(region)
        to_transport_channel()
        average_max = high(bit_depth)
        IJ.setForegroundColor(255, 255, 255)
        IJ.setBackgroundColor(1, 1, 1)
        imp2 = IJ.getImage()
        IJ.run(imp2, "Draw", "slice")
        IJ.run("Select None")

    if always_auto is True:
        to_transport_channel()
        average_max = high(bit_depth)

    if always_auto is False:
        if always_select is False:
            nbgd = NonBlockingGenericDialog("Golgi_selection")
            Methods = ['Automatic Selection', 'Manual Selection']
            nbgd.addRadioButtonGroup("Methods", Methods, 2, 1, Methods[0])
            nbgd.hideCancelButton()
            nbgd.showDialog()
            golgi_method = nbgd.getNextRadioButton()
            if golgi_method == Methods[0]:
                average_max = high(bit_depth)
            elif golgi_method == Methods[1]:
                to_golgi_channel()
                IJ.setTool("polygon")
                region = 'Select Golgi'
                selection(region)
                to_transport_channel()
                average_max = high(bit_depth)
                IJ.setForegroundColor(255, 255, 255)
                IJ.setBackgroundColor(1, 1, 1)
                imp2 = IJ.getImage()
                IJ.run(imp2, "Draw", "slice")
                IJ.run("Select None")

    # sets up tools for for ER measurement protocol
    IJ.run("Point Tool...", "type=Cross color=Yellow size=Tiny add_to")
    IJ.setTool("point")
    to_transport_channel()

    # user interface
    nbgd = NonBlockingGenericDialog("ER Selection")
    nbgd.addStringField("Selection radius: ", str(radius), 5)
    nbgd.hideCancelButton()
    imp = IJ.getImage()
    overlay = Overlay()
    overlay = imp.getOverlay()
    nbgd.showDialog()

    if mean_max_det is True:
        IJ.setTool("polygon")
    else:
        IJ.setTool("rectangle")

    radius = int(nbgd.getNextString().strip())
    imp = IJ.getImage()
    # set variables
    all_x = []
    all_y = []
    ER_measurements = []

    # function
    ER_points(all_x, all_y, overlay, ER_measurements)

    # set more variables
    ER = []
    x_y = {}

    # merges the x and y lists such that x,y are key:value pairs
    for x, y in zip(all_x, all_y):
        x_y.setdefault(x, []).append(y)
    # loops through x,y coordinate pairs, draw a circle and measures the average intensity.
    for x, y in x_y.items():
        x = (int(x))
        y = (int(y[0]))
        new_x = int(x) - radius
        new_y = int(y) - radius
        imp = IJ.getImage()
        roi = OvalRoi(new_x, new_y, radius*2, radius*2)
        imp.setRoi(roi)
        ER_mean = (selection_mean())
        ER.append(ER_mean)
        IJ.run(imp, "Draw", "slice")

    try:
        with open(Quant) as infile:
            reader = csv.reader(infile)
            row_count = sum(1 for row in reader)
            cell_number = row_count
    except:
        cell_number = 1

    gd = GenericDialog("Type cell number")
    gd.addStringField("Cell number", str(cell_number))
    gd.showDialog()
    number = gd.getNextString()

    ER1 = ER[0]
    ER2 = ER[1]
    ER3 = ER[2]
    total_ER = sum(ER)
    average_ER = total_ER / 3
    net_ER = average_ER - background
    try:
        net_golgi = average_max - background
        t_index = net_golgi / net_ER
    except:
        net_golgi = 'Pixels saturated in Transport Channel'
        t_index = 'Pixels saturated in Transport Channel'

    # saves image with cell number extension.
    imp_save = IJ.getImage()
    path = os.chdir(dest)
    Save_Title = imp_save.getTitle()
    newtitle = imp_save.setTitle('#'+number+'_'+Save_Title)
    SaveTitle = imp_save.getTitle()
    if not os.path.exists("P_" + ProFolder):
        os.mkdir("P_"+ProFolder)
        os.chdir("P_"+ProFolder)
        Path = (os.getcwd())
        IJ.saveAs(imp_save, file_type, os.path.join(Path, SaveTitle))
    else:
        os.chdir("P_"+ProFolder)
        Path = (os.getcwd())
        IJ.saveAs(imp_save, file_type, os.path.join(Path, SaveTitle))

    imp_save.close()
    imp = IJ.getImage()
    a = ImagePlus.getRoi(imp)
    a = str(a)
    roi = re.search(r'x=(\d+),\sy=(\d+),\swidth=(\d+),\sheight=(\d+)', a)
    x = int(roi.group(1))
    y = int(roi.group(2))
    width = int(roi.group(3))
    height = int(roi.group(4))
    resultProcessor = imp.getProcessor()
    u = .5 * width + x
    v = .5 * height + y
    color = Color(255, 255, 255)
    resultProcessor.setColor(color)
    resultProcessor.setFontSize(36)
    cell_label = resultProcessor.drawString(number, int(u), int(v))
    imp.updateAndDraw()
    IJ.run("Select None")

    if mean_max_det is True:
        while len(bck_int) < 4:
            bck_int.append(0)
            mean_int.append(0)
            maximum_int.append(0)
        headers = ['Cell', 'Cell Area', 'ch1_Background', 'ch1_avg', "ch1_Maximum", 'ch2_Background', 'ch2_avg',
                   'ch2_Maximum', 'ch3_Background', 'ch3_avg', "ch3_Maximum", 'ch4_Background', 'ch4_avg', "ch4_Maximum", "Image_title"]
        with open(Quant_MM, 'ab') as f_output_1:
            csv_output = csv.DictWriter(f_output_1, fieldnames=headers)
            f_output_1.seek(0, 2)
            if f_output_1.tell() == 0:
                csv_output.writeheader()
            csv_output.writerow({'Cell': number, 'Cell Area': cell_area, 'ch1_Background': bck_int[0], 'ch1_avg': mean_int[0], 'ch1_Maximum': maximum_int[0], 'ch2_Background': bck_int[1], 'ch2_avg': mean_int[1], 'ch2_Maximum': maximum_int[
                                1], 'ch3_Background': bck_int[2], 'ch3_avg': mean_int[2], 'ch3_Maximum': maximum_int[2], 'ch4_Background': bck_int[3], 'ch4_avg': mean_int[3], 'ch4_Maximum': maximum_int[3], 'Image_title': image_name})
    else:
        pass

    headers = ['Cell', 'AVG_Max', "bck", "bck_auto", "ER1", "ER2",
               "ER3", "net_ER", "net_golgi", "T_Index", "Image_title"]
    with open(Quant, 'ab') as f_output:
        csv_output = csv.DictWriter(f_output, fieldnames=headers)
        f_output.seek(0, 2)
        if f_output.tell() == 0:
            csv_output.writeheader()
        csv_output.writerow({'Cell': number, 'AVG_Max': average_max, 'bck': background, 'bck_auto': background_auto, 'ER1': ER1,
                             'ER2': ER2, 'ER3': ER3, 'net_ER': net_ER, 'net_golgi': net_golgi, 'T_Index': t_index, 'Image_title': image_name})
    current_image = image_name
    getOptions(dest)

	


	
		
		

	
