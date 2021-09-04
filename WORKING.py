import socket
import sys
import time
from tkinter import messagebox


def filter_analyserdata(data):
    try:
        print(data)
        data_without_G = data.replace('G','')
        data_without_GD = data_without_G.replace('D','')
        data_replace_INF = data_without_GD.replace('INF', '5555')
        data_replace_NAN = data_replace_INF.replace('NAN','9999')
        list_data_str = data_replace_NAN.split(';')
        print(list_data_str)
        list_values = [float(value) for value in list_data_str[1:]]
        print(list_values)
        
        #return list_values
    except Exception as e:
        
        messagebox.showerror("Impicit Data Convesion", "Data Conversion Error")



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
##    data = []
##    data.append(sock.recv(1000))
##    print(data)
##    data.append(sock.recv(1000))
##    print(data)
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

while(i < 10):
    try:
        message = 'MEAS:POW?\r\n'.encode()
        print(message)
        sock.send(message)
        data = sock.recv(1000)
        print(data)
        data_dec = data.decode()
        new_data = data_dec.split(';')
        print(new_data)
##        data.append(sock.recv(1000))
##        print(data)
        filter_analyserdata(data_dec)
        time.sleep(1)
        i = i + 1
    except Exception as e:
        print(e)
        
##try:
##    #start = input("Enter anything\t")
##    data = sock.recv(20)
##    print(data)
####    message = 'anonymous\n'.encode()
####    sock.send(message)
####    print(message)
####    data = sock.recv(10)
####    print(data)
##    
##    message = "\x80\x00\x00\x09anonymous".encode('latin-1')
##    print(message)
##    sock.send(message)
##    data = sock.recv(1000)
##    print(data)
##    data = sock.recv(1000)
##    print(data)
##    
##    message = "\x80\x00\x00\x00".encode('latin-1')
##    print(message)
##    sock.send(message)
##    
##    data = sock.recv(1000)
##    print(data)
##    data = sock.recv(1000)
##    print(data)
####    data = sock.recv(1000)
####    print(data)
##    message = "\x80\x00\x00\x05*IDN?".encode('latin-1')
##    print(message)
##    sock.send(message)
##    data = sock.recv(1000)
##    print(data)
##    
####    message = "COMM:REM 1".encode('latin-1')
####    print(message)
####    sock.send(message)
##    
##    
##    message = "\x80\x00\x00\x0a:STAT:ERR?".encode('latin-1')
##    print(message)
##    sock.send(message)
##    data = sock.recv(1000)
##    print(data)
##    
##    message = "\x80\x00\x00\x04*CLS".encode('latin-1')
##    print(message)
##    sock.send(message)
##    
##    data = sock.recv(1000)
##    print(data)
##
##    message = "\x80\x00\x00\x05*IDN?".encode('latin-1')
##    print(message)
##    sock.send(message)
##    
##    data = sock.recv(1000)
##    print(data)
##
##    time.sleep(5)
##
##    message = "\x80\x00\x00\x0b:HARM:STAT?".encode('latin-1')
##    print(message)
##    sock.send(message)
##    
##    data = sock.recv(1000)
##    print(data)
##
##    command = '\x80\x00\x00\x0a:HARM:OBJ?'.encode('latin-1')
##    print(command)
##    sock.send(command)
##    state = sock.recv(10)
##    print(state)
##
##    command = '\x80\x00\x00\x0e:NUM:HARM:VAL?'.encode('latin-1')
##    print(command)
##    sock.send(command)
##    state = sock.recv(2100)
##    print(state)
##    
##except Exception as e:
##    print(e)
####finally:
####    print(sys.stderr, 'closing socket')
##  sock.close()
    
