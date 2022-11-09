# Flash Firmware 4061 for XB24Cz7wit-004 XBEE modules, set parameter to API Escape mode [2]
#
# Place Module for Coordinator in top USB slot /dev/ttyUSB0
# Place Module for Router in bottom USB slot /dev/ttyUSB1
#
# PAN-ID = studienummer student
#
# Jan van Hulzen 02-09-2022 V1.0
#

import time as timelib
from datetime import datetime
import os
from digi.xbee.devices import DigiMeshDevice, RemoteXBeeDevice, XBeeDevice , ZigBeeDevice
from digi.xbee.io import IOLine
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.models.mode import APIOutputModeBit
from digi.xbee.util import utils

NetworkParameters=dict([("ID","PAN ID "),("SC","Scan Channels" ),("SD","Scan Duration"),("ZS","Zigbee Stack Profile"),("NJ","Node Joint Time"),
      ("OP","Operating PAN ID"),("OI","Operating 16 Bit PAN ID"),("CH","Operating Channel"),("NC","Number of remaining children"),
      ("CE","Coordinator Enable")])

AddressingParameters = dict([("SH","Serial Number High"),("SL","Serial Number Low"),("MY","16 Bit Network Address"),("DH","Desitination Address High"),
                             ("DL","Desitination Address Low"),("NI","Node Identifier"),("NH","Maximum number op hops"),("BH","Broadcast Radius"),
                             ("AR","Many-To-One Broadcast Time"),("DD","Device Type Identifier"),("NT","Node Discovery BackOff"),
                             ("NO","Node Discovery Options"),("NP","Maximum Number of API Transmission Bytes"),("CR","PAN Conflict Threshold")])

IOParameters = dict([("D0","AD0/DIO0 Configuration"),("D1","AD1/DIO1 Configuration"),("D2","AD2/DIO2 Configuration"),("D3","AD3/DIO3 Configuration"),
                     ("D4","DIO4 Configuration"),("D5","DIO5/Assoc Configuration "),("P0","DIO10/PWM0 Configuration"),("P1","DIO11 Configuration"),("P2","DIO12 Configuration"),("PR","Pull-up Resistor Enable"),("LT","Associate LED Blink Time"),("RP","RSSI PWM Timer"),
                     ("DO","Device Options "),("DC","Device Controls "),("IR","IO Sampling Rate")])

IOParameterValuesRouter = dict([("D0","02"),("D1","00"),("D2","00"),("D3","00"),("D4","00"),("D5","01"),("P0","01"),("P1","00"),("P2","00"),
                                ("PR","1FBF"),("LT","00"),("RP","28"),("DO","08"),("DC","20"),("IR","03E8")])

IOParameterValuesCoordinator = dict([("D0","00"),("D1","00"),("D2","00"),("D3","00"),("D4","00"),("D5","01"),("P0","01"),("P1","00"),("P2","00"),
                                ("PR","1FBF"),("LT","00"),("RP","28"),("DO","08"),("DC","20"),("IR","0000")])
    
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
IOParameterOptions["DC"] = [ "NA" ]
IOParameterOptions["IR"] = [ "NA" ]

def PrintXbeeSettings(device:ZigBeeDevice):
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

def PrintXbeeSettings2Devices(Coordinator:ZigBeeDevice,Router:ZigBeeDevice):
    try:
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+".ljust(27,"-")+"+")
        for k,v in NetworkParameters.items():
            print("|",v.ljust(40," "),"|",k,"| %s | %s |" % (utils.hex_to_string(Coordinator.get_parameter(k)).ljust(24," ") , utils.hex_to_string(Router.get_parameter(k)).ljust(24," ")))
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+".ljust(27,"-")+"+")
        for k,v in AddressingParameters.items():
            if k=="NI":
                print("|",v.ljust(40," "),"|",k,"|%s  |%s  |" % (Coordinator.get_parameter(k).decode().ljust(24," ") , Router.get_parameter(k).decode().ljust(24," ")))
            else:
                print("|",v.ljust(40," "),"|",k,"| %s | %s |" % (utils.hex_to_string(Coordinator.get_parameter(k)).ljust(24," ") , utils.hex_to_string(Router.get_parameter(k)).ljust(24," ")))
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+".ljust(27,"-")+"+")
        for k,v in IOParameters.items():
            if IOParameterOptions[k][0]=="NA":
                print("|",v.ljust(40," "),"|",k,"| %s | %s |" % (utils.hex_to_string(Coordinator.get_parameter(k)).ljust(24," ") , utils.hex_to_string(Router.get_parameter(k)).ljust(24," ")))
            else:
                print("|",v.ljust(40," "),"|",k,"| %s | %s |" % (IOParameterOptions[k][int(utils.hex_to_string(Coordinator.get_parameter(k)),16)].ljust(24," ") , IOParameterOptions[k][int(utils.hex_to_string(Router.get_parameter(k)),16)].ljust(24," ")))
        print("+".ljust(43,"-")+"+----+".ljust(32,"-")+"+".ljust(27,"-")+"+")
    except:
        print("Error reading settings...")
        return(-1)                                                                                 
    return(0)  


