# /*****************************************************************************
# * | File        :	  config.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface,for Raspberry pi
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-06-17
# * | Info        :   
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


import time
from smbus import SMBus
import spidev
import ctypes
from gpiozero import *

Device_SPI = 0
Device_I2C = 1

class RaspberryPi:
    def __init__(self,spi_freq=10000000,bl_freq=1000,i2c=None):
        self.INPUT = False
        self.OUTPUT = True
        
        self.SPEED  =spi_freq

        
        self.Device = Device_I2C
        self.address = 0x3C
        self.bus = SMBus(1)


    def delay_ms(self,delaytime):
        time.sleep(delaytime / 1000.0)

    def digital_write(self, Pin, value):
        if value:
            Pin.on()
        else:
            Pin.off()

    def digital_read(self, Pin):
        return Pin.value

    def spi_writebyte(self,data):
        self.spi.writebytes([data[0]])

    def i2c_writebyte(self,reg, value):
        self.bus.write_byte_data(self.address, reg, value)
    

    def module_exit(self):
        self.bus.close()

### END OF FILE ###
