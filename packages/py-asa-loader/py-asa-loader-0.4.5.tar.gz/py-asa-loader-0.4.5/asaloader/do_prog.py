# -*- coding: utf-8 -*-
from asaloader.loader import Loader
from asaloader.device import device_list
from asaloader.locale import _
from asaloader import exceptions

import progressbar
import serial
import sys
import time
import math

def do_prog(args):

    ser = serial.Serial()
    ser.port = args.port
    ser.baudrate = 115200
    ser.timeout = 1
    try:
        ser.open()
    except:
        print(_('ERROR: com port has been opened by another application.').format(args.port))
        sys.exit(1)
    
    try:
        loader = Loader(
            ser = ser,
            device_type = args.device_type,
            is_flash_prog = args.is_prog_flash,
            is_eeprom_prog = args.is_prog_eep,
            is_go_app = args.is_go_app,
            flash_file = args.flash_file,
            eeprom_file = args.eep_file,
            go_app_delay = args.go_app_delay
        )
    except exceptions.ComuError:
        print(_("ERROR: Can't communicate with the device."))
        print(_("       Please check the comport and the device."))
        return
    except exceptions.CheckDeviceError as e:
        print(_("ERROR: Device is not match."))
        print(_("       Assigned device is '{0:s}'".format(device_list[e.in_dev]['name'])))
        print(_("       Detected device is '{0:s}'".format(device_list[e.real_dev]['name'])))
        return

    print(_("Device is '{0:s}'").format(device_list[loader.device_type]['name']))
    print(_('Flash  hex size is {0:0.2f} KB ({1} bytes)').format(loader.flash_size/1024, loader.flash_size))
    print(_('EEPROM hex size is {0} bytes。').format(loader.eeprom_size))
    print(_('Estimated time  is {0:0.2f} s。').format(loader.prog_time))

    widgets=[
        ' [', progressbar.Timer(_('Elapsed Time: %(seconds)0.2fs'), ), '] ',
        progressbar.Bar(),
        progressbar.Counter(format='%(percentage)0.2f%%'),
    ]
    
    bar = progressbar.ProgressBar(max_value=loader.total_steps, widgets=widgets)
    bar.update(0)
    for i in range(loader.total_steps):
        try:
            loader.do_step()
            bar.update(i)
        except exceptions.ComuError:
            print(_("ERROR: Can't communicate with the device."))
            print(_("Please check the comport is correct."))
            break
        except Exception:
            bar.finish(end='\n', dirty=True)
            print(_("ERROR: Can't communicate with the device."))
            print(_("Please check the comport is correct."))
            break
    
    bar.finish(end='\n')
    ser.close()
