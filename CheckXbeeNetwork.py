
#!/usr/bin/python
# scp "/Users/janvanhulzen/Documents/Courses/Inholland/project11/Editie_20212022/ProjectRPI.nosync/setup local L027/testxbee3.py" pi@studentpi.local:
#
# Script voor de controle van Xbee settings (Zigbee protocol) voor project11
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


XbeeNetworkParameters=dict([("ID","PAN ID "),("OP","Operating PAN ID"),("OI","Operating 16 Bit PAN ID"),("CH","Operating Channel"),
                            ("CE","Coordinator Enable"),("SH","Serial Number High"),("SL","Serial Number Low"),("DH","Desitination Address High"),
                             ("DL","Desitination Address Low"),("NI","Node Identifier"),("D0","AD0/DIO0 Configuration"),("D1","AD1/DIO1 Configuration"),
                             ("D2","AD2/DIO2 Configuration"),("D3","AD3/DIO3 Configuration"),("D4","DIO4 Configuration"),
                             ("D5","DIO5/Assoc Configuration "),("P0","DIO10/PWM0 Configuration"),("P1","DIO11 Configuration"),
                             ("P2","DIO12 Configuration"),("PR","Pull-up Resistor Enable"),("LT","Associate LED Blink Time"),
                             ("RP","RSSI PWM Timer")])
    
XbeeNetworkParameterOptions={}

XbeeNetworkParameterOptions["D0"] = [ "Disabled [0]","Commisioning Button [1]", "ADC [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
XbeeNetworkParameterOptions["D1"] = [ "Disabled [0]","NA [1]", "ADC [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
XbeeNetworkParameterOptions["D2"] = [ "Disabled [0]","NA [1]", "ADC [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
XbeeNetworkParameterOptions["D3"] = [ "Disabled [0]","NA [1]", "ADC [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
XbeeNetworkParameterOptions["D4"] = [ "Disabled [0]","NA [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
XbeeNetworkParameterOptions["D5"] = [ "Disabled [0]","Associated Indicator [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
XbeeNetworkParameterOptions["P0"] = [ "Disabled [0]","RSSI PWM Output [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
XbeeNetworkParameterOptions["P1"] = [ "Disabled [0]","RSSI PWM Output [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]
XbeeNetworkParameterOptions["P2"] = [ "Disabled [0]","RSSI PWM Output [1]", "NA [2]","Digital Input [3]","Digital Out, Low [4]","Digital Out, High [5]"]


def PrintXbeeSettings(device:ZigBeeDevice):
    try:
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+")
        for k,v in XbeeNetworkParameters.items():
            if k=="NI":
                print("|",v.ljust(40," "),"|",k,"|%s  |" % device.get_parameter(k).decode().ljust(24," "))
            elif k in XbeeNetworkParameterOptions:
                print("|",v.ljust(40," "),"|",k,"| %s |" % XbeeNetworkParameterOptions[k][int(utils.hex_to_string(device.get_parameter(k)),16)].ljust(24," "))
            else:
                print("|",v.ljust(40," "),"|",k,"| %s |" % utils.hex_to_string(device.get_parameter(k)).ljust(24," "))    
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+")
    except Exception as e:
        print("Error reading settings...")
        print(e)
        return(-1)                                                                                
    return(0)    

try:

    os.system("sudo systemctl stop serial-getty@ttyS0.service")
    print ("opening zigbee device ")
    device = ZigBeeDevice('/dev/ttyS0',9600)
    #device  = ZigBeeDevice("/dev/ttyUSB0", 9600)

    device.open()
    print ("Device opened...")
    
    print("Address = " + str(device.get_64bit_addr()))
    print("Hardware version = " + str(device.get_hardware_version()))
    print("Firmware version = " + utils.hex_to_string(device.get_firmware_version()))
    print("Protocol is " + str(device.get_protocol()))
    
    PrintXbeeSettings(device)
    
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
    else:
        print("There are no remote nodes...")
    
except Exception as e:
    print("Some Error Has Occurred...")
    print(e)
finally:
    if device is not None and device.is_open():
        device.close()
exit(0)