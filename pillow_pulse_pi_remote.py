# piSerial has to be installed to run this code (http://playground.arduino.cc/Interfacing/Python)
# pulse_sensor_amped_arduino.io script has to be uploaded to arduino from mac, then it reads to raspberry pi serial from analog pins on arduino - check arduino usb ID before running

import socket
import time
import serial

host = '147.75.100.13' # enter address of remote server here
port = 12345
ser = serial.Serial('/dev/arduino', 115200)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#for index in xrange(1000):
while True:
	data = None
	data = "%s" % ser.readline()
	print data
	if "B" in data:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((host, port))
		data = data.strip('B')
		print 'send to server: ' + data
		if client_socket.recv(2048) == "ready":
			client_socket.send(data)
			time.sleep(1)
			#send disconnect message                                                                                                                           
			dmsg = "disconnect"
			print "Disconnecting"
			client_socket.send(dmsg)
			client_socket.close()
		time.sleep(1)

