#!/usr/bin/python3

import spidev
import time
import os
import struct

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



def binary(num):
    # Struct can provide us with the float packed into bytes. The '!' ensures that
    # it's in network byte order (big-endian) and the 'f' says that it should be
    # packed as a float. Alternatively, for double-precision, you could use 'd'.
    packed = struct.pack('!f', num)
    print ('Packed: %s' % repr(packed))

    # For each character in the returned string, we'll turn it into its corresponding
    # integer code point
    # 
    # [62, 163, 215, 10] = [ord(c) for c in '>\xa3\xd7\n']
    integers = [ord(c) for c in packed]
    print ('Integers: %s' % integers)

    # For each integer, we'll convert it to its binary representation.
    binaries = [bin(i) for i in integers]
    print ('Binaries: %s' % binaries)

    # Now strip off the '0b' from each of these
    stripped_binaries = [s.replace('0b', '') for s in binaries]
    print ('Stripped: %s' % stripped_binaries)

    # Pad each byte's binary representation's with 0's to make sure it has all 8 bits:
    #
    # ['00111110', '10100011', '11010111', '00001010']
    padded = [s.rjust(8, '0') for s in stripped_binaries]
    print ('Padded: %s' % padded)

    # At this point, we have each of the bytes for the network byte ordered float
    # in an array as binary strings. Now we just concatenate them to get the total
    # representation of the float:
    return ''.join(padded)



# Split an integer input into a two byte array to send via SPI
def write_pot(input):
    msb = input >> 8
    lsb = input & 0xFF
    tx_array[0] = msb
    tx_array[1] = lsb
    tmp = tx_array.copy()
    rx_array = spi.xfer(tmp)
    os.system('clear')
    print(input)
    print("Phase 1 CURRE = %4.4f" % (struct.unpack_from('f', bytes(rx_array[POS_ENERG_V+0:POS_ENERG_V+4]))[0]))
    print("Phase 2 CURRE = %4.4f" % (struct.unpack_from('f', bytes(rx_array[POS_ENERG_V+4:POS_ENERG_V+8]))[0]))
    print("Phase 3 CURRE = %4.4f" % (struct.unpack_from('f', bytes(rx_array[POS_ENERG_V+8:POS_ENERG_V+12]))[0]))

    print("Phase 1 VOLTA = %4.4f" % (struct.unpack_from('f', bytes(rx_array[POS_ENERG_V+0+12:POS_ENERG_V+4+12]))[0]))
    print("Phase 2 VOLTA = %4.4f" % (struct.unpack_from('f', bytes(rx_array[POS_ENERG_V+4+12:POS_ENERG_V+8+12]))[0]))
    print("Phase 3 VOLTA = %4.4f" % (struct.unpack_from('f', bytes(rx_array[POS_ENERG_V+8+12:POS_ENERG_V+12+12]))[0]))

    print("Phase 1 POWER = %4.4f" % (struct.unpack_from('f', bytes(rx_array[POS_ENERG_V+0+24:POS_ENERG_V+4+24]))[0]))
    print("Phase 2 POWER = %4.4f" % (struct.unpack_from('f', bytes(rx_array[POS_ENERG_V+4+24:POS_ENERG_V+8+24]))[0]))
    print("Phase 3 POWER = %4.4f" % (struct.unpack_from('f', bytes(rx_array[POS_ENERG_V+8+24:POS_ENERG_V+12+24]))[0]))



    print(Base.BOLD, "RX:" + Base.OKGREEN, Base.END, rx_array[0:8], ''.join(str(chr(e)) for e in rx_array[POS_ENERG_S:POS_ENERG_S+16])) #, ''.join(str(chr(e)) for e in rx_array[POS_ENERG_V+12:POS_ENERG_V+64]))
    #print(Base.BOLD, "RX:" + Base.OKGREEN, Base.END, rx_array[0:8], rx_array[POS_ENERG_S:POS_ENERG_S+8],  rx_array[POS_ENERG_V:POS_ENERG_V+64])

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
     time.sleep(0.02)
     data = data + 1
     write_pot(data)
     for x in range(8):
       if tx_array[POS_EXT_RELAY+x] == 1:
         tx_array[POS_EXT_RELAY+x] = 0
       else:
         tx_array[POS_EXT_RELAY+x] = 1

     
    # break

