from __future__ import division     #int div to float
########################################################################
# Title: Rohde & Schwarz Simple ATE example GUI
# Description:
#
#
########################################################################
# User Input Settings
########################################################################
btnWid = 11
Col0Wid = 10                                       #Text Labels
Col1Wid = 14                                       #Text Input
ColxWid = 4*(btnWid+4) -4
BotWindWid = Col0Wid+Col1Wid+ColxWid+10
maxCol = 6
btnRow = 20 
ClrTxtBg    = "black"                              #gray30
ClrTxtFg    = "green"
ColorCurs   = "white"
ClrAppBG    = "grey30"

########################################################################
### Code Start
########################################################################
try:                 ### Python 2.x naming
   import Tkinter as Tk
   import ttk
   import tkFileDialog
except:              ### Python 3.x naming
   import tkinter as Tk
   from tkinter import ttk
   import tkinter.filedialog as tkFileDialog
END = Tk.END

#Code specific libraries
import csv
import copy
from datetime  import datetime
from os.path   import split
from yaVISA    import jaVisa

########################################################################
### Functions
########################################################################
class GUIData(object):
   def __init__(self):
      GUIData.K2_IP = "127.0.0.1"
      GUIData.K2_SCPI = "*IDN?"
      GUIData.FreqArry = ""
      GUIData.WvArry = ""
      GUIData.PwrArry = ""
      
def mnu_TopWindLoad_Files():
   lstTopWind.delete(0,END)
   filez = tkFileDialog.askopenfilenames()
   fileList = list(filez)
   for i in fileList:
      lstTopWind.insert(END,i)
   lstTopWind.see(END)

def mnu_TopWindLoad_Read():
   lstTopWind.delete(0,END)
   filez = tkFileDialog.askopenfilename()
   fprintf(filez)
#   for i in fileList:
#      lstTopWind.insert(END,i)
   lstTopWind.see(END)
 
def mnu_TopWindClear():
   posi = lstTopWind.curselection()
   lstTopWind.delete(0,END)

def mnu_SaveCond():
   dataSave()

def btn_Clear():
   posi = lstBotWind.curselection()
   lstBotWind.delete(0,END)
   
def btn_IDN():
   fprintf("--> *IDN?")
   K2 = jaVisa()
   K2.jav_Open(Entry1.get())
   readStr = K2.query("*IDN?")
   fprintf("<-- " + readStr)
   K2.jav_Close()
   
def btn_Query():
   fprintf("--> " + Entry2.get())
   K2 = jaVisa()
   K2.jav_Open(Entry1.get())
   readStr = K2.query(Entry2.get())
   fprintf("<-- " + readStr)
   K2.jav_Close()
         
def btn_Scan():
   fprintf("[Resource List]")
   K2 = jaVisa()
   InstrList = K2.jav_reslist()
   for i in InstrList:
      fprintf("   " + i)
   K2.jav_Close()

def btn_SCPIList():
   fprintf("[SCPI LIST]")
   K2 = jaVisa()
   K2.jav_Open(Entry1.get())
   SCPIList = list(lstTopWind.get(0,END))
   OutList = K2.jav_scpilist(SCPIList)
   try:
      fprintf('   Err:' + ''.join(K2.jav_Close()))
   except:
      pass

   for Ostr in OutList:
      fprintf("   " + Ostr)
   
def btn_Write():
   fprintf("--> " + Entry2.get())
   K2 = jaVisa()
   K2.jav_Open(Entry1.get())
   K2.write(Entry2.get())
   K2.jav_Close()
   
def menu_Open():
   asdf = tkFileDialog.askopenfilename()
   print(asdf)
   
def menu_Exit():
   global GUI
   dataSave() 
   GUI.quit()
   GUI.destroy()
   print("Program End")

def menu_Save():
   dataSave()

def ArrayInput(stringIn):
   OutputList = []
   InputList = stringIn.split(",")
   for i in InputList:
      i = i.strip()
      OutputList.append(i)
   return OutputList
   
def fprintf(inStr):
   sDate = datetime.now().strftime("%y%m%d-%H%M%S.%f") #Date String
   try:
      if 0:    #Text moves down
         lstBotWind.insert(Tk.INSERT,"%s %s\n"%(sDate[:-3],inStr))
      else:    #Text moves up
         lstBotWind.insert(END,"%s %s\n"%(sDate[:-3],inStr))
         lstBotWind.see(END)
      GUI.update()
   except: 
      pass

def dataSave():
   #RSVar.WvArry = list(lstTopWind.get(0,END))
   f = open("yaVISA_GUI.csv","wb")
   f.write('%s,'%(Entry1.get()))
   f.write('%s,'%(Entry2.get()))
   f.close()
   
   fprintf("DataSave: File Saved")

def dataLoad():
   OutObj = GUIData()
   try:
      f = open("yaVISA_GUI.csv","rb")
      data = f.read().split(',')
      OutObj.K2_IP   = data[0]
      OutObj.K2_SCPI = data[1]
   except:
      fprintf("DataLoad: Default")
   return OutObj
                 
