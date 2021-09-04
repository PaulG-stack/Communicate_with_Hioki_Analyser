import time
import matplotlib.pyplot as plt
import numpy

import socket
import sys
import time
import matplotlib.pyplot as plt

#Create Plot
plt.axis([0, 200, -50, 50])

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('169.254.83.83', 3100)
print(sys.stderr, 'connecting to %s port %s' % server_address)
try:
    sock.connect(server_address)
except Exception as e:
    print(e)
else:
    print("Connection Complete")

try:
    message = '*IDN?\r\n'.encode()
    print(message)
    sock.send(message)
    data = sock.recv(1000)
    print(data)
except:
    print("Failed!")


try:
    message = 'HEAD OFF\r\n'.encode()
    print(message)
    sock.send(message)
##    data = sock.recv(1000)
##    print(data)
except:
    print("Failed!")

try:
    message = 'HEAD?\r\n'.encode()
    print(message)
    sock.send(message)
    data = sock.recv(1000)
    print(data)
except:
    print("Failed!")



try:
    message = 'MEAS:ITEM:POW 15,1,1,0,0\r\n'.encode()
    print(message)
    sock.send(message)
except:
    print("Failed!")

try:
    message = 'MEAS:ITEM:POW?\r\n'.encode()
    print(message)
    sock.send(message)
    data = sock.recv(1000)
    print(data)
except:
    print("Failed!")
    
i = 0

while(i < 1000):
    try:
        message = 'MEAS:POW?\r\n'.encode()
        #print(message)
        sock.send(message)
        data = sock.recv(1000)
        #print(data)
        data_dec = data.decode()
        new_data = data_dec.split(';')
        #print(new_data)
        list_values = [float(value) for value in new_data[1:]]
        plt.scatter(i,list_values[4])
        plt.pause(0.05)
##        data.append(sock.recv(1000))
##        print(data)
        i = i + 1

    except Exception as e:
        print(e)
        
plt.show()


##for i in range(200):
##    response = getdata.communicatewithmeter(meter)
##    print(response)
##    update(h1,i,response)
##    time.sleep(0.1)
