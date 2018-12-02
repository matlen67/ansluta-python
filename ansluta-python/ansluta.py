#!/usr/bin/python

import time
import spidev
import sys

import CC2500

spi=spidev.SpiDev()

def openSpi():
	spi.open(0, 0)
	spi.max_speed_hz = 600000
	spi.mode = 0


def readReg(addr):
	buf=list([ addr | 0x80, 0x00])
	result = spi.xfer(buf)
	return result[1]


def writeReg(addr, value):
	buf=list([addr , value])
	spi.xfer(buf)

	
def sendStrobe(strobe):
	spi.xfer([strobe])
	#time.sleep(0.01)


def initCC2500():
	writeReg(CC2500.REG_IOCFG2, 0x29)
	writeReg(CC2500.REG_IOCFG0, 0x06)
	writeReg(CC2500.REG_PKTLEN, 0xFF) # Max packet length
	writeReg(CC2500.REG_PKTCTRL1, 0x04)
	writeReg(CC2500.REG_PKTCTRL0, 0x05) # variable packet length; CRC enabled
	writeReg(CC2500.REG_ADDR, 0x01) # Device address
	writeReg(CC2500.REG_CHANNR, 0x10) # Channel number
	writeReg(CC2500.REG_FSCTRL1, 0x09)
	writeReg(CC2500.REG_FSCTRL0, 0x00)
	writeReg(CC2500.REG_FREQ2, 0x5D) # RF frequency 2433.000000 MHz 
	writeReg(CC2500.REG_FREQ1, 0x93) # RF frequency 2433.000000 MHz 
	writeReg(CC2500.REG_FREQ0, 0xB1) # RF frequency 2433.000000 MHz
	writeReg(CC2500.REG_MDMCFG4, 0x2D)
	writeReg(CC2500.REG_MDMCFG3, 0x3B) # Data rate 250.000000 kbps
	writeReg(CC2500.REG_MDMCFG2, 0x73) # MSK, No Manchester; 30/32 sync mode
	writeReg(CC2500.REG_MDMCFG1, 0xA2)
	writeReg(CC2500.REG_MDMCFG0, 0xF8) # Channel spacing 199.9500 kHz
	writeReg(CC2500.REG_DEVIATN, 0x01)
	writeReg(CC2500.REG_MCSM2, 0x07)
	writeReg(CC2500.REG_MCSM1, 0x30)
	writeReg(CC2500.REG_MCSM0, 0x18)
	writeReg(CC2500.REG_FOCCFG, 0x1D)
	writeReg(CC2500.REG_BSCFG, 0x1C)
	writeReg(CC2500.REG_AGCCTRL2, 0xC7)
	writeReg(CC2500.REG_AGCCTRL1, 0x00)
	writeReg(CC2500.REG_AGCCTRL0, 0xB2)
	writeReg(CC2500.REG_WOREVT1, 0x87)
	writeReg(CC2500.REG_WOREVT0, 0x6B)
	writeReg(CC2500.REG_WORCTRL, 0xF8)
	writeReg(CC2500.REG_FREND1, 0xB6)
	writeReg(CC2500.REG_FREND0, 0x10)
	writeReg(CC2500.REG_FSCAL3, 0xEA)
	writeReg(CC2500.REG_FSCAL2, 0x0A)
	writeReg(CC2500.REG_FSCAL1, 0x00)
	writeReg(CC2500.REG_FSCAL0, 0x11)
	writeReg(CC2500.REG_RCCTRL1, 0x41)
	writeReg(CC2500.REG_RCCTRL0, 0x00)
	writeReg(CC2500.REG_FSTEST, 0x59)
	writeReg(CC2500.REG_TEST2, 0x88)
	writeReg(CC2500.REG_TEST1, 0x31)
	writeReg(CC2500.REG_TEST0, 0x0B)
	writeReg(CC2500.REG_DAFUQ, 0xFF)


def readAddressBytes():
	tries = 0
	AddressFound = False
	addrA = ""
	addrB = ""
	recvPacket = []
	
	print("Listening for AddressBytes")
	
	while tries <= 2000 and AddressFound == False:
	
		sys.stdout.write(".")
		sys.stdout.flush()
		sendStrobe(CC2500.CC2500_SRX)
		writeReg(CC2500.REG_IOCFG1,0x01)
		time.sleep(0.002)
		PacketLength = readReg(CC2500.CC2500_FIFO)
		
		if PacketLength >= 1 and PacketLength <=8:
			for i in range(PacketLength):
				recvPacket.append(readReg(CC2500.CC2500_FIFO))
			print ""
			print " ".join([hex(i) for i in recvPacket])
			
			start=0;
			while recvPacket[start] <> 0x55 and start < PacketLength:
				start += 1
		
			if recvPacket[start+1] == 0x01 and recvPacket[start+5] == 0xAA:
				AddressFound = True
				AddressByteA = recvPacket[start+2]                       
				AddressByteB = recvPacket[start+3]
			
				print"AddressBytes found :)"
				print''.join( hex(AddressByteA) )
				print''.join( hex(AddressByteB) )
				break
		
		sendStrobe(CC2500.CC2500_SIDLE)
		sendStrobe(CC2500.CC2500_SFRX)
		tries += 1


def sendCommand(addrByteA, addrByteB, command):
    for i in range(50):    	
		sendStrobe(CC2500.CC2500_SFTX)
		sendStrobe(CC2500.CC2500_SIDLE)
		
		buf=list([0x7F, 0x06, 0x55, 0x01, addrByteA, addrByteB, command, 0xAA])
		spi.xfer(buf)
        
		sendStrobe(CC2500.CC2500_STX)      # 0x35  transmit data in TX
		time.sleep(0.0016)



def main():	

	for arg in sys.argv[0:]:
		print arg
	
	
	if len(sys.argv) == 4:
		addrA = int(sys.argv[1][2:],16)
		addrB = int(sys.argv[2][2:],16)
		
		
		if sys.argv[3] == "0":
			print "argv 1"
			print('open spi')
			openSpi()
			writeReg(0x3E, 0xFF)
			sendCommand(addrA,addrB,0x01)
			spi.close
			sys.exit(0)
			
		elif sys.argv[3] == "50":
			print "argv 50"
			print('open spi')
			openSpi()
			writeReg(0x3E, 0xFF)
			sendCommand(addrA,addrB,0x02)
			spi.close
			sys.exit(0)
			
		elif sys.argv[3] == "100":
			print "argv 100"
			print('open spi')
			openSpi()
			writeReg(0x3E, 0xFF)
			sendCommand(addrA,addrB,0x03)
			spi.close
			sys.exit(0)	
			
		else:
			print('open spi')
			openSpi()
			print('reset CC2500')
			sendStrobe(CC2500.CC2500_SRES)
			#time.sleep(0.01)
			print('init CC2500')
			initCC2500()
			writeReg(0x3E, 0xFF)
			readAddressBytes()
			spi.close
			print('close spi')
			sys.exit(0)
	else:
		print ("\nUsage: python ansluta.py <addrByte1 addrByte2 0> <addrByte1 addrByte2 50> <addrByte1 addrByte2 100>\n")
		print ("Example: python ansluta.py 0xD0 0x9A 50\n")
		sys.exit(2)
	

if __name__== '__main__':
	main()