def SetXbeeSettings(device:ZigBeeDevice,Parameters:dict):
    try:
        for k,v in Parameters.items():
            device.set_parameter(k,bytearray.fromhex(v))
        device.apply_changes()
        device.write_changes()
    except Exception as e:
        print("Setting parameters failed...")
        print(e)
        return(-1)
    finally:                                                                                 
        return(0) 


def DetectXbeeHardAndFirmware(device:ZigBeeDevice):
    try:
        print("|Hardware version".ljust(43," ")+"|    |%s|" % str(device.get_hardware_version()).ljust(32," "))
        print("|Firmware version".ljust(43," ")+"|    |%s|" % utils.hex_to_string(device.get_firmware_version()).ljust(32," "))
        print("|Protocol".ljust(43," ")+"|    |%s|" % str(device.get_protocol()).ljust(32," "))
        print("|Operating Mode".ljust(43," ")+"|    |%s|" % str(device._get_operating_mode()).ljust(32," "))
        print("Address = " + str(device.get_64bit_addr()))
    except Exception as e:
        print("Hard and Firmware detection failed...")
        print(e)
        return(-1)
    finally:                                                                                 
        return(0) 
    
def SetUpAsCoordinator(device:ZigBeeDevice):
    try:
        print(device._get_operating_mode())
        print("Address = " + str(device.get_64bit_addr()))
        print("Hardware version = " + str(device.get_hardware_version()))
        print("Firmware version = " + utils.hex_to_str(device.get_firmware_version()))
        print("Protocol is " + str(device.get_protocol()))
    except:
        print("Set up as coordinator failed...")
        return(-1)
    finally:                                                                                 
        return(0) 

def PairDevices(Coordinator:ZigBeeDevice,Router:ZigBeeDevice,studienummer:int):
    try:
        Router.set_pan_id(bytearray([0,0]+list(map(int,str(studienummer)))))
        #Router.set_pan_id(bytearray.fromhex("0000DDCD"))
        Router.set_parameter("DH",bytearray.fromhex("00000000"))
        Router.set_parameter("DL",bytearray.fromhex("00000000"))
        Router.set_parameter("CE",bytearray.fromhex("00"))
        Router.apply_changes()
        Router.write_changes()
        
        Coordinator.set_pan_id(bytearray([0,0]+list(map(int,str(studienummer)))))
        #Coordinator.set_pan_id(bytearray.fromhex("0000DDCD"))
        Coordinator.set_parameter("DH",bytearray.fromhex("0013A200"))
        Coordinator.set_parameter("DL",Router.get_parameter("SL"))
        Coordinator.set_parameter("CE",bytearray.fromhex("01"))
        Coordinator.apply_changes()
        Coordinator.write_changes()   
    except Exception as e:
        print("Pairing Devices Failed...")
        print(e)
        return(-1)
    finally:                                                                                 
        return(0) 

try:

    os.system("sudo systemctl stop serial-getty@ttyS0.service")
    print ("opening zigbee device ")
    #device = ZigBeeDevice('/dev/ttyS0',9600) # uncomment for GPIO
    Coordinator  = ZigBeeDevice("/dev/ttyUSB0", 9600)
    Router  = ZigBeeDevice("/dev/ttyUSB1", 9600)
    
    Coordinator.open()
    Router.open()
    print ("Devices opened...")
    DetectXbeeHardAndFirmware(Coordinator)
    DetectXbeeHardAndFirmware(Router)
    
    studienummer=123457
    PairDevices(Coordinator,Router,studienummer)
    
    
    SetXbeeSettings(Coordinator,IOParameterValuesCoordinator)
    SetXbeeSettings(Router,IOParameterValuesRouter)
    
    #PrintXbeeSettings(Coordinator)
    #PrintXbeeSettings(Router)
    #PrintXbeeSettings2Devices(Coordinator,Router)
    
    # Set Router device using network discovery
    print("Resetting network starting with coordinator...")
    Coordinator.reset()
    timelib.sleep(1)
    Router.reset()
    print("Wait 10 s for network to reset...")
    timelib.sleep(10)
    print("Start Network discovery...")
    xbeenet = Coordinator.get_network()
    xbeenet.start_discovery_process()
    while xbeenet.is_discovery_running():
        timelib.sleep(0.1)
    nodes = xbeenet.get_devices()
    if nodes:
        print("The number of remode nodes is %s ..." %str(len(nodes)))
        remote = RemoteXBeeDevice(Coordinator, nodes[0].get_64bit_addr())
        print("Remote address = "+ str(remote.get_64bit_addr()))
        PrintXbeeSettings2Devices(Coordinator,remote)
    else:
        print("There are no remote nodes...")
        PrintXbeeSettings2Devices(Coordinator,Router)
 
except Exception as e:
    print("Some Error Has Occurred...")
    print(e)

if Coordinator is not None and Coordinator.is_open():
	Coordinator.close()
if Router is not None and Router.is_open():
	Router.close()
exit(0)