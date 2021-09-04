#-------------------------Tkinter Modules---------------------------------#
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
#------------------------Modules Communicating with Analyser------------------#
import socket
##import normalmeasurement as nm
##import harmonicmeasurement as hm
###---------------------------Other Modules---------------------------------#
##import save_to_excel as stxl
import xlsxwriter
import sys
import concurrent.futures
from PIL import Image
from PIL import ImageTk
from io import BytesIO
import threading
import time
#----------------------------------Program-------------------------------#

#col = 2 #Set column number for the first readings. It's start from the column C in excel

class ConnecttoAnalyser():
    def __init__(self,master):
        #------------------Declarations----------------------------------------------#
        self.sock = None
        self.wk = self.ws = self.listnmdata = self.listsiga = self.listsigb = None
        self.col = 2
        self.startKeepAlive = 0
        self.t1 = None
        #-----------------------------------------------------------------------------$
        self.master = master
        self.master.title("ConnecttoAnalyser")
        self.master.resizable(0,0)
        #vertivlogo = PhotoImage(file = "vertiv.png")
        #window.iconphoto(False,vertivlogo)

        #Frames
        self.topframe = tk.Frame(self.master, bd = 5, relief = tk.RIDGE)
        self.bottomframe = tk.Frame(self.master, bd = 5, relief = tk.RIDGE)
        self.rightframe = tk.Frame(self.master, bd = 5, width = 900, height = 500, relief = tk.RIDGE)

        #Frames Layout
        self.topframe.grid(row = 0, sticky = "NSEW", padx = 10, pady = 10)
        self.bottomframe.grid(row = 3, sticky = "NSEW", padx = 10)
        self.rightframe.grid(row = 0, column = 5, rowspan = 7, sticky = "NSEW", padx = 10, pady = 10)

        #Top fram variables
        self.var = [tk.StringVar() for i in range(4)]
        
        #Top frame Widgets
        self.enterip = tk.Label(self.topframe, text = "Enter IP address")
        self.ip1 = tk.Entry(self.topframe, textvariable = self.var[0], width = 3)
        self.dot1 = tk.Label(self.topframe, text = ".")
        self.ip2 = tk.Entry(self.topframe, textvariable = self.var[1], width = 3)
        self.dot2 = tk.Label(self.topframe, text = ".")
        self.ip3 = tk.Entry(self.topframe, textvariable = self.var[2], width = 3)
        self.dot3 = tk.Label(self.topframe, text = ".")
        self.ip4 = tk.Entry(self.topframe, textvariable = self.var[3], width = 3)
        self.establishcomm = tk.Button(self.topframe, text = "Connect",activebackground='#00ff00', command = self.initialisation)  #Initialisation Button
        
        #Top frame Widget Layout
        self.enterip.grid(row = 0,column = 0, pady = 10, padx = 10)
        self.ip1.grid(row = 0,column = 1, pady = 10, padx = 10)
        self.dot1.grid(row = 0,column = 2, pady = 10, padx = 10)
        self.ip2.grid(row = 0,column = 3, pady = 10, padx = 10)
        self.dot2.grid(row = 0,column = 4, pady = 10, padx = 10)
        self.ip3.grid(row = 0,column = 5, pady = 10, padx = 10)
        self.dot3.grid(row = 0,column = 6, pady = 10, padx = 10)
        self.ip4.grid(row = 0,column = 7, pady = 10, padx = 10)
        self.establishcomm.grid(row = 1,column = 1, ipadx = 50, ipady = 10, rowspan = 2, columnspan = 8, sticky = "W")
        
        #Bottom frame
        self.message1 = tk.Label(self.bottomframe, text = "Select folder to save report")
        self.location = tk.StringVar()
        self.disp_loc = tk.Entry(self.bottomframe, width = 20, textvariable = self.location)
        self.browse = tk.Button(self.bottomframe, text = "Browse",activebackground='#00ff00', command = self.open_folder)
        self.name1 = tk.Label(self.bottomframe, text = "Enter name of the report")
        self.rname = tk.StringVar()
        self.reportname = tk.Entry(self.bottomframe,textvariable = self.rname,width  = 20)
        self.CreateExcelFile = tk.Button(self.bottomframe, text = "Create Excel File",activebackground='#00ff00', command = self.CreateExcel)
        #-------------------------------------Get Data from Analyser and Store it in a Excel file-----------------------------------------------------------------------------#
        self.load = tk.Label(self.bottomframe, text = "Load Percentage")
        self.Lvar = tk.StringVar()
        self.loadvalue = tk.Entry(self.bottomframe, width = 20, textvariable = self.Lvar)
        self.counter = tk.IntVar() #Mentions number of readings
        self.counter.set(0)
        self.setload = tk.Button(self.bottomframe, text = "Set Load", command = self.onClick)
        self.lbl = tk.Label(self.bottomframe, textvariable = self.counter)
        self.readings = tk.Label(self.bottomframe, text = "Number of Readings")

        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        #Bottom frame Widget Layout

        self.message1.grid(row = 3,column = 0, padx = 10, pady = 10, sticky = "E")
        self.disp_loc.grid(row = 3,column = 1, padx = 10, pady = 10, sticky = "EW", columnspan = 3)
        self.browse.grid(row = 3,column = 4, padx = 10, pady = 10)

        self.name1.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = "E")
        self.reportname.grid(row = 4, column = 1, padx = 10, pady = 10,columnspan = 2, sticky = "EW")
        self.CreateExcelFile.grid(row = 4, column = 3, padx = 10, pady = 10,sticky ="EW")

        self.load.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = "E")
        self.loadvalue.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = "EW")
        self.setload.grid(row = 5, column = 2, padx = 10, pady = 10, sticky = "EW")
        self.readings.grid(row = 5, column = 3, padx = 10, pady = 10, sticky = "EW")
        self.lbl.grid(row = 5, column = 4, padx = 10, pady = 10, sticky = "EW")

        #Right Frame
        self.snap = tk.Button(self.rightframe, text = "Take Screenshot", command = self.calldisplayscreenshot)
        self.count = tk.IntVar()        #For storing count of pictures
        self.count.set(0)
        self.CheckVar1 = tk.IntVar()
        self.C1 = tk.Checkbutton(self.rightframe, text = "Take Pictures\nalong with\nvalues of parameters", variable = self.CheckVar1, onvalue = 1, offvalue = 0, height = 3, width = 20)

        self.Normalvalues = tk.Button(self.rightframe,text= "Get Normal Measurement",activebackground='#0000ff',command = self.GetNormalParameters)
        self.HarmonicvaluesSIGA = tk.Button(self.rightframe,text = "Get Harmonic Measurement SIGA",activebackground='#0000ff',command = self.GetHarmonicParametersSIGA)
        self.HarmonicvaluesSIGB = tk.Button(self.rightframe,text = "Get Harmonic Measurement SIGB",activebackground='#0000ff',command = self.GetHarmonicParametersSIGB)
        self.SavetoExcel = tk.Button(self.rightframe, text = "Save to Excel",activebackground='#0000ff',command = self.SendtoExcel)
        self.Exitbutton = tk.Button(self.rightframe, text = "Exit",activebackground='#0000ff',command = self.closeandexit)
