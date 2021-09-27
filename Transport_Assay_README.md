
**Transport Assay:** <br>
**Description:**<br>
Determines a series of intensity data based upon regions of an image (ROIs). Principally, this assay calculates the ratio of maximum intensity over average intensity. This is useful for determine transport rates of synchronizeable cargo and gathering associated corollary data such as mean or max intensity of an ROI across multiple channels.  

![image](Images/Transport_GUI.png)<br>

**Image Folder:** location of the image file to be assayed. Assigned automatically. <br>
**Processed Image Folder:** name of folder containing processed images. <br>
**Transport Output:** name of csv file containing ratiometric output <br>

------------------------------------------------------------------------------------------------------
**Mean Max Output:** name of csv file containing channel intensity output data. -optional <br>
**Transport channel:** channel where the ratio of maximum intensity over average intensity is determined. <br>
**Golgi channel:** channel the golgi apparatus is visible in. -optional.  <br>
**Zoom:** the level of zoom after selection of an image ROI. <br>
**View Mode:** Look Up Table (LUT) selection. <br>
**File Type:** extension of the image file type.  <br>
**Processed File Extension:** character added to the start of an image filename after its been processed. <br>
**ER Selection Radius:** radius of the circular ROI's used to determine average intensity of the ER. <br>

------------------------------------------------------------------------------------------------------

**Advanced Options:**--will occur if checked. <br>
**Always Select Golgi:** forces the user to manually determine the region that maximum intensity is derived from. <br>
**Mean Max Detection:** generates csv file, that records: Area, mean and max intensity of a selected ROI for all channels.  <br>
**Auto Position Image Window:** positions image window at the specified coordinates. <br>
**Always Auto-Detect Golgi:** automatically determines the maximum intensity of an ROI in the transport channel.  <br>
**Manual Background Selection:** forces the user to manually assign a background value. If unchecked lowest pixel intensities will be assigned automatically.   <br>

**ER-to-Golgi Transport Assay:** ER selection phase of selected ROI <br>

![image](Images/Transport_1.png)<br>

**ER-to-Golgi Transport Assay:** Transport Output csv <br>
![image](Images/Transport_2.png)<br>
**Cell:** ROI number assayed.<br>
**AVG_Max:** average of the top .01% of pixels in selected ROI.<br>
**bck_auto:** average of the bottom .1% of pixels in selected ROI.<br>
**bck:** manually selected background.<br>
**ER1:** average pixel intensity in the first selected circular ROI.<br>
**ER2:** average pixel intensity in the second selected circular ROI.<br>
**ER3:** average pixel intensity in the third selected circular ROI.<br>
**net_ER:** average of ER regions 1-3.<br>
**net_golgi:** AVG_Max-bck_auto.<br>
**T_index:** net_golgi/net_ER.<br>
**Image_title:** image that a particular ROI was derived from.<br> 

**ER-to-Golgi Transport Assay:** Mean Max Output csv<br>
![image](Images/Transport_3.png)<br>
**Cell:** ROI number assayed.<br>
**Cell Area:** area of selected ROI, determined by FIJI’s measure function.<br>
**ch1_Background:** minimum of selected ROI in channel 1. Determined by FIJI’s measure function.<br>
**ch1_avg:** mean of selected ROI in channel 1. Determined by FIJI’s measure function.<br>
**ch1_Maximum:** maximum of selected ROI in channel 1. Determined by FIJI’s measure function.<br>
……<br>
**Image_title:** image that a particular ROI was derived from. <br>



