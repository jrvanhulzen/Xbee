#!/usr/bin/python
# scp "/Users/janvanhulzen/Documents/Courses/Inholland/project11/Editie_20212022/ProjectRPI.nosync/setup local L027/testxbee3.py" pi@studentpi.local:
#
# Script voor het uitlezen van Xbee settings (Zigbee protocol)
# Jan van Hulzen : v1.0 19-8-2022
# Project 1.1

import time as timelib
from datetime import datetime
import os
from digi.xbee.devices import DigiMeshDevice, RemoteXBeeDevice, XBeeDevice , ZigBeeDevice
from digi.xbee.io import IOLine
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.models.mode import APIOutputModeBit
from digi.xbee.util import utils
import logging
from config import logger

webroot = '/var/www/html'

NetworkParameters=dict([("ID","PAN ID "),("SC","Scan Channels" ),("SD","Scan Duration"),("ZS","Zigbee Stack Profile"),("NJ","Node Joint Time"),
      ("OP","Operating PAN ID"),("OI","Operating 16 Bit PAN ID"),("CH","Operating Channel"),("NC","Number of remaining children")])

AddressingParameters = dict([("SH","Serial Number High"),("SL","Serial Number Low"),("MY","16 Bit Network Address"),("DH","Desitination Address High"),
                             ("DL","Desitination Address Low"),("NI","Node Identifier"),("NH","Maximum number op hops"),("BH","Broadcast Radius"),
                             ("AR","Many-To-One Broadcast Time"),("DD","Device Type Identifier"),("NT","Node Discovery BackOff"),
                             ("NO","Node Discovery Options"),("NP","Maximum Number of API Transmission Bytes"),("CR","PAN Conflict Threshold")])

IOParameters = dict([("D0","AD0/DIO0 Configuration"),("D1","AD1/DIO1 Configuration"),("D2","AD2/DIO2 Configuration"),("D3","AD3/DIO3 Configuration"),
                     ("D4","DIO4 Configuration"),("D5","DIO5/Assoc Configuration "),("P0","DIO10/PWM0 Configuration"),("P1","DIO11 Configuration"),("P2","DIO12 Configuration"),("PR","Pull-up Resistor Enable"),("LT","Associate LED Blink Time"),("RP","RSSI PWM Timer"),
                     ("DO","Device Options ")])
    
IOParameterOptions={}

