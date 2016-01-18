#=================================================================================================================
# Structure of PyjAmaseis 
#
# - IMPORTS
# - STATION INFORMATION USER INTERFACE CODE (class myFrame4)
# - SECONDARY OPTIONS UI WINDOW CODE (class selectionWindow)
# - CODE FOR FRAME WHICH APPEARS AT BOTTOM OF PLOTTING WINDOW (class lowerFrame)
# - DATA SELECTION AND EXTRACTION CODE (class dataHandler)
# - INITIALIZATION OF PLOTTING CODE (class Plotting)
# - CLASS FOR HANDLING TK FRAMES WHICH MUST BE IN MAIN THREAD (class mFrame)
# - alignToBottomRight Function - aligns secondary window to bottom right hand corner of screen
# - secondaryWindow Function - creates the Options window
# - Collecting Function - collects and process data read from the TC1
# - plotPrevious Function - loads and plots pre-recorded data
# - saveHourData Function - saves data recorded by TC1
# - getSerialPort Function - finds the serial port the TC1 is connected to
# - serial_ports Functions - returns all active serial ports
# - initializeHeader Function used to create a header object for headers in a SAC object
# - plotData - called by the Plotting function to plot data
# - calculateYAxisLabels - creates 24 hour UTC labels for the y axis, these are saved in an array
# - calculateYAxisLabelsOneHour - creates y axis labels for the current hour in UTC divided into 5 minute sections
# - xAxisLabels Function - Creates the labels which appear on the x axis of teh plottting window
# - window_close Function - causes the collecting and plotting processes to stop before closing windows
# - directory_handler Function - checks for a directory or creates a new one
# - getHourData Function - looks for an loads previously recorded data
# - if __name__ == '__main__': - the is where the code starts
#
#=================================================================================================================

### Importing all required libraries for running PyjAmaseis
### v1.0 change: The cross-platform screenshot module pyscreenshot is imported instead of the PIL module ImageGrab
### which is Windows-only. Tkinter messagebox is also imported.
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import sys
import platform
import Tkinter as tk
import tkMessageBox as msgbx
import time as Time
import serial
from obspy import read, Trace, UTCDateTime
from obspy.core.stream import Stream
from obspy.core import AttribDict
from obspy.core.trace import Stats
import datetime as dt
from datetime import datetime
from decimal import *
from multiprocessing import Queue
import pyscreenshot
from threading import Thread
import wx
from pygeocoder import Geocoder
import os
import errno
import glob
import fileinput
import pycurl
import base64


