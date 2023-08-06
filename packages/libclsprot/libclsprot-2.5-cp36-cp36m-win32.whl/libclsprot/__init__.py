# -*- coding:utf-8 -*-
""" Library for chipless reader. """
# !/usr/bin/python
# Python:   3.6.5
# Platform: Windows/Linux
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Library for chipless reader.
# History:  2019-01-17 Wheel Ver:0.1 [Heyn] Initialization
#           2019-01-23 Wheel Ver:0.2 [Heyn] New Protocols.
#           2019-01-30 Wheel Ver:0.2 [Heyn] New add class ChiplessProtocolFactory and ChipLessTags
#           2019-04-04 Wheel Ver:0.3 [Heyn] New __del__() and worker_stop() functions.
#           2019-06-24 Wheel Ver:0.4 [Heyn] New scan serial port functions.
#           2019-07-04 Wheel Ver:0.4 [Heyn] New select and configure functions.
#           2019-08-16 Wheel Ver:0.6 [heyn] New add ChiplessProtocolFactory.connection_lost()
#                                           New add ChiplessTags.worker_close() function
#           2019-08-21 Wheel Ver:1.0 [Heyn] New add windows platform (set_buffer_size)
#           2019-11-12 Wheel Ver:2.0 [Heyn] New add offline protocol & Not Supported v0.4 protocol.
#           2019-12-10 Wheel Ver:2.1 [Heyn] New add online function.
#           2019-12-13 Wheel Ver:2.1 [Heyn] Modified restart function.
#           2019-12-26 Wheel Ver:2.3 [Heyn] New add uuid & version function.
#           2020-01-03 Wheel Ver:2.4 [Heyn] New add getEncoder() and getScan()
#           2020-01-15 Wheel Ver:2.5 [Heyn] Dynamic modification protocol type( ONLINE or OFFLINE )

__author__    = 'Heyn'
__version__   = '2.4'

import os
import queue
import serial
import logging
import serial.threaded
import serial.tools.list_ports

from struct import unpack
from libclsprot import chipless
from libclsprot.chipless import Protocol

CHIPLESS_ONLINE   = chipless.ONLINE
CHIPLESS_OFFLINE  = chipless.OFFLINE

class ChiplessProtocolFactory( serial.threaded.FramedPacket ):
    def __init__(self, unpack=None, disconnect=None, protocol=chipless.ONLINE ):
        super( ChiplessProtocolFactory, self ).__init__()
        self.__protocol  = protocol        # See self.select( ... ) function.
        self.transport   = None
        self.__unpackage = unpack
        self.__disconnect= disconnect

    def __call__( self ):
        return self

    def connection_made( self, transport ):
        """Store transport"""
        self.transport = transport

    def protocol( self, value=chipless.ONLINE  ):
        self.__protocol = value

    def data_received( self, data ):
        self.__unpackage( data, self.__protocol )
    
    def connection_lost( self, exc ):
        self.__disconnect()
        self.transport = None
        logging.debug( 'connection_lost' )
        super( ChiplessProtocolFactory, self ).connection_lost(exc)

def register_uart_write( func ):
    def wrapper( self, *args, **kwargs ):
        payload = func( self, *args, **kwargs )
        logging.debug( 'UART->Tx: {}'.format(' '.join([ hex(i) for i in payload ])) )
        try:
            self.ser.write( payload )
            result = self.response_queue.get( timeout=3 )
        except BaseException as err:
            return ( False, err )
        return result
    return wrapper

