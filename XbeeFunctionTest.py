# Flash Firmware 4061 for XB24Cz7wit-004 XBEE modules, set parameter to API Escape mode [2]
#
# Place Module for Coordinator in top USB slot /dev/ttyUSB0
# Place Module for Router in bottom USB slot /dev/ttyUSB1
#
# PAN-ID = studienummer student
#
# Jan van Hulzen 02-09-2022 V1.0
#



import Xbee
import os
import time as timelib
from digi.xbee.devices import RemoteXBeeDevice, ZigBeeDevice
from digi.xbee.util import utils
import sys

mode=['',''] #default
device=None
device1=None

try:
    print("Number of parameters given :", len(sys.argv) )
    
    if len(sys.argv)==1:
        mode=['usb','read'] 
    elif len(sys.argv)>1:
        if sys.argv[1]=='-usb2':
            mode[0]='usb2'
        elif sys.argv[1]=='-usb':
            mode[0]='usb'
        elif sys.argv[1]=='-gpio':
            mode[0]='gpio'
        elif sys.argv[1]=='-?':
            print("First parameter %s is unknown ..." %sys.argv[1] )
            print("Use Python3 XbeeFunctionTest.py -[usb (default),usb2,gpio] -[r (default),w=number]")
            exit(-1)
    if len(sys.argv)==3:
        if sys.argv[2].strip('-ead')=='r':
                mode[1]='read'
                if sys.argv[1]=='-usb':
                    mode[0]='usb'
                elif sys.argv[1]=='-gpio':
                    mode[0]='gpio'
        elif sys.argv[2].strip('-0123456789rite=')=='w':
                mode[1]='write'
                mode[0]='usb2' # writing is for usb2 for now
                studienummer=int(sys.argv[2].strip('-abcdefghijklmnopqrstuvwxyz='),10)
                print("Writing to two devices with PanID %i..." %studienummer)
        else:
            print("Second parameter %s is unknown ..." %sys.argv[2] )
            print("Use Python3 XbeeFunctionTest.py -[usb (default),usb2,gpio] -[r (default),w=number]")
            exit(-1)        
except Exception as e:
    print("Error occured in parsing command...")
    print(e)
    print("Arguments: %s and %s unknown..." %(sys.argv[1],sys.argv[2]) )
    print("Use Python3 XbeeFunctionTest.py -[usb (default),usb2,gpio] -[r (default),w=number]")
    exit(-1)
    
# main program
try:
    os.system("sudo systemctl stop serial-getty@ttyS0.service")
    if mode[0]=='gpio':
        device = ZigBeeDevice('/dev/ttyS0',9600)
        device.open()
        print(" Opening device on GPIO UART bus device /dev/ttyS0 at 9600")
    elif mode[0]=='usb': 
        print("Opening one device...",mode[0])
        device  = ZigBeeDevice("/dev/ttyUSB0", 9600)
        device.open()
        print(" Opening device on USB serial device /dev/ttyUSB0 at 9600")
    elif mode[0]=='usb2':
        print("Opening two devices...",mode[0])
        device = ZigBeeDevice("/dev/ttyUSB0", 9600)
        device.open()
        device1 = ZigBeeDevice("/dev/ttyUSB1", 9600)
        device1.open()
        print(" Opening devices on USB serial device /dev/ttyUSB0 and /dev/ttyUSB1 at 9600")
    else:
        print("Error: no device to open...")
        print("USB serial devices found : %s" % os.system('ls /dev/ttyUSB*'))
        exit(-1)    
    if device is not None and device.is_open():
        print(" Device opened...")
        print("+--------------------------------------------------------------------------+")
        print(" Address node 0      = " + str(device.get_64bit_addr()))
        print(" Hardware version    = " + str(device.get_hardware_version()))
        print(" Firmware version    = " + utils.hex_to_string(device.get_firmware_version()))
        print(" Protocol node 0     = " + str(device.get_protocol()))
        if device1 is not None and device1.is_open():
            print(" Device opened...")
            print("+--------------------------------------------------------------------------+")
            print(" Address remote node = " + str(device1.get_64bit_addr()))
            print(" Hardware version    = " + str(device1.get_hardware_version()))
            print(" Firmware version    = " + utils.hex_to_string(device1.get_firmware_version()))
            print(" Protocol node 0     = " + str(device1.get_protocol()))
    
        if mode[1]=='read':
            print("Reading settings on Node 0...")
            Xbee.PrintXbeeSettings(device)
            Xbee.PrintXbeeSettingsHTML(device)
            
            # Set Router device using network discovery

            xbeenet = device.get_network()
            xbeenet.start_discovery_process()
            while xbeenet.is_discovery_running():
                timelib.sleep(0.1)
            nodes = xbeenet.get_devices()
            if nodes:
                print("  Nr of remote nodes  = %s" %str(len(nodes)))
                remote = RemoteXBeeDevice(device, nodes[0].get_64bit_addr())
                print("  Address remote node = "+ str(remote.get_64bit_addr()))
                Xbee.PrintXbeeSettings(remote)
                Xbee.PrintXbeeSettingsHTML2(device,remote)
            else:
                print("There are no remote nodes...")
        elif mode[1].strip('-0123456789rite')=='w':
                Xbee.DetectXbeeHardAndFirmware(device)
                Xbee.DetectXbeeHardAndFirmware(device1)
                print("Pan id number %i set" %studienummer)
                Xbee.PairDevices(device,device1,studienummer)
                Xbee.SetXbeeSettings(device,Xbee.IOParameterValuesCoordinator)
                Xbee.SetXbeeSettings(device1,Xbee.IOParameterValuesRouter)
                # Set Router device using network discovery
                print("Resetting network starting with coordinator...")
                device.reset()
                timelib.sleep(1)
                device1.reset()
                print("Wait 10 s for network to reset...")
                timelib.sleep(10)
                print("Start Network discovery...")
                xbeenet = device.get_network()
                xbeenet.start_discovery_process()
                while xbeenet.is_discovery_running():
                    timelib.sleep(0.1)
                nodes = xbeenet.get_devices()
                if nodes:
                    print("The number of remode nodes is %s ..." %str(len(nodes)))
                    remote = RemoteXBeeDevice(device, nodes[0].get_64bit_addr())
                    print("Remote address = "+ str(remote.get_64bit_addr()))
                    Xbee.PrintXbeeSettings2Devices(device,remote)
                else:
                    print("There are no remote nodes...")
                    Xbee.PrintXbeeSettings2Devices(device,device1)
        else:
            print("Error, %s is an invalid second parameter..." % mode[1] )
            exit(-1)
    else:
        print("Error opening device, try resetting module...")
        exit(-1)

except Exception as e:
    print("Some Error Has Occurred...")
    print(e)
    #if e=='Unsupported operating mode: AT mode':
    device.close()
    Xbee.command_mode("/dev/ttyUSB0",'ATAP1\r')
    device1.close()
    Xbee.command_mode("/dev/ttyUSB1",'ATAP1\r')
    print('attempting reset')

if device is not None and device.is_open():
	device.close()
if device1 is not None and device1.is_open():
	device.close()
exit(0)