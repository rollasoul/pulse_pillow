from multiprocessing import Process, Queue
# Server
import socket
import sys
import multiprocessing
import errno
import time

# Servo Control
import time
import wiringpi

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period_in = 0.030
delay_period_out = 0.04
delay_break = 0.8

# server setup
s = socket.socket()
host = "147.75.100.89"
port = 12344
#s.connect((host, port))
pulse = None
last_pulse = None

def reader(queue):
    ## Read from the queue
    while True:
            msg = queue.get()         # Read from the queue and do nothing
            pulse = msg
            print "start breathing"
            pulse_in = delay_period_in * 60 / (pulse*4)
            pulse_out = delay_period_out * 60 / (pulse*4)
            for breathing in range(150, 70, -1):
		 wiringpi.pwmWrite(18, breathing)
                 time.sleep(pulse_in)
                 wiringpi.pwmWrite(18, breathing)
                 time.sleep(pulse_in)
                 wiringpi.pwmWrite(18, breathing)
                 time.sleep(pulse_in)
                 wiringpi.pwmWrite(18, breathing)
                 time.sleep(pulse_in)
            time.sleep(delay_break*30 / pulse)
            for breathing in range(70, 150, 1):
                 wiringpi.pwmWrite(18, breathing)
                 time.sleep(pulse_out)
                 wiringpi.pwmWrite(18, breathing)
                 time.sleep(pulse_out)
                 wiringpi.pwmWrite(18, breathing)
                 time.sleep(pulse_out)
                 wiringpi.pwmWrite(18, breathing)
                 time.sleep(pulse_out)
                #delay_period_out * 60 / pulse*2)
            time.sleep(delay_break * 50 / pulse)
	    break
def writer(queue):
    # Write to the queue
    s = socket.socket()
    s.connect((host, port))
    print "Connected to server"
    output = None
    s.send("ready")
    print "ready sent,waiting for pulse"
    output = s.recv(2048)
    if output.strip() == "disconnect":
        s.close()
    if output.strip() != "disconnect": 
                print "Message received from client:"		
                try: 
                    pulse = float(output[:3])
                except ValueError:
                    pass
                #s = socket.socket()
                #s.connect((host, port))
	        print "pulse is %s" % (pulse)
                last_pulse = pulse
                queue.put(pulse) 
#            queue.put('DONE') 

if __name__=='__main__':
    while True:
        queue = Queue()   # reader() reads from queue
                          # writer() writes to queue
        reader_p = Process(target=reader, args=((queue),))
        reader_p.daemon = True
        reader_p.start()        # Launch reader() as a separate python process

        _start = time.time()
        writer(queue)    # Send a lot of stuff to reader()
        reader_p.join()         # Wait for the reader to finish
        print "done"
