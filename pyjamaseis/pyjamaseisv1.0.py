#=================================================================================================================
# Structure of PyjAmaseis 
#
# - IMPORTS
# - STATION INFORMATION USER INTERFACE CODE (class myFrame4)
# - SECONDARY OPTIONS UI WINDOW CODE (class selectionWindow)
# - alignToBottomRight Function - aligns secondary window to bottom right hand corner of screen
# - secondaryWindow Function - creates the Options window
# - Collecting Function - collects and process data read from the TC1
# - getSerialPort Function - finds the serial port the TC1 is connected to
# - serial_ports Functions - returns all active serial ports
# - initializeHeader Function used to create a header object for headers in a SAC object
# - Plotting Function - plots data sent from collecting process live
# - plotData - called by the Plotting function to plot data
# - calculateYAxisLabels - creates 24 hour UTC labels for the y axis, these are saved in an array
# - calculateYAxisLabelsOneHour - creates y axis labels for the current hour in UTC divided into 5 minute sections
# - if __name__ == '__main__': - the is where the code starts
#
#=================================================================================================================

### Importing all required libraries for running PyjAmaseis
import matplotlib
matplotlib.use('TkAgg')

import easygui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random
import numpy as np
import sys
import Tkinter as tk
import time as Time
import serial
import struct
import easygui as eg
from obspy import read, Trace, UTCDateTime
from obspy.core.stream import Stream
from obspy.core import AttribDict
import pylab as pylt
from datetime import datetime
import time
from decimal import *
from multiprocessing import Process, Pipe, Queue
from PIL import ImageGrab
from threading import Thread
import wx
from pygeocoder import Geocoder
import gettext
import os
import glob
from attrdict import AttrDict
import fileinput
import pycurl
import base64
from urllib import urlencode


