import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

##def animate(i):
    #--------GET DATA----------#
    ##pullData = open("sampleText.txt","r").read()
    #-------PULL USEFUL INFO OUT OF IT-------------#
    ##dataArray = pullData.split('\n')
    ##xar = []
    ##yar = []
##    for eachLine in dataArray:
##        if len(eachLine)>1:
##            x,y = eachLine.split(',')
##            xar.append(int(x))
##            yar.append(int(y))
##    
##    ax1.clear()
##    ax1.plot(xar,yar)


def animate(i):
    #Get data in array format
    getdata = askforData()
    #Convert values into float format

    xar = []
    yar = []

    #data point to 
    




#--------------------INITIALIZATION-------------------#
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
    message = 'MEAS:ITEM:POW 55,33,33,63,0\r\n'.encode()
    print(message)
    sock.send(message)
except:
    print("Failed!")



ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
