# -*- coding:utf-8 -*-
""" Test script. """
# !/usr/bin/python
# Python:   3.6.5
# Platform: Windows/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Library for chipless reader.
# History:  2019-04-04 Wheel Ver:0.1 [Heyn] Initialization
#           2019-07-04 Wheel Ver:0.4 [Heyn]
#           2019-11-12 Wheel Ver:2.0 [Heyn] Not Supported v0.4.
#           2020-01-03 Wheel Ver:2.3 [Heyn] New add getEncoder() and getScan()

import struct
import pprint
import logging
from libclsprot import Protocol
from libclsprot import ChiplessTags

from libclsprot import CHIPLESS_ONLINE, CHIPLESS_OFFLINE

logging.basicConfig( level=logging.DEBUG )

INTERFACE_PORT = 'COM3'
INTERFACE_BAUDRATE = 460800
ANTENA_ARRAY_SIZE  = 9

ANTENA_ARRAY_KEYS = [ 'Antenna{}'.format(i) for i in range( 1, ANTENA_ARRAY_SIZE+1 ) ]

def module_notify( data ):
    print('Notify:')
    for items in data:
        pprint.pprint( items )      # Item is a dictionary type.
        print(len(items['data']))
        # Offline protocol.
        if 'weight' in items.keys():
            print( list( map( lambda  x : ((x & 0xFFFF) ^ items['weight'] ) & 0x00FF, items['data'] ) ) )

try:
    CHIPLESSPRT = ChiplessTags(  )
    CHIPLESSPRT.connect( INTERFACE_PORT, INTERFACE_BAUDRATE )
    CHIPLESSPRT.notify_callback( module_notify )
    CHIPLESSPRT.worker_start()
    print( '<OK> Port:{}, Baudrate:{}bps'.format(INTERFACE_PORT, INTERFACE_BAUDRATE) )
except BaseException as err:
    print( '<NG> Port:{}, Baudrate:{}bps'.format(INTERFACE_PORT, INTERFACE_BAUDRATE) )
    import sys
    sys.exit()

# print( CHIPLESSPRT.readRegister ( address=0x1000, size=5 ) )
# print( CHIPLESSPRT.writeRegister( address=0x1000, data=b'\x01\x02\x03\x04\x00\x05' ) )
# print( CHIPLESSPRT.synchronize() )

# print( CHIPLESSPRT.scan( antenna=16, sac=0x1234 ) )
# print( CHIPLESSPRT.scan( antenna=1, start=150, stop=1000, step=10 ) )
# print( CHIPLESSPRT.setEncoder( index=5, enable=True, coder=65535 ) )

# print( CHIPLESSPRT.gpio_output( index=1, enable=True, level=True ) )
# print( CHIPLESSPRT.gpio_output( index=2, enable=True, level=True ) )

# print( CHIPLESSPRT.gpio_input(  ) )

# print( CHIPLESSPRT.start()          )
# print( CHIPLESSPRT.mute()           )
# print( CHIPLESSPRT.setADC()            )

# MSG = CHIPLESSPRT.restart()
# MSG = CHIPLESSPRT.watchdog( True )
# MSG = CHIPLESSPRT.mute( False )
# MSG = CHIPLESSPRT.select( mode=chipless.OFFLINE )
# MSG = CHIPLESSPRT.online( ) # True:online False:offline
# MSG = CHIPLESSPRT.configure( index=1 )
# MSG = CHIPLESSPRT.temperature( )
# MSG = CHIPLESSPRT.clocksource( ch1=2500, ch2=2500, ch3=2500 )
# MSG = CHIPLESSPRT.adc( frequency=1000, accuracy=12, filter=True, voltage=2500, gain=6 )

# MSG = CHIPLESSPRT.getEncoder( )
# for i in range( 16 ):
#     values = struct.unpack( '>HHHHH',    MSG[1][ i*10 : (i+1)*10 ] )
#     print( values )

# MSG = CHIPLESSPRT.getScan(  )
# for i in range( 4 ):
#     values = struct.unpack( '>HHHHHHHH', MSG[1][ i*16 : (i+1)*16 ] )
#     print(values)

#### Ver:0.4
TEST_FRAME1 = b'\xAA\x80\x00\x00\x00\x0B\x01\xFF\x00\x64\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\xBB\xC0\x55'
TEST_FRAME2 = b'\xAA\x80\x00\x00\x00\x0B\x10\xFF\x00\x65\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x47\xFD\x55'
TEST_FRAME3 = b'\xAA\x81\x00\x00\x00\x0B\x01\xFF\x00\x00\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x2A\x7A\x55'

### Ver:0.5
# OnLine
TEST_FRAME4 = b'\xAA\x80\x00\x00\x00\x0C\x01\x0A\x00\x64\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\x2C\xE1\x55'

# OffLine
TEST_FRAME5 = b'\xAA\x81\x00\x00\x00\x06\x00\x0F\xF2\xD3\xF3\xD7\xFE\xD6\xF7\xD0\xFB\xD4\x90\x54\x55'

CHIPLESSPRT.unpackage( TEST_FRAME5, CHIPLESS_OFFLINE )

TEST_FRAME6 = b'\xAA\x80\x00\x00\x00\x5c\x01\x5a\x00\x64\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\x99\x99\x88\x88\x77\x77\x66\x66\x55\x55\x44\x44\x33\x33\x22\x22\x11\x11\x00\x00\xa7\x53\x55'
CHIPLESSPRT.unpackage(TEST_FRAME6, CHIPLESS_ONLINE)
