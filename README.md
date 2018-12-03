# ansluta-python
### Ikea Ansluta remote control by Raspberry pi and CC2500 2.4Ghz transceiver via python


This project was created to control Ikea Omlopp/Utrusta lights by Raspberry pi.
The original remote has one Button. With every push the lights cycle -> 50% -> 100% -> 50% -> off

The original remote send a series of data icluded two own address bytes. 
- example: 0x55 0x01 0xD0 0x9A 0x02 0xAA (0xD0 & 0x9A my addressbytes)
