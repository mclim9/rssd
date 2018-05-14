from __future__ import division     #int div to float
# *****************************************************************
# Title: Rohde & Schwarz Simple ATE example GUI
#
# Description:
#
#
# *****************************************************************
# User Input Settings
# *****************************************************************
btnWid = 15
textWindWid = 120
maxCol = 6
btnRow = 20
ColorBG = "black"  #gray30
ColorFG = "green"
ColorCurs = "White"

# *****************************************************************
# Code Start
# *****************************************************************
#from Tkinter import *
import Tkinter
import ttk
import tkMessageBox
import tkFileDialog
END = Tkinter.END

#Code specific libraries
import random
import math
import pickle
import copy
from RSVar import RSATE
import RSATE_K96
from os.path import split
import test

# *****************************************************************
# Functions
# *****************************************************************
def btn_Button():
   pass
   
def btn_Waveforms():
   lstWaveF.delete(0,END)
   filez = tkFileDialog.askopenfilenames()
   fileList = list(filez)
   for i in fileList:
      lstWaveF.insert(END,i)
   lstWaveF.see(END)
 
def btn_ClearWaves():
   posi = lstWaveF.curselection()
   lstWaveF.delete(0,END)

def btn_SaveCond():
   RSVar.SMW_IP = Entry1.get()
   RSVar.FSW_IP = Entry2.get()
   RSVar.WvArry = list(lstWaveF.get(0,END))
   RSVar.FreqArry = Entry3.get()
   RSVar.PwrArry  = Entry4.get()
   dataSave(RSVar)
   
def btn_Test():
   test.funcy(GUI,lstOutpt)
   
def btn_Clear():
   posi = lstOutpt.curselection()
   lstOutpt.delete(0,END)

def btn_RunLoops():
   fprintf("RSATERun: Run Tests")
   btn_SaveCond()
   RSVar.FreqArry = map(float,ArrayInput(Entry3.get()))
   RSVar.PwrArry  = map(float,ArrayInput(Entry4.get()))
   for i, item in enumerate(RSVar.WvArry):
      head, tail = split(item)       
      RSVar.WvArry[i] = tail.split(".")[0]
   RSVar.GUI_Element = lstOutpt
   RSVar.GUI_Object = GUI
   RSATE_K96.main(RSVar)
   fprintf("RSATERun: Tests Done")
   
def menu_Open():
   asdf = tkFileDialog.askopenfilename()
   print asdf
   
def menu_Exit():
   global GUI
   btn_SaveCond()
   GUI.quit()
   GUI.destroy()
   print("Program End")

def menu_Save():
   dataSave(RSVar)

def ArrayInput(stringIn):
   OutputList = []
   InputList = stringIn.split(",")
   for i in InputList:
      i = i.strip()
      OutputList.append(i)
   return OutputList
   
def fprintf(inStr):
   #print(inStr)
   try:
      #lstOutpt.insert(END,inStr)
      lstOutpt.insert(0,inStr)
      #lstOutpt.see(END)
      GUI.update()
   except:
      pass

def dataSave(data):
   with open("RSATE_GUI.dat","wb") as f:
      pickle.dump(data, f)
   fprintf("DataSave: File Saved")

def dataLoad():
   try:
      with open("RSATE_GUI.dat","rb") as f:
         data = pickle.load(f)
      fprintf("DataLoad: OK")
   except:
      data = RSATE()
      fprintf("DataLoad: Default")
   return data
                 
