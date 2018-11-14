from __future__ import division     #int div to float
########################################################################
# Title: Rohde & Schwarz Simple ATE example GUI
# Description:
#
########################################################################
# User Input Settings
########################################################################
btnWid = 11
Col0Wid = 15                                       #Text Labels
Col1Wid = 15                                       #Text Input
ColxWid = 4*(btnWid+4) -4
BotWindWid = Col0Wid+Col1Wid+ColxWid
maxCol = 6
btnRow = 20 
ClrTxtBg    = "black"                              #gray30
ClrTxtFg    = "white"
BtnTxtFg    = "white"
ColorCurs   = "white"
ClrAppBG    = "grey30"

########################################################################       
### Code Import
########################################################################
from datetime                 import datetime
try:      #Python2 naming
   import Tkinter             as    Tk
   import ttk
   import tkFileDialog
except:   #Python3 naming
   import tkinter             as     Tk
   from   tkinter             import ttk
   import tkinter.filedialog  as     tkFileDialog
END = Tk.END
GUI = Tk.Tk()                                      #Create GUI object

#Code specific libraries
import copy
from rssd.yaVISA              import jaVisa
from rssd.FSW_5GNR_K144       import VSA
from rssd.SMW_5GNR_K144       import VSG
from rssd.examples.SMW_FSW_5GNR_K144_Read    import NR5G_ReadSettings
from rssd.examples.SMW_FSW_5GNR_K144_Set     import NR5G_SetSettings

########################################################################
### Functions
########################################################################
class GUIData(object):
   def __init__(self):
      self.Title     = "Rohde&Schwarz VISA Utility"
      self.EntTxt1   = "SMW IP"
      self.Entry1    = "192.168.1.114"
      self.EntTxt2   = "FSW IP"
      self.Entry2    = "192.168.1.109"
      self.EntTxt3   = "Frequency"
      self.Entry3    = "28000000000"
      self.EntTxt4   = "SMW Power,RMS"
      self.Entry4    = "-5"
      self.EntTxt10  = "Direction"
      self.Entry10   = "UL"
      self.EntTxt11  = "DeployFreq"
      self.Entry11   = "HIGH"
      self.EntTxt12  = "Ch BW,MHz"
      self.Entry12   = "100"
      self.EntTxt13  = "SubCarrier,kHz"
      self.Entry13   = "60"
      self.EntTxt14  = "RB"
      self.Entry14   = "100"
      self.EntTxt15  = "Modulation"
      self.Entry15   = "QPSK"
      self.List1     = ['K144 Settings']
      self.BtnTxt1   = '*IDN?'
      self.BtnTxt2   = ''
      self.BtnTxt3   = 'Max RB'
      self.BtnTxt4   = 'Set_5GNR'
      self.BtnTxt5   = 'Read_5GNR'
      
Enum10 = Tk.StringVar(GUI)
Enum10.set("UL") # default value
Enum11 = Tk.StringVar(GUI)
Enum11.set("HIGH") # default value
Enum12 = Tk.StringVar(GUI)
Enum12.set("100") # default value
Enum13 = Tk.StringVar(GUI)
Enum13.set("60") # default value
Enum15 = Tk.StringVar(GUI)
Enum15.set("QPSK") # default value

PullD10 = Tk.OptionMenu(GUI, Enum10, "UL", "DL")
PullD11 = Tk.OptionMenu(GUI, Enum11, "LOW", "MIDD", "HIGH")
PullD12 = Tk.OptionMenu(GUI, Enum12, "20","50","100","200","400")
PullD13 = Tk.OptionMenu(GUI, Enum13, "15", "30", "60", "120")
PullD15 = Tk.OptionMenu(GUI, Enum15, "QPSK", "QAM16", "QAM64", "QAM256")
      
def ArrayInput(stringIn):
   OutputList = []
   InputList = stringIn.split(",")
   for i in InputList:
      i = i.strip()
      OutputList.append(i)
   return OutputList

def btn1():
   ### *IDN Query ###
   SMW = VSG().jav_Open(Entry1.get())  #Create SMW Object
   FSW = VSA().jav_Open(Entry2.get())  #Create FSW Object
   windowLowerWrite(SMW.query('*IDN?'))
   windowLowerWrite(FSW.query('*IDN?'))
   SMW.jav_Close()
   FSW.jav_Close()
   
def btn2():
   pass
   
def btn3():
   ### Get Max RB ###
   SMW = VSG().jav_Open(Entry1.get())  #Create SMW Object
   data = SMW.Get_5GNR_RBMax()
   windowUpperWrite("")
   windowUpperWrite("=== Max RB ===")
   for i in data:
      windowUpperWrite("SubC:%d  RB Max:%d"%(i[0],i[1]))
   pass
   SMW.jav_Close()
   