##        self.progress = tk.Text(self.rightframe,height = 2, width = 20)
##        self.scroll = tk.Scrollbar(self.rightframe)
##        self.scroll.config(command = self.progress.yview)
##        self.progress.config(yscrollcommand= self.scroll.set)
##        
        #Right Frame Layout
        self.snap.grid(row = 0, column = 5, padx = 10, pady = 10, sticky = "EW")
        self.C1.grid(row = 1, column = 5, padx = 10, pady = 10, sticky = "EW")
        self.Normalvalues.grid(row = 2, column = 5, padx = 10, pady = 10, sticky = "NSEW")
        self.HarmonicvaluesSIGA.grid(row = 3, column = 5, padx = 10, pady = 10, sticky = "NSEW")
        self.HarmonicvaluesSIGB.grid(row = 4, column = 5, padx = 10, pady = 10, sticky = "NSEW")
        self.SavetoExcel.grid(row = 5, column = 5, padx = 10, pady = 10, sticky = "NSEW")
        self.Exitbutton.grid(row = 6, column = 5, padx = 10, pady = 10, sticky = "EW")
##        self.progress.grid(row = 7, column = 5, sticky = "EW")
##        self.scroll.grid(row = 7, column = 6, sticky = "EW")
        #----------------------------------------------------------------------------------------------------------------#
    def initialisation(self):
        try:
            # Create a TCP/IP socket
            self.startKeepAlive = 0
            #self.t1.join()
            socket.setdefaulttimeout(5)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip = self.var[0].get() + '.' + self.var[1].get() + '.' + self.var[2].get() + '.' + self.var[3].get()
            # Connect the socket to the port where the server is listening
            server_address = (ip, 3100)
            print(sys.stderr, 'connecting to %s port %s' % server_address)
            
            self.sock.connect(server_address)

##            data = self.sock.recv(100)
##            print(data)
##            message = "\x80\x00\x00\x09anonymous".encode('latin-1')
##            print(message)
##            self.sock.send(message)
##            #time.sleep(0.1)
##            data = self.ReadData()
##            print(data)
##            
##            message = "\x80\x00\x00\x00".encode('latin')
##            print(message)
##            self.sock.send(message)
##            data = self.ReadData()
##            print(data)
            
