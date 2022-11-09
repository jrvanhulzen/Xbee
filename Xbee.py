#!/usr/bin/python
# Library voor XBEE functies project 11
# Jan van Hulzen : v1.0 19-8-2022
# Project 1.1

from digi.xbee.util import utils
from digi.xbee.devices import ZigBeeDevice
from digi.xbee.models.mode import APIOutputModeBit
from digi.xbee.util import utils

import serial
import time as timelib
from datetime import datetime



webroot = '/var/www/html'

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

IOParameterValuesRouter = dict([("D0","02"),("D1","02"),("D2","00"),("D3","00"),("D4","00"),("D5","01"),("P0","01"),("P1","00"),("P2","00"),
                                ("PR","1FBF"),("LT","00"),("RP","28"),("DO","08"),("DC","20"),("IR","03E8")])

IOParameterValuesCoordinator = dict([("D0","00"),("D1","00"),("D2","00"),("D3","00"),("D4","00"),("D5","01"),("P0","01"),("P1","00"),("P2","00"),
                                ("PR","1FBF"),("LT","00"),("RP","28"),("DO","08"),("DC","20"),("IR","0000")])
    

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
        Router.set_parameter("DH",bytearray.fromhex("00000000"))
        Router.set_parameter("DL",bytearray.fromhex("00000000"))
        Router.set_parameter("CE",bytearray.fromhex("00"))
        Router.apply_changes()
        Router.write_changes()
        
        Coordinator.set_pan_id(bytearray([0,0]+list(map(int,str(studienummer)))))
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

def PrintXbeeSettingsHTML(device:ZigBeeDevice):
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

def PrintXbeeSettingsHTML2(DeviceA:ZigBeeDevice,DeviceB:ZigBeeDevice):
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
   
def command_mode(port="/dev/ttyS0",command='ATAP1\r'):
    ser = serial.Serial(port,9600)
    for _ in range(10):  # Limit retry count
        timelib.sleep(0.1)
        ser.write("+".encode("ascii"))
        timelib.sleep(0.1)
        ser.write("+".encode("ascii"))
        timelib.sleep(0.1)
        ser.write("+".encode("ascii"))
        print("+++")
        receive = ser.read(ser.in_waiting)
        print(str(receive).find("OK"))
        if str(receive).find("OK") != -1:
            ser.write((command + "\r").encode("ascii"))
            break
    ser.close()
    
def ReadFiveSamples(device:ZigBeeDevice):
    try:
        device.set_api_output_mode_value(APIOutputModeBit.calculate_api_output_mode_value(device.get_protocol(), {APIOutputModeBit.EXPLICIT}))
        for index in range(5):
            xbee_message = device.read_expl_data(5)
            readoutA0 = xbee_message.data[4] << 8 | xbee_message.data[5]
            print("Sample "+str(index)+" at "+str(datetime.utcfromtimestamp(xbee_message.timestamp).strftime('%Y-%m-%d %H:%M:%S'))+" T = " + str(readoutA0))
    except Exception as e:
        print("Some Error Has Occurred...")
        print(e)
    return(0)
