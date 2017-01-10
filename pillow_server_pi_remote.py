# remote server running ubuntu 16.04

# Server
import socket
import sys

# Servo Control
import time

# server setup
host = '0.0.0.0'
port_pulse = 12345
port_pi = 12344
address_pulse = (host, port_pulse)
address_pi = (host, port_pi)

server_socket_pulse = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_pulse.bind(address_pulse)
server_socket_pulse.listen(5)

server_socket_pi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_pi.bind(address_pi)
server_socket_pi.listen(5)

# server activation
print "Listening for pulse . . ."
conn_pulse, address_pulse = server_socket_pulse.accept()
print "Connected to pulse at ", address_pulse

pulse = 60
# server and servo listen                                                
while True:
    output = None
    conn_pulse.send("ready") 
    output = conn_pulse.recv(2048);
    if output:
        print "Pulse of client:"
        #print output
        if "disconnect" not in output.strip():
            pulse = output
	    print "no disconnect so far, so pulse is: "
	    print pulse
        # adjust servo to heartrate
    if output.strip() == "disconnect":
        conn_pulse.close()
        time.sleep(1)
        print "Shut down pulse client, now listening for pi . . ."
	conn_pi, address_pi = server_socket_pi.accept()
        print "Connected to pi at ", address_pi
        print pulse
	if conn_pi.recv(2048) == "ready":
		conn_pi.send(pulse[0:3])
       	time.sleep(1)
        #send disconnect message
        dmsg = "disconnect"
		conn_pi.send(dmsg)
		print "Disconnecting from pi"
        conn_pi.close()
        print "Listening for pulse again . . . "
        conn_pulse, address_pulse = server_socket_pulse.accept()
        print "Connected to pulse at ", address_pulse