##            message = "\x80\x00\x00\x05*IDN?".encode('latin-1')
##            message = "*IDN?".encode('latin-1')
##            print(message)
##            self.sock.send(message)
##            #time.sleep(0.1)
##            identity = self.ReadData()
##            
##            print(identity)

        except Exception as e:
            print(e)
            messagebox.showerror("Connection Error",e)
        else:
            print("Connection Complete")
            messagebox.showinfo("Communication established successfully!",("Connected to :" + identity[4:].decode('latin-1')))
            #self.startKeepAlive = 1
            #self.StartThread()
            
            
    def open_folder(self):
        filelocation = filedialog.askdirectory()
        self.disp_loc.delete(0,tk.END)
        self.disp_loc.insert(0,filelocation)


        
    def CreateExcel(self):
        try:
            if (self.location.get().strip() == '') or (self.rname.get().strip() == ''):
                raise Exception("Necessary Details not provided")
            self.wk, self.ws = stxl.create_excel_workbook(self.location.get(),self.rname.get())
        except Exception as error:
            messagebox.showerror("Unable to create Excel File",error)
        else:
            messagebox.showinfo("Hurray!","Excel File created successfully!")


    def onClick(self):
        try:
            self.counter.set(self.counter.get() + 1)
        except Exception as error:
            messagebox.showerror("Error", error)


    def RemoveSpecialCharacters(self,string1):
        Lname = string1.strip()
        Lnamealphanum = [character for character in Lname if character.isalnum()] #Removes Special Characters
        Lnamewithoutsc = "".join(Lnamealphanum)
        if len(Lnamewithoutsc) > 4:                                               #Total Length of the name cannot be greater than 6
            numbers = [str(int(float(i)/10)) for i in Lname.split(',')]          #Removes Ambiguity e.g. 100,20,30 and 10,20,30 would result into 10,2,3 and 1,2,3
            Lname_modified = ''.join(numbers)                                     #e.g. 10,2,3 is joined as 1023
            if len(Lname_modified) > 4:
                raise Exception("Enter appropriate Value")
            return Lname_modified
        else:
            return Lnamewithoutsc


    def GetNormalParameters(self):
        try:
            self.startKeepAlive = 0
            self.t1.join()
            
##            command = '\x80\x00\x00\x0b:HARM:STAT?'.encode('latin-1')
##            self.sock.send(command)
##            hstate = self.sock.recv(100)
##            print("hstate", hstate)
##            if hstate[4:].decode() != '0\n':
##               raise Exception("Turn Normal measurement mode ON")

            normaldata = nm.normal_measurement(self.sock)
            self.listnmdata = self.filter_analyserdata(normaldata)

            if self.CheckVar1 == 1 :
                image = self.imagereceive()
                time.sleep(0.1)
                self.displayscreenshot(image)
            
            
        except Exception as e:
            messagebox.showerror("Error", e)
        else:
            messagebox.showinfo("Data Transfer", "Successful!")
            self.startKeepAlive = 1
            self.StartThread()
            
        
            
    def GetHarmonicParametersSIGA(self):
        try:
            self.startKeepAlive = 0
            self.t1.join()
            
##            command = '\x80\x00\x00\x0b:HARM:STAT?'.encode('latin-1')
##            self.sock.send(command)
##            hstate = self.sock.recv(6)
##            print("hstate", hstate)
##            if hstate[4:].decode() != '1\n':
##               raise Exception("Turn Harmonics measurement mode ON")
            
##            command = '\x80\x00\x00\x0a:HARM:OBJ?'.encode('latin-1')
##            self.sock.send(command)
##            state = self.sock.recv(10)
##            if state[4:].decode() == 'SIGMB\n':
##               raise Exception("Turn SIGMA mode ON")

            harmonicdataA = hm.harmonic_measurement(self.sock)
            self.listsiga = self.filter_analyserdata(harmonicdataA)
            if self.CheckVar1 == 1 :
                image = self.imagereceive()
                time.sleep(0.1)
                self.displayscreenshot(image)
        
        
        except Exception as e:
            messagebox.showerror("Error", e)
        else:
            messagebox.showinfo("Data Transfer", "Successful!")
            self.startKeepAlive = 1
            self.StartThread()
            
            
    def GetHarmonicParametersSIGB(self):
        
        try:
            self.startKeepAlive = 0
            self.t1.join()