# *****************************************************************
# Define GUI Widgets
# *****************************************************************
RSVar = copy.copy(dataLoad())
GUI = Tkinter.Tk()                                 #Create GUI object
GUI.title("Rohde Schwarz DemoATE")                 #GUI Title
Lbl1 = Tkinter.Label(GUI, text="SMW IP")           #Create Label
Entry1 = Tkinter.Entry(GUI,bg=ColorBG, fg=ColorFG,insertbackground=ColorCurs) #Create Entry background
Entry1.insert(END, RSVar.SMW_IP)                   #Default Value
Lbl2 = Tkinter.Label(GUI, text="FSW IP")           #Create Label
Entry2 = Tkinter.Entry(GUI,bg=ColorBG, fg=ColorFG,insertbackground=ColorCurs) #Entry Background
Entry2.insert(END, RSVar.FSW_IP)                   #Default Value
Lbl3 = Tkinter.Label(GUI, text="Freq Array")       #Create Label
Entry3 = Tkinter.Entry(GUI,bg=ColorBG, fg=ColorFG,insertbackground=ColorCurs) #Entry Background
Entry3.insert(END, RSVar.FreqArry)                 #Default Value
Lbl4 = Tkinter.Label(GUI, text="Power Array")      #Create Label
Entry4 = Tkinter.Entry(GUI,bg=ColorBG, fg=ColorFG,insertbackground=ColorCurs) #Entry Background
Entry4.insert(END, RSVar.PwrArry)                  #Default Value
btnWaveF = Tkinter.Button(GUI, width=btnWid, text = "Select *.WV", command = btn_Waveforms)
btnWaveC = Tkinter.Button(GUI, width=btnWid, text = "Clear Waves", command = btn_ClearWaves)
btnSaveC = Tkinter.Button(GUI, width=btnWid, text = "Save", command = btn_SaveCond)
btnClear = Tkinter.Button(GUI, width=btnWid, text = "Test", command = btn_Test)
btnRunIt = Tkinter.Button(GUI, width=btnWid, text = "Run", command = btn_RunLoops)
btnQuit  = Tkinter.Button(GUI, width=btnWid, text = "Quit", command = menu_Exit)
lstOutpt = Tkinter.Listbox(GUI, width=textWindWid,bg=ColorBG, fg=ColorFG)
srlOutpt = ttk.Scrollbar(GUI, orient=Tkinter.VERTICAL, command=lstOutpt.yview) #Create scrollbar S
lstOutpt.config(yscrollcommand=srlOutpt.set)            #Link lstOutpt change to S
lstWaveF = Tkinter.Listbox(GUI,bg=ColorBG, fg=ColorFG,width=80)
srlWaveF = ttk.Scrollbar(GUI, orient=Tkinter.VERTICAL, command=lstWaveF.yview) #Create scrollbar S
for item in RSVar.WvArry:
    lstWaveF.insert(END, item)

lstWaveF.config(yscrollcommand=srlWaveF.set)            #Link lstWaveF change to S
lstFrequ = Tkinter.Listbox(GUI,bg=ColorBG, fg=ColorFG)
lstPower = Tkinter.Listbox(GUI,bg=ColorBG, fg=ColorFG)

# Grid up the Widgets
Lbl1.grid(row=0,column=0,sticky=Tkinter.E,columnspan=1)
Lbl2.grid(row=1,column=0,sticky=Tkinter.E,columnspan=1)
Lbl3.grid(row=2,column=0,sticky=Tkinter.E,columnspan=1)
Lbl4.grid(row=3,column=0,sticky=Tkinter.E,columnspan=1)
Entry1.grid(row=0,column=1,columnspan=1)
Entry2.grid(row=1,column=1,columnspan=1)
Entry3.grid(row=2,column=1,columnspan=1)
Entry4.grid(row=3,column=1,columnspan=1)
btnWaveF.grid(row=btnRow,column=0)
btnWaveC.grid(row=btnRow,column=1)
btnSaveC.grid(row=btnRow,column=2)
btnClear.grid(row=btnRow,column=3)
btnRunIt.grid(row=btnRow,column=4)
btnQuit.grid(row=btnRow,column=5)

lstWaveF.grid(row=0,column=2,columnspan=4,rowspan=5)
srlWaveF.grid(column=6,row=0,rowspan=5,sticky=(Tkinter.W,Tkinter.N,Tkinter.S))     
#lstFrequ.grid(row=0,column=4,rowspan=5)
#lstPower.grid(row=0,column=5,rowspan=5)
lstOutpt.grid(row=btnRow-1,column=0,columnspan=maxCol)
srlOutpt.grid(column=maxCol,row=btnRow-1, sticky=(Tkinter.W,Tkinter.N,Tkinter.S))     

# *****************************************************************
# Define menu
# *****************************************************************
menu = Tkinter.Menu(GUI)                        #create dropdown in GUI
GUI.config(menu=menu)

fileMenu = Tkinter.Menu(menu)                   #create dropdown in menu
fileMenu.add_command(label="Open",command=menu_Open)
fileMenu.add_command(label="Save",command=menu_Save)
fileMenu.add_separator()
fileMenu.add_command(label="Exit",command=menu_Exit)

editMenu = Tkinter.Menu(menu)                   #create dropdown in menu
editMenu.add_command(label="Edit",command=menu_Open)

menu.add_cascade(label="File",menu=fileMenu)    #add dropdown menu
menu.add_cascade(label="Edit",menu=editMenu)    #add dropdown menu

# *****************************************************************
# Start Program
# *****************************************************************
GUI.mainloop()       #Display window