def btn4():
   ### Set 5GNR Parameters
   SMW = VSG().jav_Open(Entry1.get())  #Create SMW Object
   FSW = VSA().jav_Open(Entry2.get())  #Create FSW Object
   RSVar.Freq        = int(Entry3.get())
   RSVar.SWM_Out     = float(Entry4.get())
   RSVar.NR_Dir      = Enum10.get()
   RSVar.NR_Deploy   = Enum11.get()
   RSVar.NR_ChBW     = int(Enum12.get())
   RSVar.NR_SubSp    = int(Enum13.get())
   RSVar.NR_RB       = int(Entry14.get())
   RSVar.NR_Mod      = Enum15.get()
   NR5G_SetSettings(FSW,SMW,RSVar)
   windowLowerWrite("Setting Written")
   SMW.jav_Close()
   FSW.jav_Close()

def btn5():
   SMW = VSG().jav_Open(Entry1.get())  #Create SMW Object
   FSW = VSA().jav_Open(Entry2.get())  #Create FSW Object

   ### Read 5GNR Parameters ###
   K144Data = NR5G_ReadSettings(FSW,SMW) 
   windowUpperClear()
   windowUpperWrite(" ")
   for i in range(len(K144Data[0])):
      try:
         windowUpperWrite("%s\t%s\t%s"%(K144Data[0][i],K144Data[1][i],K144Data[2][i]))
      except: 
         try:
            windowUpperWrite("%s\t%s\t%s"%(K144Data[0][i],K144Data[1][i],'<not read>'))
         except:
            windowUpperWrite("%s\t%s\t%s"%(K144Data[0][i],'<not read>',K144Data[2][i]))
   SMW.jav_Close()
   FSW.jav_Close()

def dataLoad():
   OutObj = GUIData()
   try:
      try:        #Python3
         f = open(__file__ + ".csv","rt")
      except:     #Python2
         f = open(__file__ + ".csv","rb")         
      data = f.read().split(',')
      OutObj.Entry1 = data[0]
      OutObj.Entry2 = data[1]
      OutObj.Entry3 = data[2]
      OutObj.Entry4 = data[3]
      windowLowerWrite("DataLoad: File")
   except:
      windowLowerWrite("DataLoad: Default")
   return OutObj
                 
def dataSave():
   try: #Python3
      f = open(__file__ + ".csv",'wt', encoding='utf-8')
   except:
      f = open(__file__ + ".csv",'wb')      
   f.write('%s,'%(Entry1.get()))
   f.write('%s,'%(Entry2.get()))
   f.write('%s,'%(Entry3.get()))
   f.write('%s,'%(Entry4.get()))
   f.close()
   windowLowerWrite("DataSave: File Saved")
   
def windowLowerClear():
   posi = lstBotWind.curselection()
   lstBotWind.delete(0.0,END)

def windowLowerWrite(inStr):
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

def windowUpperClear():
   #posi = lstTopWind.curselection()
   lstTopWind.delete(0.0,END)
   
def windowUpperWrite(inStr):
   lstTopWind.insert(END,'\n'+inStr)
   lstTopWind.see(END)
   GUI.update()

def menu_Exit():
   global GUI
   dataSave() 
   GUI.quit()
   GUI.destroy()
   print("Program End")

def menu_Open():
   asdf = tkFileDialog.askopenfilename()
   print(asdf)
   
def menu_Save():
   dataSave()

def menu_TopWindClear():
   windowUpplerClear()

def menu_TopWindLoad_Files():
   lstTopWind.delete(0,END)
   filez = tkFileDialog.askopenfilenames()
   fileList = list(filez)
   for i in fileList:
      lstTopWind.insert(END,i)
   lstTopWind.see(END)

def menu_TopWindLoad_Read():
   lstTopWind.delete(0,END)
   filez = tkFileDialog.askopenfilename()
   windowLowerWrite(filez)
   for i in fileList:
      lstTopWind.insert(END,i)
   lstTopWind.see(END)


########################################################################       
### Main Code
########################################################################
RSVar = copy.copy(dataLoad())
GUI.title(RSVar.Title)                             #GUI Title
#GUI.iconbitmap('RSIcon.ico')
GUI.resizable(0,0)
GUI.config(bg=ClrAppBG)

########################################################################
### Define GUI Widgets
Label1 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt1)
Entry1 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg, insertbackground=ColorCurs)
Entry1.insert(END,RSVar.Entry1)                   #Default Value

Label2 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt2)#Create Label
Entry2 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg, insertbackground=ColorCurs)
Entry2.insert(END,RSVar.Entry2)                   #Default Value

Label3 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt3)#Create Label
Entry3 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg, insertbackground=ColorCurs)
Entry3.insert(END,RSVar.Entry3)                   #Default Value

Label4 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt4)#Create Label
Entry4 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg, insertbackground=ColorCurs)
Entry4.insert(END,RSVar.Entry4)                   #Default Value

Label10 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt10) #Create Label
Entry10 = PullD10
Entry10.config(width=Col1Wid-7, bg=ClrTxtBg, fg=ClrTxtFg)

Label11 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt11)#Create Label
Entry11 = PullD11
Entry11.config(width=Col1Wid-7, bg=ClrTxtBg, fg=ClrTxtFg)

Label12 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt12)#Create Label
Entry12 = PullD12
Entry12.config(width=Col1Wid-7, bg=ClrTxtBg, fg=ClrTxtFg)