##            
##            command = '\x80\x00\x00\x0b:HARM:STAT?'.encode('latin-1')
##            self.sock.send(command)
##            hstate = self.sock.recv(6)
##            print("hstate", hstate)
##            if hstate[4:].decode() != '1\n':
##               raise Exception("Turn Harmonics measurement mode ON")
##            
##            command = '\x80\x00\x00\x0a:HARM:OBJ?'.encode('latin-1')
##            self.sock.send(command)
##            state = self.sock.recv(10)
##            if state[4:].decode() == 'SIGMA\n':
##               raise Exception("Turn SIGMB mode ON")
##  
            harmonicdataB = hm.harmonic_measurement(self.sock)
            self.listsigb = self.filter_analyserdata(harmonicdataB)
            if self.CheckVar1 == 1 :
                image = self.imagereceive()
                time.sleep(0.1)
                self.displayscreenshot(image)
        
                    
        except Exception as e:
            messagebox.showerror("Error", e)
        else:
            messagebox.showinfo("Data Transfer", "Successful!")
            self.startKeepAlive = 1
            self.StartThread()
            
            
    def SendtoExcel(self):
        try:
            stxl.save_to_workbook(self.wk, self.ws, self.Lvar.get(), self.col, self.listnmdata, self.listsiga, self.listsigb)
            self.col = self.col + 1   #Next column for the next readings
            messagebox.showinfo("Congrats!", "Data Loaded to Excel Successfully")
        except Exception as error:
            messagebox.showerror("Data couldn't be loaded to Excel",error)
##        stxl.save_to_workbook(self.wk, self.ws, self.Lvar.get(), self.col, self.listnmdata, self.listsiga, self.listsigb)
##        self.col = self.col + 1   #Next column for the next readings
##        messagebox.showinfo("Congrats!", "Data Loaded to Excel Successfully")


    def closeandexit(self):
        try:
            self.startKeepAlive = 0
            self.t1.join()
            window.destroy()
        except Exception as error:
            messagebox.showerror("Unable to close",error)
        else:
            try:
                stxl.closeworkbook(self.wk)
                self.sock.close()
            except:
                pass
            

    def filter_analyserdata(self,data):
        try:
            print(data)
            data_without_G = data.replace('G','')
            data_without_GD = data_without_G.replace('D','')
            data_replace_INF = data_without_GD.replace('INF', '5555')
            data_replace_NAN = data_replace_INF.replace('NAN','9999')
            list_data_str = data_replace_NAN.split(',')
            list_values = [float(value) for value in list_data_str]
            print(list_values)
            
            return list_values
        except:
            messagebox.showerror("Impicit Data Convesion", "Data Conversion Error")

    def imagereceive(self):
        message = "\x80\x00\x00\x0b:IMAG:SEND?".encode('latin-1')
        print(message)
        self.sock.send(message)
        data = self.sock.recv(700)
        time.sleep(0.02)
        num = 38000
        while(num>0):
            d = self.sock.recv(1000)
            #print(d)
            time.sleep(0.02)
            data = data + d
            num = num - 1000
            
        print(data[0:20])
        print(data[12:])
        
        image = Image.open(BytesIO(data[12:]))
        return image



    def displayscreenshot(self,image):
        try:
            #image = self.imagereceive()
            #image.show()
            
            l = self.location.get()
            l.replace('/', '\\')
            savehere = l + '\\' + 'PIC' + str(self.count.get() + 10) + '.bmp'
            image.save(savehere)
            self.count.set(self.count.get() + 1)
            
        except Exception as e:
            messagebox.showerror("Error",e)
            

    def calldisplayscreenshot(self):
        self.startKeepAlive = 0
        self.t1.join()
        #self.displayscreenshot()
        image = self.imagereceive()
        time.sleep(0.1)
        self.startKeepAlive = 1
        self.StartThread()
        self.displayscreenshot(image)
        

    def StartThread(self, ):
        self.t1 = threading.Thread(target = self.KeepAlive)
        self.t1.start()

    def KeepAlive(self):
        try:
            while(self.startKeepAlive == 1):
                print("It is inside")
                command = '\x80\x00\x00\x0a:STAT:ERR?'.encode('latin-1')
                print(command)
                self.sock.send(command)
                data = self.ReadData()
                print(data)
                time.sleep(0.5)
                
                
                command = '\x80\x00\x00\x05*IDN?'.encode('latin-1')
                print(command)
                self.sock.send(command)
                identity = self.ReadData()
                print(identity)
                time.sleep(0.5)
                            
        except Exception as e:
            print(e)
            messagebox.showerror("Error", e)

    def ReadData(self):
        temp1 = self.sock.recv(5)
        time.sleep(0.01)
        temp2 = self.sock.recv(30)
        return (temp1 + temp2)
            
            


window = tk.Tk()
mygui = ConnecttoAnalyser(window)
window.mainloop()