#### Initial window presented to user when launching PyjAmaseis for the first time
#### This window will require the user to enter the station information which will be later used when saving SAC files
#### Class was auto generate by using wxGlade
class MyFrame4(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame4.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.iconFile = "icon.ico"
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
        file.write("Longitude:"+self.text_ctrl_6.GetValue()+"\n")
        file.write("Latitude:"+self.text_ctrl_7.GetValue()+"\n")
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
        wx.Frame.__init__(self, *args, **kwds)
        self.iconFile = "icon.ico"
        self.icon = wx.Icon(self.iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.button_3 = wx.Button(self, wx.ID_ANY, ("24 Hour Plotting"))
        self.panel_3 = wx.Panel(self, wx.ID_ANY)
        self.button_4 = wx.Button(self, wx.ID_ANY, ("1 Hour Plotting"))
        self.panel_4 = wx.Panel(self, wx.ID_ANY)
        self.spin_button_1 = wx.SpinButton(self, wx.ID_ANY , style=wx.SP_VERTICAL)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, (" Graph Shift"), style=wx.ALIGN_CENTRE)
        self.panel_5 = wx.Panel(self, wx.ID_ANY)
        
        self.Bind(wx.EVT_BUTTON, self.twentyFourHourPlot, id = self.button_3.Id)
        self.Bind(wx.EVT_BUTTON, self.oneHourPlot, id = self.button_4.Id)
        self.Bind(wx.EVT_SPIN_UP, self.graphMoveUp, id = self.spin_button_1.Id)
        self.Bind(wx.EVT_SPIN_DOWN, self.graphMoveDown, id = self.spin_button_1.Id)
        self.Bind(wx.EVT_CLOSE, self.doNothingIfExitButtonIsPressed)
        self.__set_properties()
        self.__do_layout()
        # end wxGlade
    def doNothingIfExitButtonIsPressed(self,e):
        a = 5
        
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
    
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(("Options"))
        self.SetSize((190, 239))
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.panel_2.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.label_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.panel_2, 1, wx.EXPAND, 0)
        sizer_2.Add(self.button_3, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        sizer_2.Add(self.panel_3, 1, wx.EXPAND, 0)
        sizer_2.Add(self.button_4, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        sizer_2.Add(self.panel_4, 1, wx.EXPAND, 0)
        sizer_5.Add(self.spin_button_1, 2, wx.LEFT | wx.EXPAND, 10)
        sizer_5.Add(self.label_1, 4, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_2.Add(self.panel_5, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade
        
#### This method aligns the Options window to the bottom right hand corner of the screen so it doesn't come in the way of plotting
def alignToBottomRight(win):
    dw, dh = wx.DisplaySize()
    w, h = win.GetSize()
    x = dw - w
    y = dh - h
    win.SetPosition((x-20, y-65))

#### This method creates the Options window
def secondaryWindow(queue2):
    
    app = wx.App(False)
    frame_1 = selectionWindow(None, wx.ID_ANY, "")
    app.SetTopWindow(frame_1)
    alignToBottomRight(frame_1)
    frame_1.Show()
    frame_1.Raise()
    app.MainLoop()

#### This is the Collecting method (Thread) responsible for reading data from the TC1, sending this data via a queue to plotting thread/method, saving data into SAC, listening to commands from Options window, and uploading SAC files to NZSeis server after saving them
def Collecting(queue, queue2):
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
    
    hourSeismicData = np.array([]) #used to store 18 time values for every value read from the tc1 and sent is sent to the plotting array, then cleared for next 18 values
    tempSeismicData = np.array([]) #used to store 18 value read from the tc1 and sent is sent to the plotting array, then cleared for next 18 values
    
    #hourMillisecondData = np.array([], dtype = np.float64)
    tempMillisecond = np.array([], dtype = np.float64)
    
    serialNumber = None 
    serialPort = None
    
    #Returns the serialPort that the TC1 is connected to
    serialPort = getSerialPort()
    
    #This while loop ensures user has collected the TC1 before continuing
    while serialPort == None:
        easygui.msgbox("Please connect TC1 Seismometer", title="Warning")
        serialPort = getSerialPort()
        
    serialPort = serial.Serial(serialPort)
    serialPort.flushInput()
    serialPort.flushOutput()
    
    #create a stats object that holds all the station information retrieved from the txt file
    stats = initializeHeader(stationId, stationName,stationAddress, longitude, latitude , elevation)

    #The following two lines create the secondary options window
    secondaryWindowProcess = Thread(target= secondaryWindow, args=(queue2,))
    secondaryWindowProcess.start()
    
    queue.put("Start Plotting Process")
    
    while True:
        try:
            
            #Checks whether the user has changed the view selection in the options window from 24 hour to 1 hour or has increased or decreased the graphShift
            if(queue2.empty() == False):
                readingQueue2 = queue2.get()
                if readingQueue2 == "24-Hour-Plot":
                    mode = "24-Hour-Plot"
                    currentMode = "24Hour"
                    totalHoursConst = 23
                    tempSeismicData = np.array([])
                    tempMillisecond = np.array([])
                    
                if readingQueue2 == "1-Hour-Plot":
                    mode = "1-Hour-Plot"
                    currentMode = "1Hour"
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
               
            #Read from the TC1 seismometer     
            reading = int(serialPort.readline())
            
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
            
            
            timeNow = datetime.time(datetime.now())
            time = timeNow.minute + (timeNow.second + timeNow.microsecond/1000000.0)/60.0
            hour = timeNow.hour 
            plotClear = False
              
            if (hour != lastHour):
                ## Everytime the hour changes the following code saves hour long SAC Files
                
                lastHour = hour
                currentTime = str(datetime.utcnow()) 
                now2 = currentTime.split(' ',1 )
                now3 = now2[1].split(':',1)
                now3 = int(now3[0])-1
                if (now3 == -1):
                    now3 = 23

                stats['endtime'] = UTCDateTime()
                stats['ntps'] = len(hourSeismicData)
                
                st = Stream([Trace(data=hourSeismicData, header=stats)])
                
                sacdateAndTime = str(stats['starttime']).split('T')
                
                sacdate =  sacdateAndTime[0].split('-')
                sactime =  sacdateAndTime[1].split(':')
                sacyear  = sacdate[0][2:]
                sacmonth = sacdate[1]
                sacday = sacdate[2]
                sachour = sactime[0]
                sacminute = sactime[1]
                fileNaame = str(sacyear+sacmonth+sacday+sachour+sacminute+stats['station']+".sac")
                st.write(sacyear+sacmonth+sacday+sachour+sacminute+stats['station']+".sac", format='SAC')
                stats = initializeHeader(stationId, stationName,stationAddress, longitude, latitude , elevation)
                hourSeismicData = np.array([]) 
                
                ##Uploads SAC file right after creating it
                
                contentType = "application/octet-stream" #image/png
                c = pycurl.Curl()
                c.setopt(c.URL, 'https://nzseis.phy.auckland.ac.nz/pyjamaseis/upload/')
                c.setopt(c.HTTPHEADER, ['Authorization:'+'Basic %s' % base64.b64encode("kofi:pyjamaseis")])
                c.setopt(c.HTTPPOST, [("payload",(c.FORM_FILE, fileNaame, c.FORM_CONTENTTYPE, contentType)), ("mode","sac")])
                
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
                    else:
                        tempSeismicData = np.append(tempSeismicData,data)
                        tempMillisecond = np.append(tempMillisecond,time)
                        hourSeismicData = np.append(hourSeismicData,reading)
            
            count += 1
                
        except ValueError, e:
             print(e)

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
                           serialPort.close()
                           return port
               
#            if(serialPort.inWaiting() != 0):
#                return port
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
def initializeHeader(stationId, stationName,stationAddress, longitude, latitude , elevation):
   
    sampling_rate = 18.7647228241
    delta = 1/sampling_rate

    stats = {'network': 'RU', 'station': 'AUCK', 'location': '0.0', 'channel': ' ', 'starttime': UTCDateTime(),'_format': 'SAC', 'sampling_rate': 18.7647228241, 'calib': 1.0,'delta': delta, 'sac': AttrDict({'stla': latitude, 'stlo': longitude, 'stel': elevation})}
    return stats


#### Plotting process responsible for plotting data sent from the Collecting process, also responsible for Plotting window, and changing and refreshing the axis from 24 hour to 1 hour plots, This process saves screenshots of plot after ever hour and Uploads to NZSeis server
def Plotting(queue):
    
    while queue.get() != "Start Plotting Process":
        wait = "Waiting"
    
    timeNow = datetime.time(datetime.now())
    time = timeNow.minute + (timeNow.second + timeNow.microsecond/1000000.0)/60.0
    lastX = time
    lastY = 90250
    connect = True
    step = 0
    x=[]
    y=[]
    
    mode = "24-Hour-Plot"
    
    root = tk.Tk()
    root.wm_title("PyAmaseis v1.0")
    root.iconbitmap(r'icon.ico')
    root.wm_state('zoomed')
    
    graphHeightConst = 2500
    
    fig = plt.figure(figsize=(15,10))
    fig.set_tight_layout(0.4)
    
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim(0,60)
    ax.set_ylim(30250,92750)
    ax.set_xlabel('Time(minutes)')
    
    xAxis = [0,60]
    yAxis = [30250,92750]
    
    y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
    y2 = calculateYAxisLabels()
    
    ax.set_xticks(np.arange(min(xAxis), max(xAxis)+1,1))
    plt.yticks(y1, y2)
    ax.yaxis.grid(color = '#0000FF' )
    ax.set_axisbelow(True)
    line, = ax.plot(x, y, color='k')
    canvas = FigureCanvasTkAgg(fig, master=root)

    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    label = tk.Label(text="")
    label.pack()
    background = canvas.copy_from_bbox(ax.bbox)
    canvas.draw()

    root.after(0, plotData,queue, fig, ax, canvas, label, root, lastY, lastX, connect, background, line, mode)
    
    root.mainloop()

### This method receives several input parameters such as queue figure axis... the queue is read for arrays of values sent by the collecting process
### This data is then plotted according to the plot selection (24 or 1 hour) on the ax object
### This method is also responsible for managing the connectivity between the lines drawn
def plotData(queue, fig, ax, canvas, label, root, lastY, lastX, connect, background, line, mode):
  if(queue.empty() == False):
      
      #read the arrays and values sent by the collecting process
      values = queue.get()
      
      ##
      if values[4] == "24-Hour-Plot":
        connect = True
        lastX = 0
        lastY = 0
        mode = "24-Hour-Plot"
        graphHeightConst = 2500
           
        ax.cla()
           
        ax.set_xlim(0,60)
        ax.set_ylim(30250,92750)
        ax.set_xlabel('Time(minutes)  ')
         
        xAxis = [0,60]
        yAxis = [30250,92750]
         
        y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
        y2 = calculateYAxisLabels()
         
        ax.set_xticks(np.arange(min(xAxis), max(xAxis)+1,1))
        plt.yticks(y1, y2)
        ax.yaxis.grid(color = '#0000FF' )
        ax.set_axisbelow(True)
        canvas.draw()
        x = np.array([])
        y = np.array([])
        
      if values[4] == "1-Hour-Plot":
        connect = True
        lastX = 0
        lastY = 0
        
        mode = "1-Hour-Plot"
        graphHeightConst = 2500
           
        ax.cla()
           
        ax.set_xlim(0,5)
        ax.set_ylim(30250,62750)
        ax.set_xlabel('Time(minutes)  ')
         
        xAxis = [0,5]
        yAxis = [30250,62750]
         
        y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
        y2 = calculateYAxisLabelsOneHour()
         
        ax.set_xticks(np.arange(min(xAxis), max(xAxis)+1,1))
        plt.yticks(y1, y2)
        ax.yaxis.grid(color = '#0000FF' )
        ax.set_axisbelow(True)
        canvas.draw()
        x = np.array([])
        y = np.array([])
      ##
      
      y = values[0]
      x = values[1]
      
      #The following if statement and its content are incharge of inserting the last value of the the previous array to the front of the new array so the line would start from the last point to get connectivity between each line drawn 
      if(values[0].size != 0 and mode == "1-Hour-Plot"):
        
          if(lastX != 0 and lastY != 0):
              y = np.insert(y, 0, lastY)
              x = np.insert(x, 0, lastX)
          lastY = values[0]
          lastY = lastY[lastY.size - 1]
          lastX = (values[1])
          lastX = lastX[lastX.size - 1] 
          for value in x:
              if value > 4.999:
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
          lastY = values[0]
          lastY = lastY[lastY.size - 1]
          lastX = (values[1])
          lastX = lastX[lastX.size - 1] 
    
      if (values[2] == True and mode == "24-Hour-Plot"):
          
          connect = False
          
          # calculating time for the screenshot name when saving it
          now = str(datetime.utcnow())
          now2 = now.split(' ',1 ) 
          now3 = now2[1].split(':',1) 
          now3 = int(now3[0])-1 
          if (now3 == -1):
              now3 = 23
          name = str(now2[0]+'-'+str(now3)+".png")
          ImageGrab.grab().save(now2[0]+'-'+str(now3)+".png", "PNG")
          
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
        
        # calculating time for the screenshot name when saving it
        now = str(datetime.utcnow()) 
        now2 = now.split(' ',1 )
        now3 = now2[1].split(':',1)
        now3 = int(now3[0])-1
        if (now3 == -1):
            now3 = 23
        name = str(now2[0]+'-'+str(now3)+".png")
        ImageGrab.grab().save(now2[0]+'-'+str(now3)+".png", "PNG")
        
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
           
        ax.cla()
           
        ax.set_xlim(0,5)
        ax.set_ylim(30250,62750)
        ax.set_xlabel('Time(minutes)  ')
         
        xAxis = [0,5]
        yAxis = [30250,62750]
         
        y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
        y2 = calculateYAxisLabelsOneHour()
         
        ax.set_xticks(np.arange(min(xAxis), max(xAxis)+1,1))
        plt.yticks(y1, y2)
        ax.yaxis.grid(color = '#0000FF' )
        ax.set_axisbelow(True)
        canvas.draw()
        x = np.array([])
        y = np.array([])
        ##
          
      #Get the current time to display on the main plotting window
      now = str(datetime.utcnow())
      now1 = now.split('.',1)
      timeNow = now1[0]+' - UTC'
      label.configure(text=timeNow) #sets the time as a label on the plot
    
      if(values[3] == True and mode == "24-Hour-Plot"):
          
          graphHeightConst = 2500
          
          ax.cla()
          
          ax.set_xlim(0,60)
          ax.set_ylim(30250,92750)
          ax.set_xlabel('Time(minutes)  ')
        
          xAxis = [0,60]
          yAxis = [30250,92750]
        
          y1 = (np.arange(min(yAxis), max(yAxis)+1,graphHeightConst))
          y2 = calculateYAxisLabels()
        
          ax.set_xticks(np.arange(min(xAxis), max(xAxis)+1,1))
          plt.yticks(y1, y2)
          ax.yaxis.grid(color = '#0000FF' )
          ax.set_axisbelow(True)
          canvas.draw()
          x = np.array([])
          y = np.array([])
              
      line.set_data(x,y)
      ax.draw_artist(line)
      canvas.blit(ax.bbox)
      
  root.after(0, plotData,queue, fig, ax, canvas, label, root, lastY, lastX, connect, background, line, mode)
 

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


### Main Method, this is where the application starts - 2 queues are created for passing data between these threads, and 2 process are created one for collecting the data and the other for plotting it
if __name__ == '__main__':
    
    #Create 2 queues, one is used for communication between the collecting and plotting thread, the second is used between the collecting process and options window to send the selection information that the user does
    queue = Queue()
    queue2 = Queue()
    
    #Create 2 threads
    collectionProcess = Thread(target= Collecting, args=(queue,queue2,))
    plottingProcess = Thread(target= Plotting, args=(queue,))
    
    ##Starting everything
    collectionProcess.start() 
    plottingProcess.start()
    
    plottingProcess.join()
    collectionProcess.join()