#### Initial window presented to user when launching PyjAmaseis for the first time
#### This window will require the user to enter the station information which will be later used when saving SAC files
#### Class was auto generate by using wxGlade
class MyFrame4(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame4.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.iconFile = "icons/icon.ico"
        self.icon = wx.Icon(self.iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("logo.gif", wx.BITMAP_TYPE_ANY))
        self.label_4 = wx.StaticText(self, wx.ID_ANY, ("Station Information\n"))
        self.label_6 = wx.StaticText(self, wx.ID_ANY, ("Station ID:"))
        self.text_ctrl_2 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_7 = wx.StaticText(self, wx.ID_ANY, ("Station Name:"))
        self.text_ctrl_3 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_8 = wx.StaticText(self, wx.ID_ANY, ("Street Address:"))
        self.text_ctrl_4 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_5 = wx.StaticText(self, wx.ID_ANY, ("Geographic Coordinates\n"))
        self.label_9 = wx.StaticText(self, wx.ID_ANY, ("Longitude:"))
        self.text_ctrl_6 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_10 = wx.StaticText(self, wx.ID_ANY, ("Latitude:"))
        self.text_ctrl_7 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_11 = wx.StaticText(self, wx.ID_ANY, ("Elevation:"))
        self.text_ctrl_8 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.button_2 = wx.Button(self, wx.ID_ANY, ("Begin"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        self.Bind(wx.EVT_BUTTON, self.begin, id = self.button_2.Id)
        self.Bind(wx.EVT_TEXT, self.checkAddress, id = self.text_ctrl_4.Id)
        
        
    def checkAddress(self, e):
        ## This method makes calls to the get the geo coordinates of the entered address in the - street address field
        try:
            results = Geocoder.geocode(self.text_ctrl_4.GetValue())
            longitude, latitude = results[0].coordinates
            self.text_ctrl_6.SetValue(str(longitude))
            self.text_ctrl_7.SetValue(str(latitude))
            self.text_ctrl_8.SetValue(str(0.0))    
        except:
             pass
    def begin(self, e):

    	#### Station Information entered is saved into text file, everytime application is loaded, 
        #### the information stored in this file will be read and saved in memory for use when saving SAC files - 
        #### this information goes into the header files of SAC 
    	
        #writing user entered information to text file
        file = open("Station Information.txt", "w")
        file.write("Station ID:"+self.text_ctrl_2.GetValue()+"\n")
        file.write("Station Name:"+self.text_ctrl_3.GetValue()+"\n")
        file.write("Station Address:"+self.text_ctrl_4.GetValue()+"\n")
        file.write("Latitude:"+self.text_ctrl_6.GetValue()+"\n")
        file.write("Longitude:"+self.text_ctrl_7.GetValue()+"\n")
        file.write("Elevation:"+self.text_ctrl_8.GetValue()+"\n")
        file.write("DCShift:0"+"\n")
        file.close()
        self.Close()
        #close and exit mainloop
        

    def __set_properties(self):
        # begin wxGlade: MyFrame4.__set_properties
        self.SetTitle("PyjAmaseis v1.0")
        self.SetSize((804, 456))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.SetForegroundColour(wx.Colour(0, 0, 0))
        self.label_4.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 1, ""))
        self.label_5.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 1, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame4.__do_layout
        #--- Initial GUI setup. Creates a grid and button layout functionalities ---

        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10.Add(self.bitmap_1, 0, 0, 0)
        sizer_11.Add(self.label_4, 0, wx.LEFT | wx.TOP | wx.EXPAND, 5)
        sizer_13.Add(self.label_6, 1, wx.LEFT | wx.EXPAND, 5)
        sizer_13.Add(self.text_ctrl_2, 2, wx.RIGHT, 5)
        sizer_12.Add(sizer_13, 1, wx.EXPAND, 0)
        sizer_14.Add(self.label_7, 1, wx.LEFT | wx.EXPAND, 5)
        sizer_14.Add(self.text_ctrl_3, 2, wx.RIGHT | wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer_12.Add(sizer_14, 1, wx.EXPAND, 0)
        sizer_15.Add(self.label_8, 1, wx.LEFT | wx.EXPAND, 5)
        sizer_15.Add(self.text_ctrl_4, 2, wx.RIGHT, 5)
        sizer_12.Add(sizer_15, 1, wx.EXPAND, 0)
        sizer_11.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_11.Add(self.label_5, 0, wx.LEFT | wx.TOP | wx.EXPAND, 5)
        sizer_5.Add(self.label_9, 1, wx.LEFT, 5)
        sizer_5.Add(self.text_ctrl_6, 2, wx.RIGHT | wx.EXPAND, 5)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_6.Add(self.label_10, 1, wx.LEFT, 5)
        sizer_6.Add(self.text_ctrl_7, 2, wx.RIGHT | wx.EXPAND, 5)
        sizer_4.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_7.Add(self.label_11, 1, wx.LEFT, 5)
        sizer_7.Add(self.text_ctrl_8, 2, wx.RIGHT | wx.EXPAND, 5)
        sizer_4.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_11.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_11.Add(self.panel_1, 1, wx.EXPAND, 0)
        sizer_11.Add(self.button_2, 1, wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND | wx.ALIGN_RIGHT, 5)
        sizer_10.Add(sizer_11, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_10)
        self.Layout()
        self.Centre()
        # end wxGlade

# end of class MyFrame4

#### This class represents the secondary options window that is launching when the real time plotting of data begins
#### Signals are sent over a secondary queue that listens for when the user wants to change between a 24 Hour plot to a 1 hour plot
#### A Y Shift is also signaled to shift the graph up or down on the y axis
#### Class was auto generate by using wxGlade
class selectionWindow(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: SecondaryWindow.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, None, wx.ID_ANY, "", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.iconFile = "icons/icon.ico"
        self.icon = wx.Icon(self.iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        
        #For Plotting Options
        self.label_2 = wx.StaticText(self, wx.ID_ANY, ("Plotting Options: "), style=wx.ALIGN_LEFT)
        self.button_3 = wx.Button(self, wx.ID_ANY, ("24 Hour Plotting"))
        self.panel_3 = wx.Panel(self, wx.ID_ANY)
        self.button_4 = wx.Button(self, wx.ID_ANY, ("1 Hour Plotting"))
        self.panel_4 = wx.Panel(self, wx.ID_ANY)
        self.spin_button_1 = wx.SpinButton(self, wx.ID_ANY , style=wx.SP_VERTICAL)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, ("Graph Shift"), style=wx.ALIGN_CENTRE)
        self.panel_5 = wx.Panel(self, wx.ID_ANY)
        
        #For dividing lines
        self.div_lin1 = wx.StaticLine(self, -1, size=(3,210),style=wx.LI_VERTICAL)
        
        #For Data Options
        self.dat_label = wx.StaticText(self, wx.ID_ANY, ("Data Options: "), style=wx.ALIGN_LEFT)
        self.extract_button = wx.Button(self, wx.ID_ANY, ("Extract Data"))
        self.extract_button.Disable()
        self.dataAccess = None
        self.hourData = None
        self.extrSaveOnly = wx.RadioButton(self, wx.ID_ANY, label='Save Selection',style=wx.RB_GROUP)
        self.extrDisplayOnly = wx.RadioButton(self, wx.ID_ANY, label='Display Selection')
        self.extrBoth = wx.RadioButton(self, wx.ID_ANY, label='Save and Display\nSelection')
        self.display_button = wx.Button(self, wx.ID_ANY, ("Display Data\n    from File"))
        
        
        #Bindings of buttons and boxes
        self.Bind(wx.EVT_BUTTON, self.twentyFourHourPlot, id = self.button_3.Id)
        self.Bind(wx.EVT_BUTTON, self.oneHourPlot, id = self.button_4.Id)
        self.Bind(wx.EVT_SPIN_UP, self.graphMoveUp, id = self.spin_button_1.Id)
        self.Bind(wx.EVT_SPIN_DOWN, self.graphMoveDown, id = self.spin_button_1.Id)
        self.Bind(wx.EVT_BUTTON, self.extractData, id = self.extract_button.Id)
        self.Bind(wx.EVT_BUTTON, self.displayData, id = self.display_button.Id)
        self.Bind(wx.EVT_CLOSE, self.doNothingIfExitButtonPressed)
        self.Bind(wx.EVT_MAXIMIZE, self.doNothingIfExitButtonPressed)
        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def doNothingIfExitButtonPressed(self,e):
        a=5

    def close(self):
        self.Destroy()

    def twentyFourHourPlot(self, e):
        #Send signal via queue 2 to the collecting process to inform the plotting process to re adjust the axis to show 24 hour
        queue2.put("24-Hour-Plot")
        
    
    def oneHourPlot(self, e):
        #Send signal via queue 2 to the collecting process to inform the plotting process to re adjust the axis to show 1 hour
        queue2.put("1-Hour-Plot")
    
    def graphMoveUp(self, e):
        #Send signal via queue 2 to the collecting process to change the dcshift value
        queue2.put("UP")
    
    def graphMoveDown(self, e):
        #Send signal via queue 2 to the collecting process to change the dcshift value
        queue2.put("DOWN")
    
    #This method is the main method which handles collecting and saving a region of data which has been selected by dataHandler. It is invoked
    #when Extract Data button is pressed. It gets the start and end times of the selection, finds how many hours are included, builds a list of directories
    #where this data exists (or gets it from hourSeismicData via the 'now' marker), then puts all this data in an array which is saved in a .sac file
    #Note that this method only supports selection intervals which include up to a maximum of 24 hours.
    def extractData(self, e):
        global stationId, mainWin
        if self.dataAccess != None:
            start = self.dataAccess.initialTime
            end = self.dataAccess.endTime
            interval  = end[1]-start[1]
            if interval < 0:
                interval = interval+24
            interval += 1   #Total number of hours selected  (where an hour is counted even if only part of it is selected)
            directoryList = []
            for hour in range(int(start[1]), int(start[1]+interval)):
                if hour < 24:
                    year, month, day = start[0].year, start[0].month, start[0].day
                else:
                    year, month, day, hour = end[0].year, end[0].month, end[0].day, hour-24
                timeTuple = (int(year), int(month), int(day), int(hour))
                if len(str(hour)) < 2:
                    hour =  '0'+str(hour)
                if len(str(day)) < 2:
                    day =  '0'+str(day)
                if len(str(month)) < 2:
                    month =  '0'+str(month) 
                directory = [timeTuple, stationId+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(year)[-2:]+str(month)+str(day)+str(hour)+stationId+'.sac']
                directoryList.append(directory)
            
            now = datetime.utcnow()
            for i in range(len(directoryList)):
                if not os.path.exists(directoryList[i][1]):
                    if (end[0].year, end[0].month, end[0].day, end[1]) == (now.year, now.month, now.day, now.hour):
                        directoryList[i][1] = 'now'
                    else:
                        msgbx.showerror("Error", "Some or all of the selected time\ndoes not have recorded data. Please\nselect a region of time which has\ncontinuous data.")
                        return
                elif directoryList[i][0] == (int(now.year), int(now.month), int(now.day), int(now.hour)):
                    directoryList[i][1] = directoryList[i][1] + 'now'
            
            hourSeisDat, hourTime = self.hourData[0], self.hourData[1]
            extrxtData, tot_time = np.array([], dtype=np.float64), 0
            for i in range(len(directoryList)):
                if i == 0:
                    if directoryList[i][1][-3:] != 'now':
                        trace = read(pathname_or_url = directoryList[0][1], format = 'SAC')
                        trace = trace.pop(0)
                        trace_dat = trace.data
                        extrxtData = np.concatenate((extrxtData, trace_dat[int(start[2]*len(trace_dat)):]))
                        tot_time += 3600-start[2]*3600
                    else:
                        total_time = hourTime.minute*60+hourTime.second+hourTime.microsecond/1000000.0
                        start_index = int(start[2]*3600/total_time*len(hourSeisDat))
                        end_index = int(end[2]*3600/total_time*len(hourSeisDat))
                        print 'Ind', start_index, end_index
                        if len(directoryList[i][1]) > 3:
                            trace = read(pathname_or_url = directoryList[0][1][:-3], format = 'SAC')
                            trace = trace.pop(0)
                            hourSeisDat = np.concatenate((trace.data, hourSeisDat))            
                        extrxtData = np.concatenate((extrxtData, hourSeisDat[start_index:end_index]))
                        tot_time += (end[2]-start[2])*3600
                elif i != len(directoryList)-1:
                    trace = read(pathname_or_url = directoryList[i][1], format = 'SAC')
                    trace = trace.pop(0)
                    trace_dat = trace.data
                    extrxtData = np.concatenate((extrxtData, trace_dat[:]))
                    tot_time += 3600
                elif i == len(directoryList)-1:
                    if directoryList[i][1][-3:] != 'now':
                        trace = read(pathname_or_url = directoryList[i][1], format = 'SAC')
                        trace = trace.pop(0)
                        trace_dat = trace.data
                        extrxtData = np.concatenate((extrxtData, trace_dat[:int(end[2]*len(trace_dat))]))
                    else:
                        total_time = hourTime.minute*60+hourTime.second+hourTime.microsecond/1000000.0
                        end_index = int(end[2]*3600/total_time*len(hourSeisDat))
                        if len(directoryList[i][1]) > 3:
                            trace = read(pathname_or_url = directoryList[0][1][:-3], format = 'SAC')
                            trace = trace.pop(0)
                            hourSeisDat = np.concatenate((trace.data, hourSeisDat)) 
                        extrxtData = np.concatenate((extrxtData, hourSeisDat[:end_index]))
                    tot_time += end[2]*3600
                   
            latitude, longitude, elevation = self.hourData[2][0], self.hourData[2][1], self.hourData[2][2]
            sampling_rate = len(extrxtData)/tot_time
            stats = initializeHeader(longitude, latitude , elevation, start[0])
            stats.npts = len(extrxtData)
            stats.sampling_rate = sampling_rate
            stats.delta = 1/sampling_rate
            st = Stream(Trace(data=extrxtData, header=stats))
            self.dataAccess.dataDeselector('resize')
            
            if self.extrSaveOnly.GetValue() or self.extrBoth.GetValue():
                filename = self.file_dialog('save', start[0], end[0])
                st.write(filename, format='SAC')
            if self.extrDisplayOnly.GetValue() or self.extrBoth.GetValue():
                queue3.put(st)
                tkframes.data_ready()
                

    #Method for handling the file saving dialog box when data is extracted (13/01/16)
    def file_dialog(self, mode, start=None, end=None):
        if mode == 'save':
            start = str(start.year)+'-'+str(start.month)+'-'+str(start.day)+'-'+str(start.hour)+'.'+str(start.minute)+'.'+str(round(start.second,2))
            end = str(end.year)+'-'+str(end.month)+'-'+str(end.day)+'-'+str(end.hour)+'.'+str(end.minute)+'.'+str(round(end.second,2))
            fileBrowser = wx.FileDialog(self, 'Select Location to Save Data', os.path.expanduser('~'), start+'_to_'+end+'.sac', 'SAC files (*.sac)|*.sac', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        elif mode == 'open':
            fileBrowser = wx.FileDialog(self, 'Select Data File to Display', os.path.expanduser('~'), '', 'SAC files (*.sac)|*.sac', wx.FD_OPEN)
        fileBrowser.ShowModal()
        path = fileBrowser.GetPath()
        if mode == 'save' and path[-4:] != '.sac':
            path += '.sac'
        return path
    
    def displayData(self, e=None):
        pathName = self.file_dialog('open')
        stream = read(pathname_or_url = pathName, format = 'SAC')
        queue3.put(stream)
        tkframes.data_ready()
        
    
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(("Options"))
        self.SetSize((325, 240))
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.panel_3.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.panel_4.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.panel_5.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.label_2.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.dat_label.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.extrSaveOnly.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL,  0, ""))
        self.extrDisplayOnly.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL,  0, ""))
        self.extrBoth.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL,  0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        #Main Sizer
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)  
        
        #Plotting Options
        sizer_2 = wx.BoxSizer(wx.VERTICAL)     
        sizer_2a = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2b = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add((4,6), 0, wx.EXPAND, 0)
        sizer_2a.Add(self.label_2, 1, wx.ALIGN_CENTER_VERTICAL, 8)
        sizer_2.Add(sizer_2a, 0, wx.LEFT, 9)
        sizer_2.Add((4,10), 0, wx.EXPAND, 0)
        sizer_2.Add(self.button_3, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 8)
        sizer_2.Add(self.panel_3, 1, wx.EXPAND, 0)
        sizer_2.Add(self.button_4, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 8)
        sizer_2.Add(self.panel_4, 1, wx.EXPAND, 0)
        sizer_2b.Add(self.spin_button_1, 2, wx.LEFT | wx.EXPAND, 20)
        sizer_2b.Add(self.label_1, 4, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(sizer_2b, 1, wx.EXPAND, 0)
        sizer_2.Add(self.panel_5, 1, wx.EXPAND, 0)
        
        #First dividing line
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL) 
        sizer_3.Add(self.div_lin1, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        
        #Data Options
        sizer_4 = wx.BoxSizer(wx.VERTICAL)     
        sizer_4a = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add((4,6), 0, wx.EXPAND, 0)
        sizer_4a.Add(self.dat_label, 1, wx.ALIGN_CENTER_VERTICAL, 8)
        sizer_4.Add(sizer_4a, 0, wx.LEFT, 3)
        sizer_4.Add((4,6), 0, wx.EXPAND, 0)
        sizer_4.Add(self.extrSaveOnly, 0, wx.LEFT | wx.RIGHT, 0)
        sizer_4.Add(self.extrDisplayOnly, 0, wx.LEFT | wx.RIGHT, 0)
        sizer_4.Add(self.extrBoth, 0, wx.LEFT | wx.RIGHT, 0)
        sizer_4.Add((4,5), 0, wx.EXPAND, 0)
        sizer_4.Add(self.extract_button, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        sizer_4.Add((4,20), 0, wx.EXPAND, 0)
        sizer_4.Add(self.display_button, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        
        #Putting everything in main sizer
        sizer_1.Add((4,1), 0, wx.EXPAND, 0) 
        sizer_1.Add(sizer_2, 5, wx.RIGHT | wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 1, wx.RIGHT | wx.EXPAND, 0)
        sizer_1.Add(sizer_4, 5, wx.RIGHT, 2)
        sizer_1.Add((4,1), 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade
        

### Class to handle the frame which appears at the bottom of the main plotting window. New v2.0 (18/12/15).
class lowerFrame():
    def __init__(self, master):
        bckgrnd = '#E6E6E6'
        self.frame = tk.Frame(master, bd=1, relief='sunken', bg=bckgrnd)
        time_label = tk.Label(self.frame, text='Current Time: ', bg=bckgrnd)
        time_label.pack(side='left', pady=1, padx=4)
        self.currentLabel = tk.Label(self.frame, text="", bg=bckgrnd)
        self.currentLabel.pack(side='left', pady=1)
        self.mouselocLabel = tk.Label(self.frame, text=" "*20, bg=bckgrnd)
        self.mouselocLabel.pack(side='right', pady=1, padx=4)
        loc_time_label = tk.Label(self.frame, text='Time at mouse location: ', bg=bckgrnd)
        loc_time_label.pack(side='right', pady=1)
        self.mode = "24-Hour-Plot"   #Changed in plotData when mode is changed. Makes it easy to tell mode when mouse_move is called.
        self.firstHour = datetime.utcnow()
    
    ##Function to display the time at the mouse location on the plot. THis is called when the mouse is moved over the plot (see mpl_connect binding of fig in Plotting). (18/12/15)
    def mouse_move(self, event, graph_constant):
        x_pos, y_pos, time = event.xdata, event.ydata, False
        if x_pos and y_pos and self.mode == "24-Hour-Plot":
            hour = 23-int(((y_pos-32750)+graph_constant/2)//graph_constant)
            hour = hour+self.firstHour.hour
            if hour > 23:
                hour = hour-24
            if (y_pos+graph_constant-32750) < (graph_constant/2):
                hour = hour-1
            elif (y_pos+graph_constant-32750) > graph_constant*24+(graph_constant/2):
                hour = hour+1
            minute = int(x_pos)
            second = round((x_pos%1)*60, 4)
            time = True
        elif x_pos and y_pos and self.mode == "1-Hour-Plot":
            hour = self.firstHour.hour
            minute = int(x_pos)+(11-int(((y_pos-32750)+graph_constant/2)//graph_constant))*5
            if (y_pos+graph_constant-32750) < (graph_constant/2):
                minute = minute-5
            elif (y_pos+graph_constant-32750) > graph_constant*12+(graph_constant/2):
                minute = minute+5
            second = round((x_pos%1)*60, 4)
            time = True
        if time:
            hour, minute, second = str(hour), str(minute), str(second)
            if int(hour) < 10:
                hour = '0'+hour
            if int(minute) < 10:
                minute = '0'+minute
            if float(second) < 10:
                second = '0'+second
            if len(str(second)) < 7:
                second = second + '0'*(7-len(second))
            time = hour+':'+minute+':'+second
            self.mouselocLabel.config(text=time)
        if not x_pos and not y_pos:
            self.mouselocLabel.config(text='Not Available')
            

### Class responsible for data selection and extraction and associated bindings  (05/01/16)
class dataHandler():
    def __init__(self, fig, ax, graphHeightConst, mode_getter_class):
        self.fig = fig
        self.canvas = fig.canvas
        self.ax = ax
        self.pressId = self.canvas.mpl_connect('button_press_event', self.dataSelector)
        self.graphHeightConst = graphHeightConst
        self.mode_getter = mode_getter_class
        self.activeSelection=False
        self.hourAccess = None
        self.hourData = None
        self.displayItems = None
    
    def dataSelector(self, event):
        global options_window
        if event.button == 1:
            x_dat_pos, y_dat_pos = event.xdata, event.ydata
            x_pixel, y_pixel = event.x, event.y   #Measured from bottom left hand corner of TkAgg Canvas.
            if x_dat_pos and y_dat_pos:
                self.mode = mode = self.mode_getter.mode
                data_buffer = self.data_buffer(y_dat_pos)
                self.initialTime = self.findTime(x_dat_pos, y_dat_pos, data_buffer)
                now, then = datetime.utcnow(), self.initialTime[0]
                if then < now:
                    self.activeSelection=True
                    options_window.extract_button.Enable()
                    bbox = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
                    width, height = bbox.width*self.fig.dpi, bbox.height*self.fig.dpi
                    if mode == "24-Hour-Plot":
                        self.frame_height = height/25
                        self.plot_width = width/60
                        self.mode_no = 60
                    elif mode == "1-Hour-Plot":
                        self.frame_height = height/13
                        self.plot_width = width/5
                        self.mode_no = 5

                    self.window_height = self.canvas._tkcanvas.winfo_height()
                    self.originalx = x_pixel
                    self.original_xdat = x_dat_pos
                    self.originaly = self.window_height-y_pixel-(self.frame_height/self.graphHeightConst*data_buffer)  #self.frame_height/self.graphHeightConst is pixels/data
                    self.initialTime = self.findTime(x_dat_pos, y_dat_pos, data_buffer)
                    self.drawFrame()
                    self.moveId = self.canvas.mpl_connect('motion_notify_event', self.resizeFrame)
                    self.releaseId = self.canvas.mpl_connect('button_release_event', self.dataExtractor)

    #Function to find the times which correspond to the ends of the selection area
    def findTime(self, x_dat_pos, y_dat_pos, data_buffer):
        time = []
        if self.mode == "24-Hour-Plot":
            hour = 23-((y_dat_pos+data_buffer-self.graphHeightConst/4-32750)//self.graphHeightConst)+self.hourAccess.firstHour.hour
            date = self.hourAccess.firstHour
            if hour>23:
                hour = hour-24
                date = self.hourAccess.firstHour + dt.timedelta(days=1)
            minute = (int(x_dat_pos)*60+(x_dat_pos%1*60))/3600    #Decimal fraction of hour where initial selection is
            time.append(datetime(date.year, date.month, date.day, int(hour), int(minute*60), int(minute*3600)-int(minute*60)*60, int(minute*3600000000)-int(minute*3600)*1000000))
            time.append(hour)
            time.append(minute)
        elif self.mode == "1-Hour-Plot":    
            minute = ((11-((y_dat_pos+data_buffer-self.graphHeightConst/4-32750)//self.graphHeightConst))*5*60+(x_dat_pos//1*60+(x_dat_pos%1*60)))/3600   #Decimal fraction of hour where initial selection is
            date = self.hourAccess.firstHour
            time.append(datetime(date.year, date.month, date.day, date.hour, int(minute*60), int(minute*3600)-int(minute*60)*60, int(minute*3600000000)-int(minute*3600)*1000000))
            time.append(self.hourAccess.firstHour.hour)
            time.append(minute)
        return time
                
    
    #This function is the primary function for matching the selection area to where the mouse is moved. The selection area is drawn from 1-pixel thick
    #frames. There is either four frames (for one line selections), or eight (for multiple line selection--extras are initiated and included in self.extra_frames)
    #Several refernce points are established in the make_extra_frames function (the x-pixel for the left of the plot, and the left and right distances to the
    #edge of the plot from the original position where the selection was first started). As the mouse is moved, the frames are configured (in size and position).
    
    def resizeFrame(self, event):
        x_pixel, y_pixel = event.x, event.y
        x_dat_pos, y_dat_pos, newy = event.xdata, event.ydata, None
        x_win, y_win = mainWin.winfo_rootx(), mainWin.winfo_rooty()
        if y_dat_pos:
            newy = self.window_height-y_pixel-(self.frame_height/self.graphHeightConst*self.data_buffer(y_dat_pos))
            if self.findTime(x_dat_pos, y_dat_pos, self.data_buffer(y_dat_pos))[0] < datetime.utcnow():
                if x_dat_pos and self.originaly < self.window_height-y_pixel < self.originaly+self.frame_height:   #For selection of one line of the trace only
                    self.currentEndy = y_dat_pos
                    self.currentEndx = x_dat_pos
                    self.clear_extras()
                    self.leftVert.config(height = self.frame_height+1)
                    self.rightVert.config(height = self.frame_height+1)
                    if x_pixel > self.originalx:
                        self.rightVert.place_configure(x = x_pixel, y = self.originaly)
                        self.topHoriz.config(width = x_pixel-self.originalx)
                        self.botHoriz.config(width = x_pixel-self.originalx)      
                        self.botHoriz.place_configure(anchor = 'nw', y=self.originaly+self.frame_height,x=self.originalx)
                        self.topHoriz.place_configure(anchor = 'nw', x=self.originalx, y=self.originaly)
                    elif x_pixel < self.originalx:
                        self.rightVert.place_configure(x = x_pixel, y = self.originaly)
                        self.topHoriz.config(width = self.originalx-x_pixel)
                        self.botHoriz.config(width = self.originalx-x_pixel)           
                        self.botHoriz.place_configure(anchor = 'ne', y=self.originaly+self.frame_height, x=self.originalx)
                        self.topHoriz.place_configure(anchor = 'ne', y=self.originaly, x=self.originalx)
                elif x_dat_pos and (self.mode=='24-Hour-Plot' and 32750-self.graphHeightConst/2<y_dat_pos<32750+self.graphHeightConst*24-self.graphHeightConst/2)\
                or (self.mode=='1-Hour-Plot' and 32750-self.graphHeightConst/2<y_dat_pos<32750+self.graphHeightConst*12-self.graphHeightConst/2):        #For selection of multiple lines of the trace.
                    try:
                        if self.extra_frames:
                            pass
                    except:
                        self.extra_frames = self.make_extra_frames()
                    self.currentEndy = y_dat_pos
                    self.currentEndx = x_dat_pos
                    side_height = abs(self.originaly-newy)
                    frames = self.extra_frames
                    self.leftVert.config(height = self.frame_height)  #Height of verticals has to be reduced by one for an unknown reason
                    self.rightVert.config(height = self.frame_height)
                    if newy > self.originaly:
                        self.rightVert.place_configure(x = x_pixel, y = newy)
                        self.topHoriz.config(width = self.to_right_width)
                        self.botHoriz.config(width = self.to_left_width+(x_pixel-self.originalx))      
                        self.botHoriz.place_configure(anchor = 'nw', y = newy+self.frame_height-1, x = self.left_of_plot)
                        self.topHoriz.place_configure(anchor = 'nw', x=self.originalx, y=self.originaly)
                        frames[2].config(width = self.to_left_width)
                        frames[3].config(width = self.to_right_width-(x_pixel-self.originalx), bg = 'red')  
                        frames[0].config(height=side_height), frames[1].config(height=side_height)
                        frames[0].place_configure(anchor = 'nw', x = self.left_of_plot, y = self.originaly+self.frame_height)
                        frames[1].place_configure(anchor = 'ne', x = self.left_of_plot+self.mode_no*self.plot_width, y = self.originaly)
                        frames[2].place_configure(anchor = 'nw', x = self.left_of_plot, y = self.originaly+self.frame_height-1)
                        frames[3].place_configure(anchor = 'nw', x = x_pixel, y = newy)
                    elif newy < self.originaly:
                        self.rightVert.place_configure(x = x_pixel, y = newy)
                        self.topHoriz.config(width = self.to_right_width-(x_pixel-self.originalx))
                        self.botHoriz.config(width = self.to_left_width)           
                        self.botHoriz.place_configure(anchor = 'ne', y=self.originaly+self.frame_height-1, x=self.originalx)
                        self.topHoriz.place_configure(anchor = 'ne', y = newy, x = self.left_of_plot+self.mode_no*self.plot_width)   
                        frames[2].config(width = self.to_left_width+(x_pixel-self.originalx), bg = 'red')
                        frames[3].config(width = self.to_right_width, bg = 'red')
                        frames[0].config(height=side_height), frames[1].config(height=side_height)
                        frames[0].place_configure(anchor = 'nw', x = self.left_of_plot, y = newy+self.frame_height)
                        frames[1].place_configure(anchor = 'ne', x = self.left_of_plot+self.mode_no*self.plot_width, y = newy)
                        frames[2].place_configure(anchor = 'nw', x = self.left_of_plot, y = newy+self.frame_height-1)
                        frames[3].place_configure(anchor = 'nw', x = self.originalx, y = self.originaly)
        
    
    def clear_extras(self):
        try:
            for widget in self.extra_frames:
                tkframes.destroy(widget)
            del self.extra_frames
        except:
            pass
     
    
    def make_extra_frames(self):
        self.to_left_width = int(self.original_xdat*self.plot_width)
        self.to_right_width = int((self.mode_no-self.original_xdat)*self.plot_width)
        self.left_of_plot = np.ceil(self.originalx-self.original_xdat*self.plot_width)
        left_vert = tkframes.Frame(height = self.frame_height, width = 1, bg = 'red')
        right_vert = tkframes.Frame(height = self.frame_height, width = 1, bg = 'red')        
        top_to_left = tkframes.Frame(height = 1, width = 1, bg = 'red')
        bottom_to_right = tkframes.Frame(bg = 'red', height = 1, width = 1)
        bottom_to_right.place(), top_to_left.place(), right_vert.place(), left_vert.place()
        return (left_vert, right_vert, top_to_left, bottom_to_right)
    
    #Function which handles the mouse release event after the data area has been selected. From here, extraction and saving is handled in selectionWindow.
    def dataExtractor(self, event):
        global options_window
        if event.button == 1:
            self.canvas.mpl_disconnect(self.pressId)
            self.canvas.mpl_disconnect(self.moveId)
            self.deselectId = self.canvas.mpl_connect('button_press_event', self.dataDeselector)
            self.canvas.mpl_disconnect(self.releaseId)
            self.endTime = self.findTime(self.currentEndx, self.currentEndy, self.data_buffer(self.currentEndy))
        #Now that start and end times are established (the aim of this class), the data can be extracted and saved or displayed by the extracting and
        #saving functions in the selectionWindow class, which contains the button to initiate this task.
    
    #To clear selection on click (or otehr call such as resize or changing mode)
    def dataDeselector(self, event):
        global options_window, tkframes
        if self.activeSelection and (event == 'resize' or event.button == 1):
            self.clear_extras()
            try:
                for widget in self.selection_frame:
                    tkframes.destroy(widget)
                self.canvas.mpl_disconnect(self.deselectId)
                self.pressId = self.canvas.mpl_connect('button_press_event', self.dataSelector)
            except AttributeError:
                print 'Attribute Error Occurred'
            self.activeSelection = False
            options_window.extract_button.Disable()
    
    #Function to initiate the four 1-pixel width frames which make up the selection area. (Note extra frames initiated in make_extra_frames when required)    
    def drawFrame(self):
        global tkframes
        self.topHoriz = tkframes.Frame(height = 1, width = 3, bg = 'red')
        self.botHoriz = tkframes.Frame(height = 1, width = 3, bg = 'red')
        self.leftVert = tkframes.Frame(height = self.frame_height+1, width = 1, bg = 'red')
        self.rightVert = tkframes.Frame(height = self.frame_height+1, width = 1, bg = 'red')
        self.topHoriz.place(x = self.originalx, y = self.originaly)
        self.topHoriz.place(x = self.originalx, y = self.originaly)
        self.leftVert.place(x = self.originalx, y = self.originaly)
        self.botHoriz.place(x = self.originalx, y = self.originaly+self.frame_height-1)
        self.rightVert.place(x = self.originalx+3, y = self.originaly)
        self.selection_frame = (self.topHoriz, self.botHoriz, self.leftVert, self.rightVert)
    
    #For finding the difference (in terms of yaxis height, not pixels) between the clicked location and the next highest mid-point between traces.
    def data_buffer(self, y_dat_pos):
        if y_dat_pos:
            data_buffer = (np.ceil((y_dat_pos-32750)*2/self.graphHeightConst)*(self.graphHeightConst/2))
            mode = self.mode
            if data_buffer < 0:
                data_buffer = self.graphHeightConst/2
            elif mode == "24-Hour-Plot" and y_dat_pos > 23*self.graphHeightConst+32750:
                data_buffer = 23*self.graphHeightConst+self.graphHeightConst/2
            elif mode == "1-Hour-Plot" and y_dat_pos > 11*self.graphHeightConst+32750:
                data_buffer = 11*self.graphHeightConst+self.graphHeightConst/2
            elif data_buffer/self.graphHeightConst%1==0:
                data_buffer = data_buffer+self.graphHeightConst/2
            data_buffer = data_buffer+32750-y_dat_pos
            return data_buffer
        return None
        

###Initialization fo the main plotting window. This is a class which is called from the __main__ thread so that the mainloop() is in the main thread.
###Previously, this was the target for the plottingProcess thread, but the current architecture achieves the same plotting functionality (via root.after)
###while allowing for the mainloop of the plotting window to be in the main thread.
class Plotting():  
    def __init__(self, queue, queue2):
        global mainWin, plotting_loop, options_window
        
        looping = True
        while looping:
            if not queue.empty():
                value = queue.get()
                if value == "Start Plotting Process":
                    looping = False
            elif not plotting_loop:
                looping = False
                
        if plotting_loop:    #In case program has been closed before now (i.e. if no TC1 connected and user has selected to exit).
            timeNow = datetime.time(datetime.now())
            time = timeNow.minute + (timeNow.second + timeNow.microsecond/1000000.0)/60.0
            lastX = time
            lastY = 90250
            connect = True
            step = 0
            x=[]
            y=[]

            mode = "24-Hour-Plot"

            self.root = tk.Tk()
            mainWin = self.root
            mainWin.protocol("WM_DELETE_WINDOW", window_close)           #Closes options window and ends processes. New in v2.0.
            mainWin.wm_title("PyAmaseis v1.0")
            ### v1.0 change: Conditional added. .ico not supported on Linux. zoomed not 
            ### supported on linux.
            if platform.system() == 'Linux':
                mainWin.iconbitmap(r'@icons/icon1.xbm')
            else:
                mainWin.iconbitmap(r'icons/icon.ico')
                mainWin.wm_state('zoomed')

            graphHeightConst = 2500
            fig = plt.figure(figsize=(13,9))   #15,10

            # v1.0 change: AttributeError: 'Figure' object has no attribute 'set_tight_layout' on Linux
            if platform.system() != 'Linux':
                fig.set_tight_layout(0.4)

            ax = fig.add_subplot(1,1,1)
            ax.set_xlim(0,60)
            ax.set_ylim(30250,92750)
            ax.set_xlabel('Minute')
            ax.set_ylabel('Hour (UTC)')
            yAxis = [30250,92750]

            y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
            y2 = calculateYAxisLabels()

            ax = xAxisLabels(ax, 24)
            plt.yticks(y1, y2)
            ax.yaxis.grid(color = '#0000FF', linestyle = '-')
            ax.set_axisbelow(True)
            line, = ax.plot(x, y, color='k')
            canvas = FigureCanvasTkAgg(fig, master=mainWin)
            canvas._tkcanvas.config(highlightthickness=0)
            bottomFrame = lowerFrame(mainWin)
            bottomFrame.frame.pack(side='bottom', expand=1, fill = tk.BOTH)
            canvas._tkcanvas.pack(side=tk.TOP, expand=1, fill = tk.BOTH)
            canvas.draw()
            dataInteractive = dataHandler(fig, ax, graphHeightConst, bottomFrame)
            options_window.dataAccess = dataInteractive
            dataInteractive.hourAccess = bottomFrame
            self.displayItems = None
            dataInteractive.displayItems = self.displayItems
            fig.canvas.mpl_connect('motion_notify_event', lambda event: bottomFrame.mouse_move(event, graphHeightConst))
            mainWin.update_idletasks()
            geometry = mainWin.geometry()
            geometry = geometry[:geometry.find('+')]

            mainWin.after(0, plotData,queue, queue2, fig, ax, canvas, bottomFrame, mainWin, lastY, lastX, connect, line, mode, geometry, dataInteractive)
            

###Any tk Frames used in this program must originate from the __main__ thread. Hence, this class, which is only called from the __main__ thread, initiates a
###list of tk frames that can be used from other threads but still have their mainloops in the __main__ thread. The frames are mostly used in dataHandler.
class mFrame(tk.Frame):
    def __init__(self, queue3, root):
        tk.Frame.__init__(self)
        self.max_no = 20
        self.frames = []
        self.root = root
        for i in range(self.max_no):
            self.frames.append(tk.Frame(mainWin))
        self.frame_index = 0
        self.queue3 = queue3
        self.figureCount = 0
        self.windows = []
    
    def Frame(self, **kwargs):
        frame = self.frames[self.frame_index]
        self.frame_index+=1
        frame.config(**kwargs)
        return frame
    
    def destroy(self, widget):
        widget.destroy()
        index = self.frames.index(widget)
        del self.frames[index]
        self.frames.append(tk.Frame(mainWin))   
        self.frame_index = self.frame_index-1

    def data_ready(self):
        self.current_data = queue3.get()
        self.plot()
    
    def plot(self):
        if self.figureCount < 3:
            self.figureCount += 1
            window = tk.Toplevel(master=self.root)
            window.lower()
            self.windows.append(window)
            window.protocol("WM_DELETE_WINDOW", lambda: self.toplevel_close(window))
            if platform.system() == 'Linux':
                mainWin.iconbitmap(r'@icons/icon1.xbm')
            else:
                mainWin.iconbitmap(r'icons/icon.ico')
            window.title('Data Display')
            fig = matplotlib.figure.Figure()
            start = str(self.current_data[0].stats['starttime'])
            end = str(self.current_data[0].stats['endtime'])
            fig.suptitle("Data Extraction: "+start[:start.find('T')]+', '+start[start.find('T')+1:-1]+'\nto '+end[:end.find('T')]+', '+end[end.find('T')+1:-1])
            ax = fig.add_subplot(1,1,1)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            canvas = FigureCanvasTkAgg(fig, master=window)
            toolbarFrame = tk.Frame(window)
            toolbar = NavigationToolbar2TkAgg(canvas, toolbarFrame)
            toolbarFrame.pack(side=tk.BOTTOM, expand=1, fill = tk.BOTH)
            canvas._tkcanvas.pack(side=tk.TOP, expand=1, fill = tk.BOTH)
            self.current_data.plot(fig=fig)
            window.lift()
        else:
            msgbx.showinfo("Maximum Reached", "The maximum number of data displays has been reached. Close an open data display before proceeding.")

    def toplevel_close(self, window):
        deleted = False
        for i in range(len(self.windows)):
            if not deleted and self.windows[i] == window:
                self.windows[i].destroy()
                del self.windows[i]
                deleted = True
        self.figureCount = self.figureCount-1

#### This method aligns the Options window to the bottom right hand corner of the screen so it doesn't come in the way of plotting
def alignToBottomRight(win):
    dw, dh = wx.DisplaySize()
    w, h = win.GetSize()
    x = dw - w
    y = dh - h
    win.SetPosition((x-20, y-65))

#### This method creates the Options window
def secondaryWindow(queue2, queue3):
    global options_window       #New in v2.0.

    app = wx.App(False)
    options_window = selectionWindow()
    app.SetTopWindow(options_window)
    alignToBottomRight(options_window)
    options_window.Show()
    options_window.Raise()
    app.MainLoop()

#### This is the Collecting method (Thread) responsible for reading data from the TC1, sending this data via a queue to plotting thread/method, saving data into SAC, listening to commands from Options window, and uploading SAC files to NZSeis server after saving them
def Collecting(queue, queue2, queue3):
    global collecting_loop, stationId, options_window
    
    #Stats header information initialization
    stationId = 01
    stationName = 'Unknown'
    stationAddress = 'Unknown'
    longitude = 0.0
    latitude = 0.0
    elevation = 0.0
    dcShift = 0
    oldDCShift = 0
    
    #Check if user has already entered Station information, if yes, then go straight into 24 hour live plotting, if no create the initial station information input window
    if(os.path.exists('Station Information.txt') == False):
        app = wx.App(False)
        frame_5 = MyFrame4(None, wx.ID_ANY, "")
        app.SetTopWindow(frame_5)   
        frame_5.Center()
        frame_5.Show()
        app.MainLoop()

    else:

        pass
    
    #Once user has entered the station information and that information is saved into a txt file, it is read line by line by the following lines of code and is parsed to extract the data required or header information
    file = open("Station Information.txt", "r")
    informationArray = file.readlines()
    
    for line in informationArray:
        if "Station ID" in line:
            stationId = line[line.find(":")+1:line.find("\n")]
        if "Station Name" in line:
            stationName = line[line.find(":")+1:line.find("\n")]
        if "Station Address" in line:
            stationAddress = line[line.find(":")+1:line.find("\n")]
        if "Longitude" in line:
            longitude = line[line.find(":")+1:line.find("\n")]
        if "Latitude" in line:
            latitude = line[line.find(":")+1:line.find("\n")]
        if "Elevation" in line:
            elevation = line[line.find(":")+1:line.find("\n")]
        if "DCShift" in line:
            dcShift = int(line[line.find(":")+1::])
            
            oldDCShift = int(line[line.find(":")+1::])
    file.close()
    
    #initializing further required variables
    mode = "None"
    currentMode = "24Hour"
    graphHeightConst = 2500 #distance between each 1 hour plot on the 24 hour plot
    totalHoursConst = 23 #used to decrement the hour so that once the plot reaches the end of 24 hours the plot is cleared and plotting starts from the top
    skipConst = 1 #currently not used, but in place to skip reading values coming in from the TC1 - eg. if it is 2, then it will read every second value
    count = 0
    lastHour = datetime.time(datetime.now()).hour
    hasHourChanged = False
    plotLimit = graphHeightConst*7
    goldenNumber = 32750 #the center line of each plot, where it oscillates  - used to fix y axis according to this (32750 - graphHeightConstant which gives lower limit + graphHeightConstant * 25 (or how many ever hours gives upper limit))
    upperLim = 36000 #the top limit of each plot
    lowerLim = 28000 #bottom limit of each plot
    plotClear = False
    
    #hourMillisecondData = np.array([], dtype = np.float64)
    tempMillisecond = np.array([], dtype = np.float64)
    
    serialNumber = None 
    serialPort = None
    
    #Returns the serialPort that the TC1 is connected to
    serialPort = getSerialPort()
    
    #This while loop ensures user has connected the TC1 before continuing
    while serialPort == None:
        redundantRoot = tk.Tk()  #Parent for error dialog to display on top of. This is done so it can then be hidden and destroyed.
        redundantRoot.withdraw()
        yes_or_no =  msgbx.askokcancel(message="Please Connect TC-1 Seismometer", title="Error", parent=redundantRoot)
        redundantRoot.destroy()
        if yes_or_no:
            serialPort = getSerialPort()
        else:
            window_close(True)
            return

    serialPort = serial.Serial(serialPort)
    serialPort.flushInput()
    serialPort.flushOutput()
    
    #The following two lines create the secondary options window
    secondaryWindowProcess = Thread(target= secondaryWindow, args=(queue2,queue3,))
    secondaryWindowProcess.start()
    
    queue.put("Start Plotting Process")

    #create a stats object that holds all the station information retrieved from the txt file
    stats = initializeHeader(longitude, latitude , elevation)
    
    hourSeismicData, stats = getHourData(stats) #stores the data from the hour, populated with data from previous recordings in the hour or zeroes
    hourTimeData = np.array([], dtype = np.float64)
    tempSeismicData = np.array([]) #used to store 18 value read from the tc1 and sent is sent to the plotting array, then cleared for next 18 values
    
    queue.put(['prev', hourSeismicData, currentMode, 'None', graphHeightConst, dcShift, skipConst, stats])     #bad idea. change this becasue it will take too long, and the length of the data array will be too short by the time collecting process is started.
    
    while collecting_loop:
        try:
            #Checks whether the user has changed the view selection in the options window from 24 hour to 1 hour or has increased or decreased the graphShift
            if(queue2.empty() == False):
                readingQueue2 = queue2.get()
                if readingQueue2 == "24-Hour-Plot":
                    currentMode = "24Hour"
                    now = Time.time()
                    queue.put(['prev', hourSeismicData, currentMode, '24-Hour-Plot', graphHeightConst, dcShift, skipConst, stats])
                    totalHoursConst = 23
                    tempSeismicData = np.array([])
                    tempMillisecond = np.array([])

                if readingQueue2 == "1-Hour-Plot":
                    currentMode = "1Hour"
                    now = Time.time()
                    queue.put(['prev', hourSeismicData, currentMode, '1-Hour-Plot', graphHeightConst, dcShift, skipConst, stats])
                    tempSeismicData = np.array([])
                    tempMillisecond = np.array([])
                if readingQueue2 == "UP":
                    tempSeismicData = np.array([])
                    tempMillisecond = np.array([])
                    dcShift += 100 

                    for line in fileinput.input('Station Information.txt', inplace=True): 
                        print line.replace('DCShift:'+str(oldDCShift), 'DCShift:'+str(dcShift)),
                    oldDCShift = dcShift

                if readingQueue2 == "DOWN":
                    tempSeismicData = np.array([])
                    tempMillisecond = np.array([])
                    dcShift -= 100 

                    #Every time the user changes the graphshift - the value in against the graphShift header in the StationInformation.txt file is updated
                    for line in fileinput.input('Station Information.txt', inplace=True): 
                        print line.replace('DCShift:'+str(oldDCShift), 'DCShift:'+str(dcShift)),
                    oldDCShift = dcShift
                
            #Read from the TC1 seismometer. 
            #Causes problems if seismometer not connected properly or if python is run multiple times?? (09/12/15). See exception handler below.

            reading = int(serialPort.readline())
            timeNow = datetime.time(datetime.now())
            time = timeNow.minute + (timeNow.second + timeNow.microsecond/1000000.0)/60.0
            hourTime = timeNow.minute*60+timeNow.second + timeNow.microsecond/1000000.0
            hour = timeNow.hour 
            plotClear = False
            
            if currentMode == "24Hour":
                #Depending on the hour and viewMode which is 24 or 1 hour plotting, the data value that is read is translated to the appropriate height
                data = [int(reading+(graphHeightConst*totalHoursConst))+dcShift]

            if currentMode == "1Hour":
                minute = (datetime.time(datetime.now())).minute
                if minute < 5:
                    data = [int(reading+(graphHeightConst*11))+dcShift]
                if minute < 10 and minute >= 5:
                    data = [int(reading+(graphHeightConst*10))+dcShift]
                if minute < 15 and minute >= 10:
                    data = [int(reading+(graphHeightConst*9))+dcShift]
                if minute < 20 and minute >= 15:
                    data = [int(reading+(graphHeightConst*8))+dcShift]
                if minute < 25 and minute >= 20:
                    data = [int(reading+(graphHeightConst*7))+dcShift]
                if minute < 30 and minute >= 25:
                    data = [int(reading+(graphHeightConst*6))+dcShift]
                if minute < 35 and minute >= 30:
                    data = [int(reading+(graphHeightConst*5))+dcShift]
                if minute < 40 and minute >= 35:
                    data = [int(reading+(graphHeightConst*4))+dcShift]
                if minute < 45 and minute >= 40:
                    data = [int(reading+(graphHeightConst*3))+dcShift]
                if minute < 50 and minute >= 45:
                    data = [int(reading+(graphHeightConst*2))+dcShift]
                if minute < 55 and minute >= 50:
                    data = [int(reading+(graphHeightConst*1))+dcShift]
                if minute < 60 and minute >= 55:
                    data = [int(reading+(graphHeightConst*0))+dcShift]

            if (hour != lastHour):
                ## Everytime the hour changes the following code saves hour long SAC Files
                lastHour = hour
                fileName, stats, directory = saveHourData(stats, hourSeismicData, stationId,longitude, latitude , elevation)
                hourSeismicData = np.array([])
                hourTimeData = np.array([], dtype = np.float64)
                ##Uploads SAC file right after creating it

                contentType = "application/octet-stream" #image/png
                c = pycurl.Curl()
                c.setopt(c.URL, 'https://nzseis.phy.auckland.ac.nz/pyjamaseis/upload/')
                c.setopt(c.HTTPHEADER, ['Authorization:'+'Basic %s' % base64.b64encode("kofi:pyjamaseis")])
                c.setopt(c.HTTPPOST, [("payload",(c.FORM_FILE, directory+fileName, c.FORM_CONTENTTYPE, contentType)), ("mode","sac")])

                try:
                    c.perform()
                    c.close()
                except pycurl.error, error:
                    errno, errstr = error
                    print 'An error occurred: ', errstr


                totalHoursConst = totalHoursConst-1
                if(totalHoursConst == -1):
                    plotClear = True
                    totalHoursConst = 23

                hasHourChanged = True

            if ((count % skipConst == 0) or hasHourChanged):
                if ((tempSeismicData.size >= 18) or hasHourChanged):

                    ##After every 18 values are read from the TC1 seismometer, the array containing these values along with the tempMillisecond array which contains the exact time the value was read put on the queue for the plotting process to read
                    queue.put([tempSeismicData, tempMillisecond, hasHourChanged, plotClear, mode])
                    mode = "None"
                    #the arrays are cleared 
                    tempSeismicData = np.array([])
                    tempMillisecond = np.array([])
                    hasHourChanged = False
                    options_window.hourData = (hourSeismicData, datetime.utcnow(), (latitude,longitude,elevation))
                else:
                    if currentMode == "1Hour":

                        tempSeismicData = np.append(tempSeismicData,data)

                        if time < 5:
                            tempMillisecond = np.append(tempMillisecond,time)
                        elif time < 10:
                            tempMillisecond = np.append(tempMillisecond,time - 5)
                        elif time < 15:
                            tempMillisecond = np.append(tempMillisecond,time - 10)
                        elif time < 20:
                            tempMillisecond = np.append(tempMillisecond,time - 15)
                        elif time < 25:
                            tempMillisecond = np.append(tempMillisecond,time - 20)
                        elif time < 30:
                            tempMillisecond = np.append(tempMillisecond,time - 25)
                        elif time < 35:
                            tempMillisecond = np.append(tempMillisecond,time - 30)
                        elif time < 40:
                            tempMillisecond = np.append(tempMillisecond,time - 35)
                        elif time < 45:
                            tempMillisecond = np.append(tempMillisecond,time - 40)
                        elif time < 50:
                            tempMillisecond = np.append(tempMillisecond,time - 45)
                        elif time < 55:
                            tempMillisecond = np.append(tempMillisecond,time - 50)
                        elif time < 60:
                            tempMillisecond = np.append(tempMillisecond,time - 55)

                        hourSeismicData = np.append(hourSeismicData,reading)
                        hourTimeData = np.append(hourTimeData, hourTime)
                    else:
                        tempSeismicData = np.append(tempSeismicData,data)
                        tempMillisecond = np.append(tempMillisecond,time)
                        hourSeismicData = np.append(hourSeismicData,reading)
                        hourTimeData = np.append(hourTimeData, hourTime)

            count += 1         
        except:
            #Exception handler for seismometer connection error mentioned above. (09/12/15)
            exc_type = sys.exc_info()[0]
            if str(exc_type).find('SerialException') != -1:
                msgbx.showerror("Error", "PyjAmaSeis has detected a seismometer connection error.\nPlease exit PyjAmaSeis and reconnect seismometer.")
                window_close()
            else:
                print exc_type
    
    queue.put((stats, hourSeismicData, stationId, longitude, latitude , elevation, hourTimeData))  #saves data when program closes.
    
    return                  

##This function is responsible for plotting data whcih is pre-loaded and has not been read from the seismometer in real-time. (11/12/15)
def plotPrevious(hour_data=None, currentMode=None, mode=None, graphHeightConst=None, dcShift=None, skipConst=None, stats=None):
    data_array = hour_data
    delta = stats['delta']
    if currentMode == "24Hour":
        data_array = data_array+(graphHeightConst*23+dcShift)
        time_array = np.arange(0,len(data_array))*delta/60
        queue.put([data_array, time_array, False, False, mode])
    if currentMode == "1Hour":
        tot_length = 0
        for i in range(12):
            i = i+1
            if ((i)*300/delta) <= len(data_array):
                data = np.array(data_array[tot_length:int(((i)*300/delta))])+(graphHeightConst*(12-i))+dcShift
                time_array = np.arange(0,5,delta/60)   #Want one less than 5
                if len(time_array) == len(data)+1:
                    time_array = time_array[:len(data)] 
                if tot_length == 0:    
                    queue.put([data, time_array, False, False, "1st-1-Hour-Plot"])
                else:
                    queue.put([data, time_array, False, False, mode])
                tot_length += len(data)
            elif ((i-1)*300/delta) <= len(data_array):
                data = np.array(data_array[int(((i-1)*300/delta)):])+(graphHeightConst*(12-i))+dcShift
                if i != 1: 
                    time_array = np.arange(0,(len(data_array)-tot_length))*delta/60
                else:
                    time_array = np.arange(0,len(data_array))*delta/60
                    mode = "1st-1-Hour-Plot"
                if len(time_array) == len(data)+1:
                    print len(time_array), len(data)
                    time_array = time_array[:len(data)]                
                queue.put([data, time_array, False, False, mode])

##This function (newv2.0) saves the seismic data from the hour. (11/12/15)
def saveHourData(stats, hourSeismicData, stationId, longitude, latitude , elevation):
    now = UTCDateTime()
    diff = now-stats['starttime']
    sampling_rate = len(hourSeismicData)/diff
    delta = 1/sampling_rate
    
    stats['ntps'] = len(hourSeismicData)
    stats['sampling_rate'] = sampling_rate
    stats['delta'] = delta
    st = Stream([Trace(data=hourSeismicData, header=stats)])
    print 'Start:', stats['starttime'], 'End:', now, 'Length:', len(hourSeismicData)
    
    sacdateAndTime = str(stats['starttime']).split('T')
    sacdate =  sacdateAndTime[0].split('-')
    sactime =  sacdateAndTime[1].split(':')
    sacyear  = sacdate[0][2:]
    sacmonth = sacdate[1]
    sacday = sacdate[2]
    sachour = sactime[0]
    fileName = str(sacyear+sacmonth+sacday+sachour+stats['station']+".sac")   #v1.0 change. Removed minute from filename.
    directory = stationId+'/'+str(sacdate[0])+'/'+sacmonth+'/'+sacday+'/'
    directory_handler(directory)
    st.write(directory+fileName, format='SAC')
    stats = initializeHeader(longitude, latitude , elevation)
    return fileName, stats, directory

#### This method gets all the active usb ports and selects the port that the TC1 is connected to by doing property comparisons that are unique to the TC1 connected port
def getSerialPort():
    try:
        activePorts = serial_ports()
        for port in activePorts:
            serialPort = serial.Serial(port)
            if (serialPort.baudrate == 9600):
                if (serialPort.parity == 'N'):
                    if (serialPort.timeout == None):
                        if (serialPort.xonxoff == False):
                            if platform.system() == 'Linux':     #new v2.0. TC1 will be a /dev/ttyACM* port on linux.
                                if serialPort.port.find('/dev/ttyACM') != -1:
                                    serialPort.close()
                                    return port
                            else:
                                serialPort.close()
                                return port
               
        #if(serialPort.inWaiting() != 0):
        #    return port
    except:
        print("Device not found")
        
        
        

#### Method Returns all active usb ports
def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#### Initializes the Header information for the SAC File
def initializeHeader(longitude, latitude , elevation, start=None):
    global stationId
    stats = Stats()
    stats.network = 'RU'
    stats.station = stationId
    stats.location = latitude+'N.'+longitude+'E'
    stats.channel = ' '
    stats._format = 'SAC'
    stats.calib = 1.0
    stats.sampling_rate = 18.7647228241   #This is just a preliminary value (for get_hour_data). This is changed before saving with stats as header.
    if start:
        stats.starttime = UTCDateTime(start)
    else:
        #starttime in stats is no longer the current time this function is called, but the start of the current hour (11/12/15)
        time = str(datetime.utcnow())
        year, month, day = time.split('-')[0], time.split('-')[1], time.split('-')[2].split()[0]    #utcnow() in form of 2015-12-10 03:21:24.769079
        hour = time.split()[1].split(':')[0]
        start = UTCDateTime(int(year),int(month),int(day),int(hour),0,0)
        stats.starttime = UTCDateTime(start)
    return stats

###Plotting process responsible for plotting data sent from the Collecting process, also responsible for managing Plotting window, and changing and refreshing the axis from 24 hour to 1 hour plots, This process saves screenshots of plot after ever hour and Uploads to NZSeis server
### This method receives several input parameters such as queue figure axis... the queue is read for arrays of values sent by the collecting process
### This data is then plotted according to the plot selection (24 or 1 hour) on the ax object
### This method is also responsible for managing the connectivity between the lines drawn
def plotData(queue, queue2, fig, ax, canvas, bottomFrame, root, lastY, lastX, connect, line, mode, geometry, dataInteractive):
    global plotting_loop, options_window, mainWin
    
    #Embedded callback function (also see code below) to make sure previously recorded data is plotted after the window has been resized. (17/12/15)
    def resize(root, geometry, mode):
        root.update_idletasks()
        new_geometry = root.geometry()
        new_geometry = new_geometry[:new_geometry.find('+')]    #Only concerned about when window is resized, not moved. (18/12/15)
        if new_geometry != geometry:
            dataInteractive.dataDeselector('resize')  #Must be in this if statement
            queue2.put(mode)
        return new_geometry
    
    if(queue.empty() == False):
        #read the arrays and values sent by the collecting process. If _continue is changed to False if this gets a call to plot previous data.
        values, _continue = queue.get(), True
        geometry = resize(root, geometry, mode)
        ##
        if values[4] == "24-Hour-Plot":    #Only when data is put in queue by plotPrevious (15/12/15)
            dataInteractive.dataDeselector('resize')
            connect = True
            lastX = 0
            lastY = 0
            mode = "24-Hour-Plot"          #This variable is local to plotData and is not the same as mode in Collecting (that's values[4])
            bottomFrame.mode = "24-Hour-Plot"
            bottomFrame.firstHour = datetime.utcnow()
            graphHeightConst = 2500

            ax.cla()

            ax.set_xlim(0,60)
            ax.set_ylim(30250,92750)
            ax.set_xlabel('Minute')
            ax.set_ylabel('Hour (UTC)')
            yAxis = [30250,92750]

            y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
            y2 = calculateYAxisLabels()
            ax = xAxisLabels(ax, 24)
            plt.yticks(y1, y2)
            ax.yaxis.grid(color = '#0000FF', linestyle = '-')
            ax.set_axisbelow(True)
            canvas.draw()
        
        if values[4] == "1-Hour-Plot" or values[4] == "1st-1-Hour-Plot":      #Only when data is put in queue by plotPrevious (15/12/15)
            dataInteractive.dataDeselector('resize')
            connect = True
            lastX = 0
            lastY = 0

            mode = "1-Hour-Plot"            #This variable is local to plotData and is not the same as mode in Collecting (that's values[4])
            bottomFrame.mode = "1-Hour-Plot"
            bottomFrame.firstHour = datetime.utcnow()
            if values[4] == "1st-1-Hour-Plot":  
                values[4] = "1-Hour-Plot"
                graphHeightConst = 2500

                ax.cla()

                ax.set_xlim(0,5)
                ax.set_ylim(30250,62750)
                ax.set_xlabel('Minute')
                ax.set_ylabel('Hour (UTC)')
                yAxis = [30250,62750]

                y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
                y2 = calculateYAxisLabelsOneHour()
                ax = xAxisLabels(ax, 1)
                plt.yticks(y1, y2)
                ax.yaxis.grid(color = '#0000FF', linestyle = '-')
                ax.set_axisbelow(True)
                canvas.draw()
       
        if values[0] == 'prev':
            plotPrevious(*values[1:])
            _continue = False   #Don't continue executing function
        ##
      
        if _continue:    
            y = values[0]
            x = values[1]

            #The following if statement and its content are incharge of inserting the last value of the the previous array to the front of the new array so the line would start from the last point to get connectivity between each line drawn 
            if(values[0].size != 0 and mode == "1-Hour-Plot" and values[4] != "1-Hour-Plot"):

                if(lastX != 0 and lastY != 0):
                    y = np.insert(y, 0, lastY)
                    x = np.insert(x, 0, lastX)
                lastY = values[0][-1]
                lastX = values[1][-1] 
                for value in x:
                    if value > 4.998 or ((value > 4.9) and (str(datetime.utcnow()).split(':')[1] == '00')):   #Addition to conditional to prevent probelems if the plotting of the last set is actually slightly after the hour has changed. (10/12/15)
                        lastX = 0
                        lastY = 0
                        x = np.array([])
                        y = np.array([])

            #The following if statement and its content are incharge of inserting the last value of the the previous array to the front of the new array so the line would start from the last point to get connectivity between each line drawn        
            if (connect == True and mode == "24-Hour-Plot"):
                if(lastX != 0 and lastY != 0):
                    y = np.insert(y, 0, lastY)
                    x = np.insert(x, 0, lastX)

            if (values[0].size != 0 and mode == "24-Hour-Plot"):   
                lastY = values[0][-1]
                lastX = values[1][-1]
                #print 'Last:', lastY, lastX

            if (values[2] == True and mode == "24-Hour-Plot"):
                timestamp = open('timestamp.txt', 'a')
                connect = False
                # calculating time for the screenshot name when saving it
                # v1.0 change: pyscreenshot.grab_to_file used instead of ImageGrab.grab().save()
                now = str(datetime.utcnow())
                now2 = now.split(' ',1 ) 
                now3 = now2[1].split(':',1) 
                now3 = int(now3[0])-1 
                if (now3 == -1):
                    now3 = 23
                name = str(now2[0]+'-'+str(now3)+".png")
                timestamp.write(str(now2[0]+'-'+str(now3)))
                timestamp.close()
                yr_mnth_day = now2[0].split('-')
                directory = stationId+'/'+yr_mnth_day[0]+'/'+yr_mnth_day[1]+'/'+yr_mnth_day[2]+'/'
                directory_handler(directory)
                #New Conditional v2.0. Screenshots causing problems with X server on ubuntu.
                if platform.system() != 'Linux':    
                    pyscreenshot.grab_to_file(directory+now2[0]+'-'+str(now3)+".png")

                    #upload image to NZSeis server - using the password and user name - kofi:pyjamaseis
                    contentType = 'image/png'
                    c = pycurl.Curl()
                    c.setopt(c.URL, 'https://nzseis.phy.auckland.ac.nz/pyjamaseis/upload/') 
                    c.setopt(c.HTTPHEADER, ['Authorization:'+'Basic %s' % base64.b64encode("kofi:pyjamaseis")]) 
                    c.setopt(c.HTTPPOST, [("payload",(c.FORM_FILE, name, c.FORM_CONTENTTYPE, contentType)), ("mode","image")]) 

                    try:
                        c.perform()
                        c.close()
                    except pycurl.error, error:
                        errno, errstr = error
                        print 'An error occurred: ', errstr


            else:
                connect = True


            if (values[2] == True and mode == "1-Hour-Plot"):
                timestamp = open('timestamp.txt', 'a')
                # calculating time for the screenshot name when saving it
                # v1.0 change: pyscreenshot.grab_to_file used instead of ImageGrab.grab().save()
                now = str(datetime.utcnow()) 
                now2 = now.split(' ',1 )
                now3 = now2[1].split(':',1)
                now3 = int(now3[0])-1
                if (now3 == -1):
                    now3 = 23
                name = str(now2[0]+'-'+str(now3)+".png")
                timestamp.write(str(now2[0]+'-'+str(now3)))
                timestamp.close()
                yr_mnth_day = now2[0].split('-')
                directory = stationId+'/'+yr_mnth_day[0]+'/'+yr_mnth_day[1]+'/'+yr_mnth_day[2]+'/'
                directory_handler(directory)
                #New Conditional v2.0. Screenshots causing problems with X server on ubuntu.
                if platform.system() != 'Linux': 
                    pyscreenshot.grab_to_file(directory+now2[0]+'-'+str(now3)+".png")

                    #upload image to NZSeis server - using the password and user name - kofi:pyjamaseis
                    contentType = 'image/png'
                    c = pycurl.Curl()
                    c.setopt(c.URL, 'https://nzseis.phy.auckland.ac.nz/pyjamaseis/upload/')
                    c.setopt(c.HTTPHEADER, ['Authorization:'+'Basic %s' % base64.b64encode("kofi:pyjamaseis")])
                    c.setopt(c.HTTPPOST, [("payload",(c.FORM_FILE, name, c.FORM_CONTENTTYPE, contentType)), ("mode","image")])

                    try:
                        c.perform()
                        c.close()
                    except pycurl.error, error:
                        errno, errstr = error
                        print 'An error occurred: ', errstr
                graphHeightConst = 2500
                dataInteractive.dataDeselector('resize')
                bottomFrame.firstHour = datetime.utcnow()
                ax.cla()

                ax.set_xlim(0,5)
                ax.set_ylim(30250,62750)
                ax.set_xlabel('Minute')
                ax.set_ylabel('Hour (UTC)')
                yAxis = [30250,62750]

                y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
                y2 = calculateYAxisLabelsOneHour()
                ax = xAxisLabels(ax, 1)
                plt.yticks(y1, y2)
                ax.yaxis.grid(color = '#0000FF', linestyle = '-')
                ax.set_axisbelow(True)
                canvas.draw()
                fig.canvas.mpl_connect('motion_notify_event', lambda event: bottomFrame.mouse_move(event, graphHeightConst))
                x = np.array([])
                y = np.array([])
                ##

            #Get the current time to display on the main plotting window
            now = str(datetime.utcnow())
            now1 = now.split('.',1)
            timeNow = now1[0]+' - UTC'
            bottomFrame.currentLabel.configure(text=timeNow) #sets the time as a label on the plot

            if(values[3] == True and mode == "24-Hour-Plot"):

                graphHeightConst = 2500
                dataInteractive.dataDeselector('resize')
                ax.cla()
                
                ax.set_xlim(0,60)                                   #05/01/16
                ax.set_ylim(30250,92750)
                ax.set_xlabel('Minute')
                ax.set_ylabel('Hour (UTC)')
                yAxis = [30250,92750]

                y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
                y2 = calculateYAxisLabels()

                ax = xAxisLabels(ax, 24)
                plt.yticks(y1, y2)
                ax.yaxis.grid(color = '#0000FF', linestyle = '-')
                ax.set_axisbelow(True)
                line, = ax.plot(x, y, color='k')
                canvas.draw()
                fig.canvas.mpl_connect('motion_notify_event', lambda event: bottomFrame.mouse_move(event, graphHeightConst))
                x = np.array([])
                y = np.array([])               
                
            line.set_data(x,y)
            ax.draw_artist(line)
     
    canvas.blit(ax.bbox)  #Makes motion_notify events much faster. If this is tabbed in 2, then motion_notify events only update every second. Hopefully no adverse memory effects. (09/01/16)
      
    if plotting_loop: 
        root.after(0, plotData,queue, queue2, fig, ax, canvas, bottomFrame, root, lastY, lastX, connect, line, mode, geometry, dataInteractive)

### Calculates labels required to represent the y axis for a 24 hour plot
def calculateYAxisLabels(): 
      
    #24 hour labels
    yaxislabels = []
     
    #Gets current hour and generates an array containing values of the following 24 hours
    now = str(datetime.utcnow()) 
    now = now.split(' ',1)
    now = now[1].split(':',1)
    d = datetime.strptime(now[0], "%H")
    d = str(d.strftime("%I %p")).split(' ',1)
    
    currentHour = int(d[0]) 
    ampm = str(" "+d[1]) 

    hourAfter = currentHour + 1
    hourAfterAmPm = ampm
      
    if hourAfter == 12:
        if(hourAfterAmPm == ' AM'):
            hourAfterAmPm = ' PM'
        else:
            hourAfterAmPm = ' AM'
          
    if hourAfter == 13:
        hourAfter = 1
  
    yaxislabels.append(str(currentHour)+ampm)
      
    while currentHour != hourAfter or ampm != hourAfterAmPm:
        yaxislabels.append(str(hourAfter)+ hourAfterAmPm)
          
        hourAfter += 1
          
        if hourAfter == 12:
            if(hourAfterAmPm == ' AM'):
                hourAfterAmPm = ' PM' 
            else:
                hourAfterAmPm = ' AM'
          
        if hourAfter == 13:
            hourAfter = 1
              
    yaxislabels.append('')
    return yaxislabels[::-1]

### Calculates labels required to represent the y axis for a 1 hour plot
def calculateYAxisLabelsOneHour(): 
      
    #24 hour labels
    yaxislabels = []
     
    #Gets current hour and generates an array containing values of that hour divided into 5 minute sections
    now = str(datetime.utcnow())
    now = now.split(' ',1)
    now = now[1].split(':',1)
    d = datetime.strptime(now[0], "%H") 
    d = str(d.strftime("%I %p")).split(' ',1)
    start = 00
    currentHour = int(d[0])
    for i in range(0, 12):
        if(start<10):
            yaxislabels.append(str(currentHour)+':0'+str(start))
        else:
            yaxislabels.append(str(currentHour)+':'+str(start))
        start = start+5
    
    yaxislabels.append('')
    return yaxislabels[::-1]  
                 

## Function to find the labels for the x axis and draw grid.
def xAxisLabels(ax, mode):
    if mode == 24:
        x_list = []
        for i in range(61):   #(17/12/15)
            if i%5 == 0:
                x_list.append('+'+str(i))
            else:
                x_list.append('')
        ax.set_xticks(np.arange(0,61,5))
        ax.set_xticks(np.arange(0,61,1), minor=True)
        ax.set_xticklabels([':00',':05',':10',':15',':20',':25',':30',':35',':40',':45',':50',':55',''])
        ax.set_xticklabels(['']*61, minor=True)
        ax.xaxis.grid(which = 'minor', color = '#7DCEA0', linestyle = ':')
        ax.xaxis.grid(which = 'major', color = '#51bd80', linestyle = ':')
        ax.xaxis.set_tick_params(labeltop='on')
        return ax
    elif mode == 1:
        x_list = []
        for i in range(31):   #(17/12/15)
            if i%6 == 0:
                x_list.append('+'+str(i/6))
            else:
                x_list.append('')
        ax.set_xticks(np.arange(0,6,1))
        ax.set_xticks(np.arange(0,5.1,0.1666666666666666666666666666666), minor=True)
        ax.set_xticklabels(['+0','+1','+2','+3','+4','+5'])
        ax.set_xticklabels(['']*31, minor=True)
        ax.xaxis.grid(which = 'minor', color = '#7DCEA0', linestyle = ':')
        ax.xaxis.grid(which = 'major', color = '#51bd80', linestyle = ':')
        ax.xaxis.set_tick_params(labeltop='on')
        return ax       
    
    

###Function to define what occurs when the main plotting window is closed. This is taken as exiting PyjAmaseis, so all windows and processes are ended. (07/12/15)
def window_close(condition=False):
    global plotting_loop, collecting_loop, mainWin, options_window
    plotting_loop, collecting_loop = False, False
    if not condition:       #Condition is True if program has not yet fully started (TC1 not connected error dialog exit press)
        options_window.close()
        mainWin.quit()

##Function (new v2.0) to support the new file saving system. Tries to make directory, and if directory already exists, ignores the exception raised. All other exceptions are reported. (09/12/15)
def directory_handler(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise    

##Function to populate hourSeismicData array with any previous readings in that hour before readings start.
def getHourData(stats):
    sampling_rate = stats['sampling_rate']
    time = str(datetime.utcnow())
    year, month, day = time.split('-')[0], time.split('-')[1], time.split('-')[2].split()[0]    #utcnow() in form of 2015-12-10 03:21:24.769079
    hour = time.split()[1].split(':')[0]
    filename = year[2:]+month+day+hour+stationId+'.sac'
    directory = stationId+'/'+year+'/'+month+'/'+day+'/'+filename
    if not os.path.exists(directory):      #returns an array with appropriate number of zeroes since beginning of hour
        hour_seconds = (datetime(int(year),int(month),int(day),int(hour),0,0) - datetime(1970,1,1)).total_seconds()
        number_of_zeroes = int((Time.time()-hour_seconds)*sampling_rate)
        return np.array([32750]*number_of_zeroes), stats
    else:      #returns array with data previously recorded in that hour
        trace = read(pathname_or_url = directory, format = 'SAC')
        trace = trace.pop(0)
        data = trace.data
        hour_seconds = (datetime(int(year),int(month),int(day),int(hour),0,0) - datetime(1970,1,1)).total_seconds()
        number_of_zeroes = int((Time.time()-hour_seconds)*sampling_rate)-len(data)
        return np.append(data, [32750]*number_of_zeroes), stats
            
        
        

### Main Method, this is where the application starts - 2 queues are created for passing data between these threads, and 2 process are created one for collecting the data and the other for plotting it
if __name__ == '__main__':
    global collecting_loop, plotting_loop, options_window, tkframes  #(09/12/15)
    
    #Create 2 queues, one is used for communication between the collecting and plotting thread, the second is used between the collecting process and options window to send the selection information that the user does
    queue = Queue()
    queue2 = Queue()
    queue3 = Queue()
    
    #Create 2 threads
    collecting_loop, plotting_loop = True, True
    collectionProcess = Thread(target= Collecting, args=(queue,queue2,queue3,))

    #Making threads daemons so that the program closes when processes in them stop (09/12/15).
    collectionProcess.daemon = True

    ##Starting everything
    collectionProcess.start() 
    
    #Previously, Plotting was the target for the plotting thread (plottingProcess, v1.0). This has been changed (14/01/16), as TkInter does not behave well when
    #the mainloop is not in the Main Thread. Once the main window has been closed (see window_close, initiated by protocol of main window), the code after the
    #mainloop can be executed to save the data before the entire program is closed. The while loops wait for the tuple of data from collecting to be placed in the
    #queue.
    window = Plotting(queue,queue2)
    if plotting_loop:              #This conditional is only False if the TC-1 is not connected on startup. No windows will have been created if this is the case, and the user has chosen to exit (see while loop near beginning of Collecting).
        
        tkframes = mFrame(queue3, window.root)
        window.root.mainloop()
        
        #Wait until data is put into queue by Collecting, then save data and close.
        while queue.empty():
            waiting = 'Waiting for final data from Collecting'
        trying = True
        while trying:
            if not queue.empty():
                data = queue.get()
                if type(data) == type((1,)):
                    trying = False
        print 'Saving:'
        print ''
        saveHourData(data[0], data[1], data[2], data[3], data[4] , data[5])
        print ''
        print 'Done'
