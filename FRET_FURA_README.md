--Hay-Lab_plugins <br>

**FRET/FURA**<br>

Description: Calculates the ratio of multiple user defined ROI’s from a dual channel hyperstack (width, height, channels and time frames). <br>
![image](Images/ff_gui.png)<br>
**Output Location:** location of data output. <br>
**Processed Folder:** name of folder containing processed image (saves ROI overlay).<br>
**FRET FURA Outfile:** name of file containing ratio data for each ROI.<br>
**Selection Radius:** radius of ROI’s generated using the multi point tool.<br>
**Image Interval (sec):** number of seconds between each image interval. <br>
**ZeroDivisionErrorVal:** output when dividing by zero.<br>
**C1/C2(FURA):** if checked ROI ratio is channel 1 /channel 2.<br>
**C2/C1(FRET):** if checked ROI ratio is channel 2 /channel 1.<br>
**Apply Gaussian blur? Input sigma value:** apply a gaussian blur function prior to data aquistiion.<br>
**Set RO range (timepoint position x1 to x2):** range of channels used to determine the baseline ratio (R0)<br>
**Set Output file headers:** headers printed onto an csv file. <br>

**FRET FURA: ROI selection phase** <br>
![image](Images/ff_1.png)<br>
**FRET FURA: Output:**<br>
![image](Images/ff_2.png)<br>

**Image_title:** image that all ROI’s were derived from. <br>
**Time_min:** time in minutes after acquisition of repeating sets of dual channels.<br>
**ch1_bck:** background of channel 1.<br>
**ch2_bck:** background of channel 2.<br>
**Ch1_(n):**  average intensity of pixels within ROI ‘n’ in channel 1.<br>
**Ch2_(n):**  average intensity of pixels within ROI ‘n’ in channel 2.<br>
**C1_C2_(n):** Ch1_(n) / Ch2_(n).<br>
**R_R0_(n):** (Ch1_(n) / Ch2_(n)) / average intensity of pixels of ROI ‘n’ amassed from positions defined by the R0 range (above).<br>

