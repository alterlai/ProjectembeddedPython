import serial
import time
import sys


class Arduino():

	def __init__(self, COMPORT):
		self.ser=serial.Serial(COMPORT, 19200, timeout=1)


	# Functie request
	#	argment: command -> commando voor Arduino
	#	return value: tuple met daarin statuscode (OK of ERR) en evt. aanvullende info
	def request(self, command):
		self.ser.write((command+"\n").encode('ascii'))	# Let op! pyserial heeft geen writeline, zelf \n aan string toevoegen!
		extra_info=None
		l=self.ser.readline().decode('ascii').strip()
		if l not in ["OK", "ERR"]:
			extra_info=l
			l=self.ser.readline().decode('ascii').strip()
			if l not in ["OK", "ERR"]:
				l=None
		return (l, extra_info)

	def handshake(self):
		tries_left=4
		while(tries_left>0):
			r=self.request("hello")
			
			if r[0]==("OK"):
				tries_left=0
				self.deviceName = r[1]

			else:
				tries_left-=1
				if (tries_left==0):
					print("Handshake failed")
					sys.exit(1)

	def get_naam(self):
		return self.deviceName

	def get_maxlengte(self):
		r = self.request("get_maxlengte")
		return (r[0], ord(r[1])) 

ar1 = Arduino('COM3')
ar1.handshake()
print(ar1.get_naam())
print(ar1.get_maxlengte())


