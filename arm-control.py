import ui

import cb
import sound
import time
import struct

class BluetoothManager (object):
    def __init__(self):
        self.peripheral = None
        self.ready = False
        self.c = None
        self.print_ready = True

    def did_discover_peripheral(self, p):
        if p.name:
            if p.name == "HMSoft" or p.name == "Test":
                print(p.name)
                self.peripheral = p
                print('Connecting...')
                cb.connect_peripheral(p)

    def did_connect_peripheral(self, p):
        print('Connected:', p.name)
        print('Discovering services...')
        p.discover_services()

    def did_fail_to_connect_peripheral(self, p, error):
        print('Failed to connect: %s' % (error,))

    def did_disconnect_peripheral(self, p, error):
        print('Disconnected, error: %s' % (error,))
        self.peripheral = None

    def did_discover_services(self, p, error):
        for s in p.services:
            print(s.uuid)
            if (s.uuid == 'FFE0'):
                print('Service discovered')
                p.discover_characteristics(s)

    def did_discover_characteristics(self, s, error):
        print('Did discover characteristics...')
        for c in s.characteristics:
            print(c.uuid)
            if c.uuid == 'FFE1':
                self.ready = True
                self.c = c
                

    def did_update_value(self, c, error):
        heart_rate = struct.unpack('<B', c.value[1])[0]
        self.values.append(heart_rate)
        print('Heart rate: %i' % heart_rate)

mngr = BluetoothManager()
cb.set_central_delegate(mngr)
print('Scanning for peripherals...')
cb.scan_for_peripherals()

def write_values(data):
    if mngr.ready and mngr.print_ready:
        print(data)
        mngr.peripheral.write_characteristic_value(mngr.c, data + '\n', False)
        mngr.print_ready = False
        ui.delay(set_ready, 0.1)

        
def set_ready():
    mngr.print_ready = True
    
def waist_action(sender):
    write_values("Waist:" + str(int(sender.value*1000)))
    
def shoulder_action(sender):
    write_values("Shoulder:" + str(int(sender.value*1000)))
    
def elbow_action(sender):
    write_values("Elbow:" + str(int(sender.value*1000)))
    
def roll_action(sender):
    write_values("Roll:" + str(int(sender.value*1000)))

def pitch_action(sender):
    write_values("Pitch:" + str(int(sender.value*1000)))

def grab_action(sender):
    write_values("Grab:" + str(int(sender.value*1000)))

while (not mngr.ready):
	pass

v = ui.load_view()
v.present('sheet')
