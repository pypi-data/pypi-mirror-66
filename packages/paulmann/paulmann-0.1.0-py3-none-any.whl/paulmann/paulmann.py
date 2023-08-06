"""Main class for communicating with Paulmann BLE lights ."""

import sys
from typing import Optional

import pygatt
import logging
from pygatt import BLEAddressType
from pygatt.device import BLEDevice
from pygatt.backends import BLEBackend
from pygatt.exceptions import BLEError, NotConnectedError, NotificationTimeout

from .exceptions import PaulmannConnectionError, PaulmannAuthenticationError,PaulmannError
from .models import Info, State
from .const import *

class MockAdapter:
    __instance = None
    mac = None
    _device = None

    def __init__(self):
        raise Exception("use get_instance() instead")
        
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            cls.__instance._device: Optional[MockDevice] = None
            cls.__instance.mac = ""
        return cls.__instance

    def start(self, **kwargs):
        return True

    def stop(self):
        return True

    def connect(self, mac:str):
        self._mac = mac
        if self._device is None:
            self._device = MockDevice(self)
        return self._device

    def disconnect(self, device):
        #self._device = None
        #self._mac = ""
        return


class MockDevice:
    def __init__(self, adapter):
        self._adapter = adapter
        self._on = False
        self._color = 2700
        self._brightness = 50

    def char_write(self, uuid: str, value: bytearray):
        if uuid == UUID_BRIGHTNESS:
            self._brightness = int.from_bytes(value, 'little')
            logging.info(self._brightness)     
        elif uuid == UUID_COLOR:
            self._color = int.from_bytes(value, 'little')
            logging.info(self._color)
        elif uuid == UUID_ONOFF:
            self._on = int.from_bytes(value, 'little') == 1
            logging.info(self._on)        
        return True

    def char_read(self, uuid: str) -> bytearray:
        if uuid == UUID_BRIGHTNESS:
            return self._brightness.to_bytes(1, 'little')  
        elif uuid == UUID_COLOR:
            return self._color.to_bytes(2, 'little')
        elif uuid == UUID_CONTROLLER_ENABLE:
            return bytearray("1", "ascii")
        elif uuid == UUID_INFO_FIRMWARE_REVISION:
            return bytearray("v1.fw.mock", "ascii")  
        elif uuid == UUID_INFO_HARDWARE_REVISION:
            return bytearray("v1.hw.mock", "ascii")
        elif uuid == UUID_INFO_IEEE_CERT:
            return bytearray("ieee cert", "ascii")
        elif uuid == UUID_INFO_MODEL:
            return bytearray("Model name mock", "ascii")
        elif uuid == UUID_INFO_PNP_ID:
            return bytearray("abc.mock", "ascii")
        elif uuid == UUID_INFO_SERIAL_NUMBER:
            return bytearray("Serial number mock", "ascii")
        elif uuid == UUID_INFO_SOFTWARE_REVISION:
            return bytearray("v1.sw.mock", "ascii")
        elif uuid == UUID_INFO_SYSTEM_ID:
            return bytearray("1234.mock", "ascii")
        elif uuid == UUID_NAME:
            return bytearray("Lamp WC Mock", "ascii")
        elif uuid == UUID_ONOFF:
            logging.info("Read onoff:" + str(self._on))
            return self._on.to_bytes(int(self._on == True), 'little')  
        elif uuid == UUID_SYSTEM_TIME:
            return bytearray("today", "ascii")
        elif uuid == UUID_TIMER:
            return bytearray("tomorrow", "ascii")
        elif uuid == UUID_WORKING_MODE:
            return bytearray("aaaa", "ascii")
        elif uuid == UUID_INFO_MANUFACTURER:
            return bytearray("Paulman lichts mock", "ascii")