Label13 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt13)#Create Label
Entry13 = PullD13
Entry13.config(width=Col1Wid-7, bg=ClrTxtBg, fg=ClrTxtFg)

Label14 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt14)#Create Label
Entry14 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg, insertbackground=ColorCurs)
Entry14.insert(END,RSVar.Entry14)                   #Default Value

Label15 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt15)#Create Label
Entry15 = PullD15
Entry15.config(width=Col1Wid-7, bg=ClrTxtBg, fg=ClrTxtFg)

btnObj1 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt1,command = btn1)
btnObj2 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt2,command = btn2)
btnObj3 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt3,command = btn3)
btnObj4 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt4,command = btn4)
btnObj5 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt5,command = btn5)
btnQuit  = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg="yellow",text="Quit",      command = menu_Exit)

########################################################################
### List Boxes
########################################################################
lstTopWind = Tk.Text(GUI,bg=ClrTxtBg, fg=ClrTxtFg, width=ColxWid, height=26)
srlTopWind = ttk.Scrollbar(GUI, orient=Tk.VERTICAL,command=lstTopWind.yview)  #Create scrollbar
lstTopWind.config(tabs=('5c', '7c', '9c'))  
for item in RSVar.List1:
   lstTopWind.insert(END, item + '\n')
lstTopWind.config(yscrollcommand=srlTopWind.set)                              #Link scroll to lstTopWind

lstBotWind = Tk.Text(GUI, width=BotWindWid, bg=ClrTxtBg, fg=ClrTxtFg, 
                     wrap=Tk.CHAR, height=5)
srlBotWind = ttk.Scrollbar(GUI, orient=Tk.VERTICAL, command=lstBotWind.yview) #Create scrollbar
lstBotWind.config(wrap='none')
lstBotWind.config(yscrollcommand=srlBotWind.set)                              #Link scroll to lstBotWind
lstBotWind.insert(Tk.INSERT,"Output Window\n")
lstBotWind.tag_add("here", "1.0", "1.40")
lstBotWind.tag_config("here", background="yellow", foreground="blue")

########################################################################
### Draw Widgets w/ Grid
########################################################################
Label1.grid(row=0,column=0,sticky=Tk.E)
Label2.grid(row=1,column=0,sticky=Tk.E)
Label3.grid(row=2,column=0,sticky=Tk.E)
Label4.grid(row=3,column=0,sticky=Tk.E)
Label10.grid(row=4,column=0,sticky=Tk.E)
Label11.grid(row=5,column=0,sticky=Tk.E)
Label12.grid(row=6,column=0,sticky=Tk.E)
Label13.grid(row=7,column=0,sticky=Tk.E)
Label14.grid(row=8,column=0,sticky=Tk.E)
Label15.grid(row=9,column=0,sticky=Tk.E)

Entry1.grid(row=0,column=1)
Entry2.grid(row=1,column=1)
Entry3.grid(row=2,column=1)
Entry4.grid(row=3,column=1)
Entry10.grid(row=4,column=1)
Entry11.grid(row=5,column=1)
Entry12.grid(row=6,column=1)
Entry13.grid(row=7,column=1)
Entry14.grid(row=8,column=1)
Entry15.grid(row=9,column=1)

btnObj1.grid(row=btnRow,column=0)
btnObj2.grid(row=btnRow,column=1)
btnObj3.grid(row=btnRow,column=2)
btnObj4.grid(row=btnRow,column=3)
btnObj5.grid(row=btnRow,column=4)
btnQuit.grid(row=btnRow,column=5)

lstTopWind.grid(row=0,column=2,columnspan=4,rowspan=10, sticky=(Tk.E))
srlTopWind.grid(column=maxCol,row=0,rowspan=10,sticky=(Tk.W,Tk.N,Tk.S))
lstBotWind.grid(row=btnRow-1,column=0,columnspan=(maxCol),sticky=Tk.E)
srlBotWind.grid(column=maxCol,row=btnRow-1, sticky=(Tk.W,Tk.N,Tk.S))

########################################################################
# Define menu
########################################################################
if 0:
   menu = Tk.Menu(GUI)                                #create GUI dropdown 
   GUI.config(menu=menu)                              #define GUI's menu

   fileMenu = Tk.Menu(menu)                           #create dropdown menu
   fileMenu.add_command(label="Open",command=menu_Open)
   fileMenu.add_command(label="Save",command=menu_Save)
   fileMenu.add_separator()
   fileMenu.add_command(label="SCPI Load", command=mnu_TopWindLoad_Read)
   fileMenu.add_command(label="SCPI Clear",command=mnu_TopWindClear)
   fileMenu.add_separator()
   fileMenu.add_command(label="Exit",command=menu_Exit)
   menu.add_cascade(label="File",menu=fileMenu)       #add dropdown menu

   editMenu = Tk.Menu(menu)                           #create dropdown menu
   editMenu.add_command(label="Edit",command=menu_Open)
   menu.add_cascade(label="Edit",menu=editMenu)       #add dropdown menu

########################################################################
# Start Program
########################################################################
GUI.mainloop()                      #Display window
