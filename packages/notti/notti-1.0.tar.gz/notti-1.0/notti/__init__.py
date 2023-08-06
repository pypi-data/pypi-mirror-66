# Python module for control of Notti bluetooth lights
#
# Copyright 2020 Robin Cutshaw <robin@internetlabs.com>
#
# This code is released under the terms of the MIT license. See the LICENSE
# file for more details.

import sys
import time

from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate

class notti:
  def __init__(self, mac=None):
    self.mac = mac

  class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

  @classmethod
  def scan(self):
    # the scan method must be called with root level privileges
    nottis = []
    scanner = Scanner()
    try:
        devices = scanner.scan(5.0)
    except btle.BTLEDisconnectError:
        print ("Disconnected from the btle device")
    except AttributeError:
        print ("Disconnected from the btle device (Attribute Error)")
    except btle.BTLEManagementError:
        print ("Got root?")
    except:
        print ("Unknown exception from the btle device: ", sys.exc_info()[0])
    for dev in devices:
        scndata = dev.getScanData()
        for (adtype, desc, value) in scndata:
            if desc == 'Complete Local Name' and value.find('Notti') >= 0:
                nottis.append([value, dev.addr])
    return nottis

  def set_state(self, red, green, blue):
    self.red = red
    self.green = green
    self.blue = blue
    if red == 0 and green == 0 and blue == 0:
      self.power = False
    else:
      self.power = True

  def connect(self):
    initial = time.time()

    while True:
      if time.time() - initial >= 10:
        return False
      try:
        self.device = btle.Peripheral(self.mac, addrType=btle.ADDR_TYPE_PUBLIC)
        break
      except btle.BTLEDisconnectError:
        print ("Cannot connect to the btle device")
      except:
        print ("Cannot connect to the btle device: ", sys.exc_info()[0])
        return

    handles = self.device.getCharacteristics()
    for handle in handles:
      if handle.uuid.getCommonName() == "fff3":
        self.rgbhandle = handle
      elif handle.uuid.getCommonName() == "fff4":
        self.fff4handle = handle
      elif handle.uuid.getCommonName() == "fff5":
        self.fff5handle = handle
      elif handle.uuid.getCommonName() == "fff6":
        self.fff6handle = handle
      elif handle.uuid.getCommonName() == "Device Name":
        self.devicename = handle
      elif handle.uuid.getCommonName() == "Appearance":
        self.appearance = handle
      elif handle.uuid.getCommonName() == "Peripheral Privacy Flag":
        self.peripheralprivacyflag = handle
      elif handle.uuid.getCommonName() == "Reconnection Address":
        self.reconnectionaddress = handle
      elif handle.uuid.getCommonName() == "Peripheral Preferred Connection Parameters":
        self.ppcp = handle
      elif handle.uuid.getCommonName() == "Service Changed":
        self.servicechanged = handle
      elif handle.uuid.getCommonName() == "System ID":
        self.systemid = handle
      elif handle.uuid.getCommonName() == "Model Number String":
        self.modemnumberstring = handle
      elif handle.uuid.getCommonName() == "Serial Number String":
        self.serialnumberstring = handle
      elif handle.uuid.getCommonName() == "Firmware Revision String":
        self.firmwarerevisionstring = handle
      elif handle.uuid.getCommonName() == "Hardware Revision String":
        self.hardwarerevisionstring = handle
      elif handle.uuid.getCommonName() == "Software Revision String":
        self.softwarerevisionstring = handle
      elif handle.uuid.getCommonName() == "Manufacturer Name String":
        self.manufacturernamestring = handle
      elif handle.uuid.getCommonName() == "IEEE 11073-20601 Regulatory Certification Data List":
        self.ieeercdl = handle
      elif handle.uuid.getCommonName() == "PnP ID":
        self.pnpid = handle
      elif handle.uuid.getCommonName() == "Battery Level":
        self.batterylevel = handle
      else:
         print("unknown device characteristic: ", handle.uuid.getCommonName())

    self.set_state(0, 0, 0)
    self.power = False

  def send_packet(self, handle, data):
    initial = time.time()
    while True:
      if time.time() - initial >= 10:
        return False
      try:
        return handle.write(bytes(data), withResponse=True)
      except:
        self.connect()

  def off(self):
    self.power = False
    self.red = 0
    self.green = 0
    self.blue = 0
    packet = bytearray([0x06, 0x01, self.red, self.green, self.blue])
    self.send_packet(self.rgbhandle, packet)

  def on(self):
    self.power = True
    self.red = 255
    self.green = 255
    self.blue = 255
    packet = bytearray([0x06, 0x01, self.red, self.green, self.blue])
    self.send_packet(self.rgbhandle, packet)

  def set_rgb(self, red, green, blue):
    self.red = red
    self.green = green
    self.blue = blue
    packet = bytearray([0x06, 0x01, self.red, self.green, self.blue])
    self.send_packet(self.rgbhandle, packet)

  def set_white(self, white):
    self.red = 255
    self.green = 255
    self.blue = 255
    packet = bytearray([0x06, 0x01, self.red, self.green, self.blue])
    self.send_packet(self.rgbhandle, packet)

  def get_on(self):
    return self.power

  def get_colour(self):
    return (self.red, self.green, self.blue)
