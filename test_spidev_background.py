#!/usr/bin/python3

import spidev
import time

# Split an integer input into a two byte array to send via SPI
def write_pot(input):
#    print(input)
    msb = input >> 8
    lsb = input & 0xFF
#    print(spi.xfer([msb, lsb]))



if __name__ == '__main__':
   spi = spidev.SpiDev()
   ret = spi.open(0, 0)
   print(ret)
   spi.max_speed_hz = 30000
   spi.mode = 0
   print("Started SPIDEV = ", spidev)
   data = 0x555

   while True:
 #    print("Hello, I'm MMRPi-Hardware Energomera Library")
     time.sleep(0.2)
     data = data + 1
     write_pot(data)

