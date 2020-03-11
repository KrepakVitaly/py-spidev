#!/usr/bin/python3

import spidev
import time

tx_array = [0]*512

# Split an integer input into a two byte array to send via SPI
def write_pot(input):
    print(input)
    msb = input >> 8
    lsb = input & 0xFF
    tx_array[0] = msb
    tx_array[1] = lsb
    rx_array = spi.xfer(tx_array)
    print(rx_array)


if __name__ == '__main__':
   spi = spidev.SpiDev()
   ret = spi.open(0, 0)
   print("Spi.open = ", ret)
   spi.max_speed_hz = 300000
   spi.mode = 0
   print("Started SPIDEV = ", spi)
   data = 0x555

   while True:
 #    print("Hello, I'm MMRPi-Hardware Energomera Library")
     time.sleep(0.01)
     data = data + 1
     write_pot(data)
    # break