class ChiplessTags( Protocol ):
    """."""
    def __init__( self, mode=chipless.ONLINE ):
        super( ChiplessTags, self ).__init__()
        self.ser = None
        self.mode = mode        # See self.select( ... ) function.
        self.serial_worker = None
        self.response_queue = queue.Queue(2048)

    def scan_serial_port( self, description='COM' ):
        """
            device[0] : COMxx
            device[1] : Prolific USB-to-Serial Comm Port (COMxx)
            device[2] : USB VID:PID=067B:2303 SER=6 LOCATION=1-1.1
            ver0.2 -> 2019-04-30
        """
        for device in list( serial.tools.list_ports.comports() ):
            if description in device[1]:
                yield device[0]

    def connect( self, port='COM1', baudrate=115200 ):
        self.ser = serial.serial_for_url( port, do_not_open=True )
        self.ser.baudrate, self.ser.bytesize = baudrate, 8
        self.ser.parity, self.ser.stopbits = serial.PARITY_NONE, serial.STOPBITS_ONE

        try:
            self.ser.open( )
            if os.name == 'nt':  # sys.platform == 'win32':
                self.ser.set_buffer_size( 1024*10 )
        except BaseException as err:
            raise FileNotFoundError('Could not open serial port {}: {}'.format(self.ser.name, err))

        return True

    def __del__( self ):
        self.worker_close()

    def __response_callback( self, ret, data ):
        self.response_queue.put( ( ret, data ) )
        logging.debug( 'UART->Rx: {}'.format(' '.join([ hex(i) for i in data ])) )

    def notify_callback( self, func ):
        super( ChiplessTags, self ).notify_callback( func )

    @register_uart_write
    def readRegister( self, address, size ):
        return super( ChiplessTags, self ).rregister( address=address, size=size )

    @register_uart_write
    def writeRegister( self, data, address ):
        return super( ChiplessTags, self ).wregister( data=data, address=address )

    @register_uart_write
    def start( self ):
        return super( ChiplessTags, self ).start()

    @register_uart_write
    def stop( self ):
        return super( ChiplessTags, self ).stop()

    @register_uart_write
    def version( self ):
        """ Chipless reader software version."""
        return super( ChiplessTags, self ).version()

    def restart( self ):
        payload = super( ChiplessTags, self ).restart()
        logging.debug( 'UART->Tx: {}'.format(' '.join([ hex(i) for i in payload ])) )
        try:
            self.ser.write( payload )
        except BaseException as err:
            return ( False, err )
        return ( True, 0 )

    @register_uart_write
    def mute( self, enable=False ):
        return super( ChiplessTags, self ).mute( enable )

    @register_uart_write
    def synchronize( self ):
        """ Synchronize background data. """
        return super( ChiplessTags, self ).synchronize( )

    @register_uart_write
    def gpio_output( self, index, enable=True, level=True ):
        return super( ChiplessTags, self ).gpio_output( index=index, enable=enable, level=level )

    @register_uart_write
    def gpio_input( self ):
        return super( ChiplessTags, self ).gpio_input( )

    @register_uart_write
    def scan( self, antenna=1, enable=True, start=100, stop=1000, step=10, threshold=1, power=2, sac=0, bandwidth=25  ):
        """
            enable    -    Antenna enable
            start     -    Starting frequency
            stop      -    Cutoff frequency
            step      -    Scan step
            threshold -    Limited threshold
            power     -    Phase-locked loop output power
            sac       -    Switch antenna controller.
            bandwidth -    Band width
        """
        return super( ChiplessTags, self ).scan( antenna   = antenna,
                                                 enable    = enable,
                                                 start     = start,
                                                 stop      = stop,
                                                 step      = step,
                                                 threshold = threshold,
                                                 power     = power,
                                                 sac       = sac,
                                                 bandwidth = bandwidth )

    @register_uart_write
    def getScan( self, index=1, size=8 ):
        """ Get antenna configure.
            TODO : Currently can only read up to four antenna configurations.
                   *** Invalid function parameter. See:STM32 source code.
        """
        return super( ChiplessTags, self ).getScan( index=index, size=size )

    @register_uart_write
    def temperature( self ):
        return super( ChiplessTags, self ).temperature()

    @register_uart_write
    def uuid( self ):
        return super( ChiplessTags, self ).uuid()

    @register_uart_write
    def clk_source( self, channel1=0, channel2=0, channel3=0 ):
        return super( ChiplessTags, self ).clocksource( ch1=channel1, ch2=channel2, ch3=channel3 )

    @register_uart_write
    def setADC( self, freq=1000, acc=12, filter=True, vol=2500, gain=2 ):
        return super( ChiplessTags, self ).adc( frequency = freq,
                                                accuracy  = acc,
                                                filter    = filter,
                                                voltage   = vol,
                                                gain      = gain )

    @register_uart_write
    def select( self, mode=chipless.OFFLINE ):
        """ Select reader communiction protocol.
            mode : chipless.OFFLINE     Notify is code ( Reader decode by self. )
                   chipless.ONLINE      Notify is ADC data.
        """
        return super( ChiplessTags, self).select( mode=mode )

    def online( self ):
        """ Get reader communiction protocol.
        """
        mode = self.readRegister( address=0x100C, size=1 )
        if mode[0] and ( unpack( 'H', mode[1] )[0] == chipless.ONLINE ):
            self.cpf.protocol( chipless.ONLINE )
            return True
        self.cpf.protocol( chipless.OFFLINE )
        return False

    @register_uart_write
    def setEncoder( self, index=1, enable=True, coder=100, left=20, middle=200, right=30 ):
        """ 
            index  : code index.
            enable : True or False( disable )
            coder  : chipless coder.
            left   : Minimum frequency offset.
            middle : Middle frequency.
            right  : Maximum frequency offset.
        """
        return super( ChiplessTags, self).setEncoder( index  = index,
                                                      enable = enable,
                                                      coder  = coder,
                                                      left   = left,
                                                      middle = middle,
                                                      right  = right )

    @register_uart_write
    def getEncoder( self, index=1, size=5 ):
        """
            TODO : Currently can only read up to 16 coder configurations.
                   *** Invalid function parameter. See:STM32 source code.
        """
        return super( ChiplessTags, self).getEncoder( index=index, size=size )

    def disconnect( self ):
        if self.ser.isOpen():
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.close()

    def serial_is_open( self ):
        try:
            return self.ser.isOpen()
        except BaseException:
            return False

    def worker_start( self ):
        super( ChiplessTags, self ).response_callback( self.__response_callback )
        self.cpf = ChiplessProtocolFactory( self.unpackage, self.disconnect, self.mode )
        self.serial_worker = serial.threaded.ReaderThread( self.ser, self.cpf )
        self.serial_worker.start()

    def worker_stop( self ):
        """ Stop the reader thread and do not close serial port ."""
        if self.serial_worker is not None:
            self.serial_worker.stop()

    def worker_close( self ):
        """ Close the serial port and exit reader thread (uses lock) """
        if self.serial_worker is not None:
            self.serial_worker.close()
        self.serial_worker = None

    def worker_is_alive( self ):
        try:
            return self.serial_worker.alive
        except BaseException:
            return False
        