IOParameterOptions["D0"] = [ "Disabled [0]","Commisioning Button [1]", "ADC [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
IOParameterOptions["D1"] = [ "Disabled [0]","NA [1]", "ADC [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
IOParameterOptions["D2"] = [ "Disabled [0]","NA [1]", "ADC [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
IOParameterOptions["D3"] = [ "Disabled [0]","NA [1]", "ADC [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
IOParameterOptions["D4"] = [ "Disabled [0]","NA [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
IOParameterOptions["D5"] = [ "Disabled [0]","Associated Indicator [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
IOParameterOptions["P0"] = [ "Disabled [0]","RSSI PWM Output [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
IOParameterOptions["P1"] = [ "Disabled [0]","RSSI PWM Output [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
IOParameterOptions["P2"] = [ "Disabled [0]","RSSI PWM Output [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
IOParameterOptions["PR"] = [ "NA" ]
IOParameterOptions["LT"] = [ "NA" ]
IOParameterOptions["RP"] = [ "NA" ]
IOParameterOptions["DO"] = [ "NA" ]

#utils.hex_string_to_bytes("ABCD")
def PrintXbeeSettings(device):
    try:
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+")
        for k,v in NetworkParameters.items():
            print("|",v.ljust(40," "),"|",k,"| %s |" % utils.hex_to_string(device.get_parameter(k)).ljust(24," "))
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+")
        for k,v in AddressingParameters.items():
            if k=="NI":
                print("|",v.ljust(40," "),"|",k,"|%s  |" % device.get_parameter(k).decode().ljust(24," "))
            else:
                print("|",v.ljust(40," "),"|",k,"| %s |" % utils.hex_to_string(device.get_parameter(k)).ljust(24," "))
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+")
        for k,v in IOParameters.items():
            if IOParameterOptions[k][0]=="NA":
                print("|",v.ljust(40," "),"|",k,"| %s |" % utils.hex_to_string(device.get_parameter(k)).ljust(24," "))
            else:
                print("|",v.ljust(40," "),"|",k,"| %s |" % IOParameterOptions[k][int(utils.hex_to_string(device.get_parameter(k)),16)].ljust(24," "))
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+")
    except:
        print("Error reading settings...")
        return(-1)                                                                                 
    return(0) 

def PrintXbeeSettingsHTML(device):
    filehtml = open(f"{webroot}/XBeeData.html", "w", encoding="utf-8")
    try:
        filehtml.write('<!DOCTYPE html>\n')
        filehtml.write('<html>\n')
        filehtml.write('<head>\n')
        filehtml.write('<style>\n')
        filehtml.write('table, th  {\n')
        filehtml.write(' width: 70%;\n')
        filehtml.write(' border: 3px solid black;\n')
        filehtml.write(' border-collapse: collapse;\n')
        filehtml.write(' background-color: #96D4D4;\n')
        filehtml.write('}\n')
        filehtml.write('th.a {\n')
        filehtml.write('text-align: left;\n')
        filehtml.write(' border: 3px solid black;\n')
        filehtml.write('width: 50%;\n')
        filehtml.write('}\n')
        filehtml.write('th.b {\n')
        filehtml.write('text-align: left;\n')
        filehtml.write(' border: 3px solid black;\n')
        filehtml.write('width: 10%;\n')
        filehtml.write('}\n')
        filehtml.write('th.c {\n')
        filehtml.write(' width: 40%;\n')
        filehtml.write(' border: 3px solid black;\n')
        filehtml.write('text-align: left;\n')
        filehtml.write('}\n')
        filehtml.write('td {\n')
        filehtml.write(' border: 1px solid black;\n')
        filehtml.write(' border-collapse: collapse;\n')
        filehtml.write('}\n')
        filehtml.write('</style>\n')
        filehtml.write('</head>\n')
        filehtml.write('<body>\n')
        filehtml.write('<h2>XBee Settings</h2>\n')
        filehtml.write('<p>Local XBee Module:</p>\n')
        filehtml.write('<table>\n')
        filehtml.write(' <thead>\n')
        filehtml.write('  <tr>\n')
        filehtml.write('   <th class="a">Parameter</th>\n')
        filehtml.write('   <th class="b">ID</th>\n')
        filehtml.write('   <th class="c">Data</th>\n')
        filehtml.write('  </tr>\n')
        filehtml.write(' </thead>\n')
        filehtml.write(' <tbody>\n')
        for k,v in NetworkParameters.items():
            filehtml.write("<tr><td>"+v.ljust(40," ")+"</td><td>"+k+"</td><td> %s </td></tr>\n" % utils.hex_to_string(device.get_parameter(k)).ljust(24," "))
        for k,v in AddressingParameters.items():
            if k=="NI":
                filehtml.write("<tr><td>"+v.ljust(40," ")+"</td><td>"+k+"</td><td>%s  </td></tr>" % device.get_parameter(k).decode().ljust(24," "))
            else:
                filehtml.write("<tr><td>"+v.ljust(40," ")+"</td><td>"+k+"</td><td> %s </td></tr>" % utils.hex_to_string(device.get_parameter(k)).ljust(24," "))
        for k,v in IOParameters.items():
            if IOParameterOptions[k][0]=="NA":
                filehtml.write("<tr><td>"+v.ljust(40," ")+"</td><td>"+k+"</td><td> %s </td></tr>" % utils.hex_to_string(device.get_parameter(k)).ljust(24," "))
            else:
                filehtml.write("<tr><td>"+v.ljust(40," ")+"</td><td>"+k+"</td><td> %s </td></tr>" % IOParameterOptions[k][int(utils.hex_to_string(device.get_parameter(k)),16)].ljust(24," "))
        filehtml.write('</tbody>\n')
        filehtml.write("</table>\n")
        filehtml.write('</body>')
        filehtml.close()
    except Exception as e:
        print(e)
        filehtml.write("Error reading settings...")
        filehtml.close()
        return(-1)                                                                                 
    return(0) 

def PrintXbeeSettingsHTML2(DeviceA,DeviceB):
    filehtml = open(f"{webroot}/XBeeData.html", "w", encoding="utf-8")
    try:
        filehtml.write('<!DOCTYPE html>\n')
        filehtml.write('<html>\n')
        filehtml.write('<head>\n')
        filehtml.write('<style>\n')
        filehtml.write('table, th  {\n')
        filehtml.write(' width: 70%;\n')
        filehtml.write(' border: 3px solid black;\n')
        filehtml.write(' border-collapse: collapse;\n')
        filehtml.write(' background-color: #96D4D4;\n')
        filehtml.write('}\n')
        filehtml.write('th.a {\n')
        filehtml.write('text-align: left;\n')
        filehtml.write(' border: 3px solid black;\n')
        filehtml.write('width: 55%;\n')
        filehtml.write('}\n')
        filehtml.write('th.b {\n')
        filehtml.write('text-align: center;\n')
        filehtml.write(' border: 3px solid black;\n')
        filehtml.write('width: 5%;\n')
        filehtml.write('}\n')
        filehtml.write('th.c,th.d {\n')
        filehtml.write(' width: 20%;\n')
        filehtml.write(' border: 3px solid black;\n')
        filehtml.write('text-align: left;\n')
        filehtml.write('}\n')
        filehtml.write('td {\n')
        filehtml.write(' border: 1px solid black;\n')
        filehtml.write(' border-collapse: collapse;\n')
        filehtml.write('}\n')
        filehtml.write('td.a {\n')
        filehtml.write('text-align: center;\n')
        filehtml.write('}\n')
        filehtml.write('</style>\n')
        filehtml.write('</head>\n')
        filehtml.write('<body>\n')
        filehtml.write('<h2>XBee Settings</h2>\n')
        filehtml.write('<p>Local XBee Module:</p>\n')
        filehtml.write('<table>\n')
        filehtml.write(' <thead>\n')
        filehtml.write('  <tr>\n')
        filehtml.write('   <th class="a">Parameter</th>\n')
        filehtml.write('   <th class="b">ID</th>\n')
        filehtml.write('   <th class="c">Local</th>\n')
        filehtml.write('   <th class="d">Remote</th>\n')
        filehtml.write('  </tr>\n')
        filehtml.write(' </thead>\n')
        filehtml.write(' <tbody>\n')
        for k,v in NetworkParameters.items():
            filehtml.write("<tr><td>"+v.ljust(40," ")+'</td><td class="a">'+k+"</td><td> %s </td><td> %s </td></tr>\n" 
                           % (utils.hex_to_string(DeviceA.get_parameter(k)).ljust(24," "),
                              utils.hex_to_string(DeviceB.get_parameter(k)).ljust(24," ")))
        for k,v in AddressingParameters.items():
            if k=="NI":
                filehtml.write("<tr><td>"+v.ljust(40," ")+'</td><td class="a">'+k+"</td><td>%s  </td><td> %s </td></tr>" 
                               %(DeviceA.get_parameter(k).decode().ljust(24," "),DeviceB.get_parameter(k).decode().ljust(24," ")))
            else:
                filehtml.write("<tr><td>"+v.ljust(40," ")+'</td><td class="a">'+k+"</td><td> %s </td><td> %s </td></tr>" 
                               % (utils.hex_to_string(DeviceA.get_parameter(k)).ljust(24," "),
                                  utils.hex_to_string(DeviceB.get_parameter(k)).ljust(24," ")))
        for k,v in IOParameters.items():
            if IOParameterOptions[k][0]=="NA":
                filehtml.write("<tr><td>"+v.ljust(40," ")+'</td><td class="a">'+k+"</td><td> %s </td><td> %s </td></tr>" 
                               % (utils.hex_to_string(DeviceA.get_parameter(k)).ljust(24," "),
                                  utils.hex_to_string(DeviceB.get_parameter(k)).ljust(24," ")))
            else:
                filehtml.write("<tr><td>"+v.ljust(40," ")+'</td><td class="a">'+k+"</td><td> %s </td><td> %s </td></tr>" 
                               % (IOParameterOptions[k][int(utils.hex_to_string(DeviceA.get_parameter(k)),16)].ljust(24," "),
                                  IOParameterOptions[k][int(utils.hex_to_string(DeviceB.get_parameter(k)),16)].ljust(24," ")))
        filehtml.write('</tbody>\n')
        filehtml.write("</table>\n")
        filehtml.write('</body>')
        filehtml.close()
    except Exception as e:
        print(e)
        filehtml.write("Error reading settings...")
        filehtml.close()
        return(-1)                                                                                 
    return(0) 



def opener(path,flags):
    return os.open(path,flags,0o777)

def openDatafile(dataFilename):
    try:
        open(f"{webroot}/{dataFilename}.html",'x', opener=opener)
        logger.info(f" file doesnt exist, Creating file {dataFilename}.html in webroot of pi")
        with open(f"{webroot}/{dataFilename}.html", 'w', opener=opener) as f:
            writer = csv.writer(f)
            headers = ["Date", "Time", "power", "current", "voltage", "power factor" , "Temp", "tempKoelkast"]
            writer.writerow(headers)
    except Exception as e:
        print(e)
        logger.info(f"{dataFilename}.csv exists in webroot, appending with new data.")
    f = open(f"{webroot}/{dataFilename}.csv",'a',1,opener=opener)
    return f

def savehtml(filename="defaulthtml"):
    htmldata = data2list(data)
    htmldata = htmldata.replace("<table>", f"<table border={border}")
    with open(f"{webroot}/XBeeData.html", "w", encoding="utf-8") as filehtml:
        filehtml.write(htmldata)
    try:
        open(f"{webroot}/XBeeData.html",'x', opener=opener)
    except Exception as e:
        logger.info(f"XBeeData.html exists in webroot, replacing with new data.")
    f = open(f"{webroot}/XBeeData.html",'a',1,opener=opener)
    return f
    #os.startfile("Simple.html")
 
def data2list(data):
    d = data.splitlines()[1:-1]
    d = [x.split(",") for x in d]
    for row in d:
        for e in row:
            e_index = row.index(e)
            cell = "<td>" + e.strip() + "</td>"
            if e_index == 0:
                d[d.index(row)][row.index(e)] = "<tr>" + cell
            elif e_index == len(row) -1:
                d[d.index(row)][row.index(e)] = cell + "</tr>"
            else:
                d[d.index(row)][e_index] = cell
    d = [i for sublist in d for i in sublist]
    return "<table>" + "".join(d) + "</table>"
 
 
# ============== Persolized data ================
border = 1
data = """
Impiegato,      Performance,    data
Rossi Mario,    1000,           1/2/2018
Baldo Franco,   2000,           1/2/2018
    """
#savehtml(filename="Simple.html")


   
# main program
try:

    os.system("sudo systemctl stop serial-getty@ttyS0.service")
    print ("opening zigbee device ")
    #device = ZigBeeDevice('/dev/ttyS0',9600)
    device  = ZigBeeDevice("/dev/ttyUSB0", 9600)

    device.open()
    print ("Device opened...")
    
    print("Address = " + str(device.get_64bit_addr()))
    print("Hardware version = " + str(device.get_hardware_version()))
    print("Firmware version = " + utils.hex_to_string(device.get_firmware_version()))
    print("Protocol is " + str(device.get_protocol()))
    
    PrintXbeeSettings(device)
    PrintXbeeSettingsHTML(device)
    
    # Set Router device using network discovery

    xbeenet = device.get_network()
    xbeenet.start_discovery_process()
    while xbeenet.is_discovery_running():
        timelib.sleep(0.1)
    nodes = xbeenet.get_devices()
    if nodes:
        print("The number of remode nodes is %s ..." %str(len(nodes)))
        remote = RemoteXBeeDevice(device, nodes[0].get_64bit_addr())
        print("Remote address = "+ str(remote.get_64bit_addr()))
        PrintXbeeSettings(remote)
        PrintXbeeSettingsHTML2(device,remote)
    else:
        print("There are no remote nodes...")
    
except Exception as e:
    print("Some Error Has Occurred...")
    print(e)

if device is not None and device.is_open():
	device.close()
exit(0)