class Paulmann:
    """Main class for communicating with Paulmann BLE lights ."""

    _device = None

    _adapter: BLEBackend = None

    def __init__(
            self,
            mac: str,
            pwd: str = "1234",
            request_timeout: int = 8
    ) -> None:
        """Initialize connection with the Paulman BLE light."""
        self.mac: str = mac
        self.request_timeout: int = request_timeout
        self._adapter: BLEBackend = None
        self._authenticated = False
        self._pwd: str = pwd


    def _connect(self, retry_count=5, force_restart=False)->BLEDevice:
        """ Connect to the devices and save the connection in _device """
        if self._adapter is None or force_restart == True:
            self._adapter = pygatt.backends.GATTToolBackend()
            #self._adapter = MockAdapter.get_instance()
            self._adapter.start(reset_on_start=force_restart)

        if self._device is not None and force_restart == False:
            return self._device
            
        i = 0
        while i < retry_count:
            try:
                self._device = self._adapter.connect(self.mac)
                logging.info("Successfully connected to " + self.mac)
                break
            except:
                logging.info("Attempted connecting to " + self.mac + " and failed, retrying "
                      + str(i+1) + " time")
            i += 1

        if self._device is None:
            raise PaulmannConnectionError("Could not connect to the light " + self.mac)        
        return self._device


    def _disconnect(self):
        """ disconnect from device """
        #if self._device is not None:
        #    self._adapter.disconnect(self._device)
        #    self._device = None

        #if self._adapter is not None:
        #   self._adapter.stop()
        #    self._adapter = None

    def disconnect(self):
        self._disconnect()

    def _authenticate (self, pwd: str = None):
        """ authenticate with the device """
        self._connect()

        if pwd is None:
            pwd = self._pwd

        logging.info("Sending password " + pwd)
        try:
            self._device.char_write (UUID_PWD, bytearray(pwd, "ascii"))
            self._authenticated = True
        except:
            raise PaulmannAuthenticationError("Could not authenticate to the light " + self.mac + " using password")
        logging.info("Password successfully sent!")

    def connect_and_authenticate(self, pwd: str = None) -> BLEDevice:
        try:
            self._connect()    
            
            if self._authenticated == False:
                self._authenticate(pwd)           
            return self._device
        except:
            raise

    def switch(self, on: bool):
        """ switch the light on or off according to parareter on """
        try:
            self.connect_and_authenticate()                    
            if on:
                logging.info("Switching on")
                self._device.char_write (UUID_ONOFF, bytearray([0x01]))
            else:
                logging.info("Switching off")
                self._device.char_write (UUID_ONOFF, bytearray([0x00]))
        finally:
            self._disconnect()               

    def toggle (self):
        """ flip the switch regardless of current state """
        try:
            self.connect_and_authenticate()        
            state = self._device.char_read(UUID_ONOFF)
            print("Current state is " + str(state))
            if state == bytearray([0x00]):
                logging.info("Toggle on")
                self._device.char_write (UUID_ONOFF, bytearray([0x01]))
            else:
                self._device.char_write (UUID_ONOFF, bytearray([0x00]))
                logging.info("Toggle off")
        finally:
            self._disconnect()

    def color (self, value: int):
        """ brightness between 0 and 100 """
        try:
            self.connect_and_authenticate()            

            if value > 6500:
                value = 6500
            elif value < 2700:
                value = 2700

            logging.info("Color to " + value)
            self._device.char_write(UUID_COLOR, value.to_bytes(2, "little"))

        finally:
            self._disconnect()

    def brightness (self, value: int):
        """ brightness between 0 and 100 """
        try:
            self.connect_and_authenticate()            

            if value > 100:
                value = 100
            elif value < 0:
                value = 0
            logging.info("Brightness to " + value)
            self._device.char_write(UUID_BRIGHTNESS, value.to_bytes(1, "little"))

        finally:
            self._disconnect()

    def is_on(self)->bool:
        """ return current state of light = on or off """
        try:
            state = self.get_state()
            return state.on

        finally:
            self._disconnect()

    def get_brightness(self)->int:
        """ return current brightness level """
        try:
            state = self.get_state()
            return state.brightness
        finally:
            self._disconnect()

    def get_color(self)->bool:
        """ return current color of light """
        try:
            state = self.get_state()
            return state.color
        finally:
            self._disconnect()

    def set_state(self, on, brightness, color):
        self.connect_and_authenticate()

        if on is not None:
            if on:
                logging.info("Toggle on")
                self._device.char_write (UUID_ONOFF, bytearray([0x01]))
            else:
                self._device.char_write (UUID_ONOFF, bytearray([0x00]))
                logging.info("Toggle off")

        if brightness is not None:
            if brightness > 100:
                brightness = 100
            elif brightness < 0:
                brightness = 0
            logging.info("Brightness to " + str(brightness))
            self._device.char_write(UUID_BRIGHTNESS, brightness.to_bytes(1, "little"))

        if color is not None:
            color = round(1e6/color)
            if color > 6500:
                color = 6500
            elif color < 2700:
                color = 2700

            logging.info("Color to " + str(color))
            self._device.char_write(UUID_COLOR, color.to_bytes(2, "little"))

        self._disconnect()


    def get_state(self)-> State:
        """ return full state of the light """
        try:
            self.connect_and_authenticate()

            logging.info("Retrieving state")
            data = {
                UUID_SYSTEM_TIME: self._device.char_read(UUID_SYSTEM_TIME),
                UUID_ONOFF: int.from_bytes(self._device.char_read(UUID_ONOFF), 'little') == 1,
                UUID_BRIGHTNESS: int.from_bytes(self._device.char_read(UUID_BRIGHTNESS), 'little'),
                UUID_NAME: self._device.char_read(UUID_NAME).decode('ascii').rstrip("\x00"),
                UUID_COLOR: int.from_bytes(self._device.char_read(UUID_COLOR), 'little'),
                UUID_TIMER: self._device.char_read(UUID_TIMER),
                UUID_WORKING_MODE: self._device.char_read(UUID_WORKING_MODE),
                UUID_CONTROLLER_ENABLE: bool(self._device.char_read(UUID_CONTROLLER_ENABLE)),
            }

            return State.from_dict(data)

        finally:
            self._disconnect()

    def get_info(self)-> Info:
        """ return full info of the light """
        try:
            self._connect()

            logging.info("Retrieving info")
            data = {
                UUID_INFO_SYSTEM_ID:
                    self._device.char_read(UUID_INFO_SYSTEM_ID),
                UUID_INFO_MODEL:
                    self._device.char_read(UUID_INFO_MODEL).decode('ascii').rstrip("\x00"),
                UUID_INFO_SERIAL_NUMBER:
                    self._device.char_read(UUID_INFO_SERIAL_NUMBER).decode('ascii').rstrip("\x00"),
                UUID_INFO_FIRMWARE_REVISION:
                    self._device.char_read(UUID_INFO_FIRMWARE_REVISION).decode('ascii')
                    .rstrip("\x00"),
                UUID_INFO_HARDWARE_REVISION:
                    self._device.char_read(UUID_INFO_HARDWARE_REVISION).decode('ascii')
                    .rstrip("\x00"),
                UUID_INFO_SOFTWARE_REVISION:
                    self._device.char_read(UUID_INFO_SOFTWARE_REVISION).decode('ascii')
                    .rstrip("\x00"),
                UUID_INFO_MANUFACTURER:
                    self._device.char_read(UUID_INFO_MANUFACTURER).decode('ascii').rstrip("\x00"),
                UUID_INFO_IEEE_CERT:
                    self._device.char_read(UUID_INFO_IEEE_CERT),
                UUID_INFO_PNP_ID:
                    self._device.char_read(UUID_INFO_PNP_ID).decode('ascii').rstrip("\x00"),
            }

            return Info.from_dict(data)

        finally:
            self._disconnect()
