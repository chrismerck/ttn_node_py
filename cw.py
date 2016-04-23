"""
Python Code for Putting LoRaMOTE into CW Mode

Copyright (c) 2016 Jason Biegel, Chris Merck
All Rights Reserved 

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import serial
import time
import sys

BAUD_RATE = 57600

class LoRaSerial(object):
    def __init__(self,_serial_port,_dev_addr):
        '''
            configures serial connection
        '''
        self._ser = serial.Serial(_serial_port, BAUD_RATE)

        # timeout block read
        self._ser.timeout = 8

        # disable software flow control
        self._ser.xonxoff = False

        # disable hardware (RTS/CTS) flow control
        self._ser.rtscts = False

        # disable hardware (DSR/DTR) flow control
        self._ser.dsrdtr = False

        # timeout for write
        self._ser.writeTimeout = 0

        #print "Resetting LoRa Tranceiver..."
        self.write_command('sys reset',False)
        #print "Configuring Tranceiver..."
        self.write_command('radio set mod lora')
        self.write_command('mac pause')

    def read(self):
        '''
            reads serial input
        '''
        return self._ser.readline().strip()

    def write(self, str):
        '''
            writes out string to serial connection, returns response
        '''
        self._ser.write(str + '\r\n')
        return self.read()
    
    def write_command(self, config_str, check_resp=False):
        '''
            writes out a command
        '''
        #print "Command: '%s'"%config_str
        response = self.write(config_str)
        if check_resp and response != 'ok':
          print "ERROR: Unexpected response: '%s'"%response
        
    def send_message(self, data):
        '''
            sends a message to backend via gateway
        '''
        print "Sending message: ", data
        # send packet (returns 'ok' immediately)
        self.write_command('mac tx uncnf 1 %s'%data)
        # wait for success message
        response = self.read()
        if response == 'mac_tx_ok':
          print "Message sent successfully!"
        else:
          print "ERROR: mac tx command returned unexpected response: ", response 

    def receive_message(self):
        '''
            waits for a message
        '''
        pass


if __name__ == "__main__":
  if len(sys.argv) < 4:
    print "Usage: python cw.py <port> <dev_addr> <period>"
    print
    exit(0)

  port = sys.argv[1]
  dev_addr = sys.argv[2]
  period = int(sys.argv[3])
  loramote = LoRaSerial(port,dev_addr)
  while True:
    loramote.write('radio cw on')
    time.sleep(0.1)
    loramote.write('radio cw off')
    time.sleep(0.1)
    loramote.write('radio cw on')
    time.sleep(0.1)
    loramote.write('radio cw off')
    time.sleep(0.1)
    loramote.write('radio cw on')
    time.sleep(0.1)
    loramote.write('radio cw off')
    time.sleep(0.1)
    loramote.write('radio cw on')
    time.sleep(2)
    loramote.write('radio cw off')
    time.sleep(0.5)

