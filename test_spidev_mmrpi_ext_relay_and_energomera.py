#!/usr/bin/python3

import spidev
import time


class Base:
    # Foreground:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    # Formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # End colored text
    END = '\033[0m'
    NC = '\x1b[0m'  # No Color


tx_array = [0xFF]*512

POS_EXT_RELAY = 40
POS_ENERG_S = 320
POS_ENERG_V = 384


tx_array[POS_EXT_RELAY + 0] = 1
tx_array[POS_EXT_RELAY + 1] = 0
tx_array[POS_EXT_RELAY + 2] = 1
tx_array[POS_EXT_RELAY + 3] = 0
tx_array[POS_EXT_RELAY + 4] = 1
tx_array[POS_EXT_RELAY + 5] = 0
tx_array[POS_EXT_RELAY + 6] = 1
tx_array[POS_EXT_RELAY + 7] = 0



# Split an integer input into a two byte array to send via SPI
def write_pot(input):
    print(input)
    msb = input >> 8
    lsb = input & 0xFF
    tx_array[0] = msb
    tx_array[1] = lsb
    rx_array = spi.xfer(tx_array)
    print(Base.BOLD, "RX:" + Base.OKGREEN, Base.END, tx_array[0:8], ''.join(str(chr(e)) for e in tx_array[POS_ENERG_S:POS_ENERG_S+8]), ''.join(str(chr(e)) for e in tx_array[POS_ENERG_V:POS_ENERG_V+64]))
    print(Base.BOLD, "RX:" + Base.OKGREEN, Base.END, tx_array[0:8], tx_array[POS_ENERG_S:POS_ENERG_S+8],  tx_array[POS_ENERG_V:POS_ENERG_V+64])

    #print(Base.BOLD, "TX:" + Base.OKGREEN, Base.END, tx_array[0:8], tx_array[POS_EXT_RELAY:POS_EXT_RELAY+8], ''.join(str(chr(e)) for e in tx_array[POS_ENERG_V-64:POS_ENERG_V+64]))
    #print(Base.BOLD, "RX:" + Base.OKGREEN, Base.END, rx_array[0:8], rx_array[POS_EXT_RELAY:POS_EXT_RELAY+8], ''.join(str(chr(e)) for e in rx_array[POS_ENERG_V-64:POS_ENERG_V+64]))


if __name__ == '__main__':
   print("Hello, I'm MMRPi-Hardware External Relay Tester")
   spi = spidev.SpiDev()
   ret = spi.open(0, 0)
   print("Spi.open = ", ret)
   spi.max_speed_hz = 300000
   spi.mode = 0
   print("Started SPIDEV = ", spi)
   data = 0x555

   while True:
     time.sleep(0.1)
     data = data + 1
     write_pot(data)
     for x in range(8):
       if tx_array[POS_EXT_RELAY+x] == 1:
         tx_array[POS_EXT_RELAY+x] = 0
       else:
         tx_array[POS_EXT_RELAY+x] = 1

     
    # break