########################################################################
### GUI Object
RSVar = copy.copy(dataLoad())
GUI = Tk.Tk()                                      #Create GUI object
GUI.title("Rohde&Schwarz VISA Utility")            #GUI Title
#GUI.iconbitmap('RSIcon.ico')
GUI.resizable(0,0)
GUI.config(bg=ClrAppBG)

########################################################################
### Define GUI Widgets
Lbl1   = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text="Instrument IP")          #Create Label
Entry1 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg,insertbackground=ColorCurs) #Create Entry background
Entry1.insert(END,RSVar.K2_IP)                                                   #Default Value
Lbl2   = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text="SCPI String")            #Create Label
Entry2 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg,insertbackground=ColorCurs) #Entry Background
Entry2.insert(END,RSVar.K2_SCPI)                                                 #Default Value
Lbl3   = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text="Freq Array")             #Create Label
Entry3 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg,insertbackground=ColorCurs) #Entry Background
Entry3.insert(END,RSVar.FreqArry)                                                #Default Value
Lbl4   = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text="Power Array")            #Create Label
Entry4 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg,insertbackground=ColorCurs) #Entry Background
Entry4.insert(END,RSVar.PwrArry)                                                 #Default Value
btnWaveF = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,text="VISA Scan",  command = btn_Scan)
btnWaveC = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,text="SCPI List",  command = btn_SCPIList)
btnSaveC = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,text="*IDN?",      command = btn_IDN)
btnClear = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,text="Query",      command = btn_Query)
btnRunIt = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,text="Write",      command = btn_Write)
btnQuit  = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,text="Quit",       command = menu_Exit)

########################################################################
### List Boxes
lstBotWind = Tk.Text(GUI, width=BotWindWid, bg=ClrTxtBg, fg=ClrTxtFg, wrap=Tk.CHAR, height=20)
srlBotWind = ttk.Scrollbar(GUI, orient=Tk.VERTICAL, command=lstBotWind.yview) #Create scrollbar
lstBotWind.config(yscrollcommand=srlBotWind.set)                              #Link scroll to lstBotWind
lstBotWind.insert(Tk.INSERT,"Output Window\n")
lstBotWind.tag_add("here", "1.0", "1.40")
lstBotWind.tag_config("here", background="yellow", foreground="blue")

lstTopWind = Tk.Listbox(GUI,bg=ClrTxtBg, fg=ClrTxtFg,width=ColxWid)
srlTopWind = ttk.Scrollbar(GUI, orient=Tk.VERTICAL, command=lstTopWind.yview) #Create scrollbar
lstTopWind.insert(0,"*IDN?")
lstTopWind.insert(0,"*OPT?")
for item in RSVar.WvArry:
   lstTopWind.insert(END, item)
lstTopWind.config(yscrollcommand=srlTopWind.set)                              #Link scroll to lstTopWind

########################################################################
### Draw Widgets w/ Grid
Lbl1.grid(row=0,column=0,sticky=Tk.E)
Lbl2.grid(row=1,column=0,sticky=Tk.E)
#Lbl3.grid(row=2,column=0,sticky=Tk.E,columnspan=1)
#Lbl4.grid(row=3,column=0,sticky=Tk.E,columnspan=1)
Entry1.grid(row=0,column=1)
Entry2.grid(row=1,column=1)
#Entry3.grid(row=2,column=1,columnspan=1)
#Entry4.grid(row=3,column=1,columnspan=1)
btnWaveF.grid(row=btnRow,column=0)
btnWaveC.grid(row=btnRow,column=1)
btnSaveC.grid(row=btnRow,column=2)
btnClear.grid(row=btnRow,column=3)
btnRunIt.grid(row=btnRow,column=4)
btnQuit.grid(row=btnRow,column=5)

lstTopWind.grid(row=0,column=2,columnspan=4,rowspan=4, sticky=(Tk.E))
srlTopWind.grid(column=maxCol,row=0,rowspan=4,sticky=(Tk.W,Tk.N,Tk.S))
lstBotWind.grid(row=btnRow-1,column=0,columnspan=(maxCol),sticky=Tk.E)
srlBotWind.grid(column=maxCol,row=btnRow-1, sticky=(Tk.W,Tk.N,Tk.S))

# *****************************************************************
# Define menu
# *****************************************************************
menu = Tk.Menu(GUI)                                #create dropdown in GUI
GUI.config(menu=menu)                              #define GUI's menu

fileMenu = Tk.Menu(menu)                           #create dropdown menu
fileMenu.add_command(label="Open",command=menu_Open)
fileMenu.add_command(label="Save",command=menu_Save)
fileMenu.add_separator()
fileMenu.add_command(label="SCPI Load", command=mnu_TopWindLoad_Read)
fileMenu.add_command(label="SCPI Clear",command=mnu_TopWindClear)
fileMenu.add_separator()
fileMenu.add_command(label="Exit",command=menu_Exit)

editMenu = Tk.Menu(menu)                           #create dropdown menu
editMenu.add_command(label="Edit",command=menu_Open)

menu.add_cascade(label="File",menu=fileMenu)       #add dropdown menu
menu.add_cascade(label="Edit",menu=editMenu)       #add dropdown menu

# *****************************************************************
# Start Program
# *****************************************************************
GUI.mainloop()       #Display window
