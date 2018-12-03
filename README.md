# ansluta-python
#### Ikea Ansluta remote control by Raspberry pi and CC2500 2.4Ghz transceiver via python


This project was created to control Ikea Omlopp/Utrusta lights by Raspberry pi.
The original remote has one Button. With every push the lights cycle -> 50% -> 100% -> 50% -> off

The original remote send a series of data icluded two own address bytes. 
- example: 0x55 0x01 0xD0 0x9A 0x02 0xAA (0xD0 & 0x9A my addressbytes)

<img src="https://github.com/matlen67/ansluta-python/blob/master/pictures/ansluta_original.jpg" width="128"> <img src="https://github.com/matlen67/ansluta-python/blob/master/pictures/leiterplatte.jpg" width="128">


## Hardware:
  - Raspbery pi 3B+
  - CC2500 Transiver module (WLC24D) [ebay](https://www.ebay.com/itm/2PCS-1-8-3-6V-CC2500-IC-Wireless-RF-2400MHZ-Transceiver-Module-SPI-ISM-Demo-Code/401239287968)

<img src="https://github.com/matlen67/ansluta-python/blob/master/pictures/rpi.jpg" width="128">       <img src="https://github.com/matlen67/ansluta-python/blob/master/pictures/WLC-24D.png" width="128">

## Install software:
- Copy 'ansluta-python' folder to Raspberry /usr/src/
- got to folder: ``cd usr/src/ansluta-python``
- listen for your addressbytes: ``python ansluty.py l``
- press button on original remote
- note your found address Bytes

<img src="https://github.com/matlen67/ansluta-python/blob/master/pictures/console.png" width="128">
