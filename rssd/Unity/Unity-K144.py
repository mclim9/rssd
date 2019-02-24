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
EntTxtFg    = "green2"
EntTxtBg    = "black"                              #gray30
LblTxtFg    = 'white'
BtnTxtFg    = "white"
ColorCurs   = "white"
ClrAppBg    = "grey30"

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
from rssd.yaVISA              import jaVisa        #pylint:disable=E0611,E0401
from rssd.VST_5GNR_K144       import VST           #pylint:disable=E0611,E0401

########################################################################
### Functions
########################################################################
class GUIData(object):
   def __init__(self):
      self.Title     = "Rohde&Schwarz FSW SMW 5GNR Utility"
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
      self.EntTxt11  = "Freq Band"
      self.Entry11   = "HIGH"
      self.EntTxt12  = "Ch BW,MHz"
      self.Entry12   = "100"
      self.EntTxt13  = "SubCarrier,kHz"
      self.Entry13   = "60"
      self.EntTxt14  = "RB"
      self.Entry14   = "132"
      self.EntTxt15  = "RB Offset"
      self.Entry15   = "0"
      self.EntTxt16  = "Modulation"
      self.Entry16   = "QPSK"
      self.List1     = ['- Simplified 5GNR Demo utility',
                        '- Utility does not validate settings against 3GPP 5G',
                        '- Click *IDN? to validate IP Addresses',
                        '- Frequency & SMW Power labels are clickable',
                        '']
      self.BtnTxt1   = '*IDN?'
      self.BtnTxt2   = 'Max RB'
      self.BtnTxt3   = 'Get EVM'
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
Enum16 = Tk.StringVar(GUI)
Enum16.set("QPSK") # default value

Entry10 = Tk.OptionMenu(GUI, Enum10, "UL", "DL")
Entry11 = Tk.OptionMenu(GUI, Enum11, "LOW", "MIDD", "HIGH")
Entry12 = Tk.OptionMenu(GUI, Enum12, "20","50","100","200","400")
Entry13 = Tk.OptionMenu(GUI, Enum13, "15", "30", "60", "120")
Entry16 = Tk.OptionMenu(GUI, Enum16, "QPSK", "QAM16", "QAM64", "QAM256")

def ArrayInput(stringIn):
   OutputList = []
   InputList = stringIn.split(",")
   for i in InputList:
      i = i.strip()
      OutputList.append(i)
   return OutputList

def btn1():
   ### *IDN Query ###
   NR5G = VST().jav_Open(Entry1.get(),Entry2.get())
   windowLowerWrite(NR5G.SMW.query('*IDN?'))
   windowLowerWrite(NR5G.FSW.query('*IDN?'))
   NR5G.jav_Close()
   
def btn2():
   ### Get Max RB ###
   windowUpperWrite('--------------------------   --------------------------')
   windowUpperWrite('|u[<6GHz ]010 020 050 100|   |u[>6GHz ]050 100 200 400|')
   windowUpperWrite('|-+------+---+---+---+---|   |-+------+---+---+---+---|')
   windowUpperWrite('|0 015kHz|052 106 270 N/A|   |0 015kHz|N/A N/A N/A N/A|')
   windowUpperWrite('|1 030kHz|024 051 133 273|   |1 030kHz|N/A N/A N/A N/A|')
   windowUpperWrite('|2 060kHz|011 024 065 135|   |2 060kHz|066 132 264 N/A|')
   windowUpperWrite('|3 120kHz|N/A N/A N/A N/A|   |3 120kHz|032 066 132 264|')
   windowUpperWrite('--------------------------   --------------------------')
   windowUpperWrite(' ')

   NR5G = VST().jav_Open(Entry1.get(),Entry2.get())
   data = NR5G.SMW.Get_5GNR_RBMax()
   windowUpperWrite("=== Max RB ===")
   windowUpperWrite("Mode: %s %sMHz"%(NR5G.SMW.Get_5GNR_FreqRange(),NR5G.SMW.Get_5GNR_ChannelBW()))
   for i in data:
      windowUpperWrite("SubC:%d  RB Max:%d"%(i[0],i[1]))
   NR5G.jav_Close()

def btn3():
   ### Get EVM ###
   NR5G = VST().jav_Open(Entry1.get(),Entry2.get())
   NR5G.FSW.Set_InitImm()
   windowUpperWrite('EVM:' + str(NR5G.FSW.Get_5GNR_EVM()))
   NR5G.FSW.jav_Close()
   
def btn4():
   ### Set 5GNR Parameters
   NR5G = VST().jav_Open(Entry1.get(),Entry2.get())
   
   ### Read values from GUI
   NR5G.Freq        = int(Entry3.get())
   NR5G.SWM_Out     = float(Entry4.get())
   NR5G.NR_Dir      = Enum10.get()
   NR5G.NR_Deploy   = Enum11.get()
   NR5G.NR_ChBW     = int(Enum12.get())
   NR5G.NR_SubSp    = int(Enum13.get())
   NR5G.NR_RB       = int(Entry14.get())
   NR5G.NR_RBO      = int(Entry15.get())
   NR5G.NR_Mod      = Enum16.get()
   
   ### Do some work
   windowLowerWrite("SMW Creating Waveform.")
   NR5G.Set_5GNR_All()
   windowLowerWrite(NR5G.FSW.jav_ClrErr())
   windowLowerWrite(NR5G.SMW.jav_ClrErr())
   windowLowerWrite("SMW/FSW Setting Written")
   NR5G.jav_Close()

def btn5():
   NR5G = VST().jav_Open(Entry1.get(),Entry2.get())

   ### Read 5GNR Parameters ###
   K144Data = NR5G.Get_5GNR_All() 
   #windowUpperClear()
   windowUpperWrite(" ")
   for i in range(len(K144Data[0])):
      try:
         windowUpperWrite("%s\t%s\t%s"%(K144Data[0][i],K144Data[1][i],K144Data[2][i]))
      except: 
         try:
            windowUpperWrite("%s\t%s\t%s"%(K144Data[0][i],K144Data[1][i],'<notRead>'))
         except:
            windowUpperWrite("%s\t%s\t%s"%(K144Data[0][i],'<notRead>',K144Data[2][i]))
   NR5G.jav_Close()

def click3(tkEvent):
   #print(tkEvent)
   freq = int(Entry3.get())
   NR5G = VST().jav_Open(Entry1.get(),Entry2.get())
   NR5G.SMW.Set_Freq(freq)
   NR5G.FSW.Set_Freq(freq)
   NR5G.jav_Close()
   windowLowerWrite('SMW/FSW Freq: %d Hz'%freq)
   
def click4(tkEvent):
   #print(tkEvent)
   NR5G = VST().jav_Open(Entry1.get(),Entry2.get())
   NR5G.SMW.Set_RFPwr(int(Entry4.get()))
   NR5G.jav_Close()
   windowLowerWrite('SMW RMS Pwr : %d dBm'%int(Entry4.get()))

def click14(tkEvent):
   #print(tkEvent)
   if 0:
      NR5G = VST().jav_Open(Entry1.get(),Entry2.get())
      NR_RB  = int(Entry14.get())
      NR_Dir = Enum10.get()
      if 0:
         NR5G.SMW.Set_5GNR_Direction(NR_Dir)
         NR5G.SMW.Set_5GNR_BWP_ResBlock(NR_RB)
         NR5G.SMW.Set_5GNR_BWP_Ch_ResBlock(NR_RB)
         NR5G.FSW.Set_5GNR_Direction(NR_Dir)
         NR5G.FSW.Set_5GNR_BWP_ResBlock(NR_RB)
         NR5G.FSW.Set_5GNR_BWP_Ch_ResBlock(NR_RB)
      NR5G.jav_Close()
   windowLowerWrite('FSW:Signal Description-->RadioFrame-->BWP Config-->RB')
   windowLowerWrite('FSW:Signal Description-->RadioFrame-->PxSCH Config-->RB')
   windowLowerWrite('SMW:User/BWP-->UL BWP-->RB')
   windowLowerWrite('SMW:Scheduling-->PxSCH-->RB')
   
def click15(tkEvent):
   windowLowerWrite('FSW:Signal Description-->RadioFrame-->BWP Config-->RB Offset')
   windowLowerWrite('SMW:User/BWP-->UL BWP-->RB Offset')
   pass
   
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
   
def windowLowerClear(tk=1):
   #posi = lstBotWind.curselection()
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

def windowUpperClear(tk=1):
   #posi = lstTopWind.curselection()
   lstTopWind.delete(0.0,END)
   
def windowUpperWrite(inStr):
   lstTopWind.insert(END,inStr+'\n')
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
   windowUpperClear()

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
   for i in filez:
      lstTopWind.insert(END,i)
   lstTopWind.see(END)

########################################################################       
### Main Code
########################################################################
RSVar = copy.copy(dataLoad())
GUI.title(RSVar.Title)                             #GUI Title
try:
   #GUI.tk.call('wm', 'iconphoto', GUI._w, Tk.PhotoImage(file='Unity.gif'))
   GUI.resizable(0,0)
   GUI.config(bg=ClrAppBg)
   #Tk.Font(family="Helvetica", size=10, weight=Tk.font.BOLD, slant=Tk.font.ITALIC)
   GUI.iconbitmap('Unity.ico')
except:
   pass
########################################################################
### Define GUI Widgets
Label1 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt1)
Entry1 = Tk.Entry(GUI,width=Col1Wid, bg=EntTxtBg, fg=EntTxtFg, insertbackground=ColorCurs)
Entry1.insert(END,RSVar.Entry1)                   #Default Value

Label2 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt2)#Create Label
Entry2 = Tk.Entry(GUI,width=Col1Wid, bg=EntTxtBg, fg=EntTxtFg, insertbackground=ColorCurs)
Entry2.insert(END,RSVar.Entry2)                   #Default Value

Label3 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt3)#Create Label
Label3.bind("<Button-1>",click3)
Entry3 = Tk.Entry(GUI,width=Col1Wid, bg=EntTxtBg, fg=EntTxtFg, insertbackground=ColorCurs)
Entry3.insert(END,RSVar.Entry3)                   #Default Value

Label4 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt4)#Create Label
Label4.bind("<Button-1>",click4)
Entry4 = Tk.Entry(GUI,width=Col1Wid, bg=EntTxtBg, fg=EntTxtFg, insertbackground=ColorCurs)
Entry4.insert(END,RSVar.Entry4)                   #Default Value

Label10 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt10) #Create Label
Entry10.config(width=Col1Wid-7, bg=EntTxtBg, fg=EntTxtFg)

Label11 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt11)#Create Label
Entry11.config(width=Col1Wid-7, bg=EntTxtBg, fg=EntTxtFg)

Label12 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt12)#Create Label
Entry12.config(width=Col1Wid-7, bg=EntTxtBg, fg=EntTxtFg)

Label13 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt13)#Create Label
Entry13.config(width=Col1Wid-7, bg=EntTxtBg, fg=EntTxtFg)

Label14 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt14)#Create Label
Label14.bind("<Button-1>",click14)
Entry14 = Tk.Entry(GUI,width=Col1Wid, bg=EntTxtBg, fg=EntTxtFg, insertbackground=ColorCurs)
Entry14.insert(END,RSVar.Entry14)                   #Default Value

Label15 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt15)#Create Label
Label15.bind("<Button-1>",click15)
Entry15 = Tk.Entry(GUI,width=Col1Wid, bg=EntTxtBg, fg=EntTxtFg, insertbackground=ColorCurs)
Entry15.insert(END,RSVar.Entry15)                   #Default Value

Label16 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBg, fg=LblTxtFg, text=RSVar.EntTxt16)#Create Label
Entry16.config(width=Col1Wid-7, bg=EntTxtBg, fg=EntTxtFg)

btnObj1 = Tk.Button(GUI,width=btnWid,bg=ClrAppBg,fg=BtnTxtFg,text=RSVar.BtnTxt1,command = btn1)
btnObj2 = Tk.Button(GUI,width=btnWid,bg=ClrAppBg,fg=BtnTxtFg,text=RSVar.BtnTxt2,command = btn2)
btnObj3 = Tk.Button(GUI,width=btnWid,bg=ClrAppBg,fg=BtnTxtFg,text=RSVar.BtnTxt3,command = btn3)
btnObj4 = Tk.Button(GUI,width=btnWid,bg=ClrAppBg,fg=BtnTxtFg,text=RSVar.BtnTxt4,command = btn4)
btnObj5 = Tk.Button(GUI,width=btnWid,bg=ClrAppBg,fg=BtnTxtFg,text=RSVar.BtnTxt5,command = btn5)
btnQuit = Tk.Button(GUI,width=btnWid,bg='red2',fg=BtnTxtFg,text="Quit",         command = menu_Exit)

########################################################################
### List Boxes
########################################################################
lstTopWind = Tk.Text(GUI,bg=EntTxtBg, fg=EntTxtFg, width=ColxWid, height=26)
lstTopWind.bind("<Button-3>",windowUpperClear)
srlTopWind = ttk.Scrollbar(GUI, orient=Tk.VERTICAL,command=lstTopWind.yview)  #Create scrollbar
lstTopWind.config(font='Courier 10 bold')
lstTopWind.config(tabs=('5c', '7c', '9c'))
if 1: ### Default text
   lstTopWind.insert(Tk.INSERT,"===Please Click Buttons Below===\n")
   lstTopWind.tag_add("here", "1.0", "1.40")
   lstTopWind.tag_config("here", background="green2", foreground="black")
for item in RSVar.List1:
   lstTopWind.insert(END, item + '\n')
lstTopWind.config(yscrollcommand=srlTopWind.set)                              #Link scroll to lstTopWind

lstBotWind = Tk.Text(GUI, width=BotWindWid, bg=EntTxtBg, fg=EntTxtFg, 
                     wrap=Tk.CHAR, height=5)
srlBotWind = ttk.Scrollbar(GUI, orient=Tk.VERTICAL, command=lstBotWind.yview) #Create scrollbar
lstBotWind.config(wrap='none')
lstBotWind.config(yscrollcommand=srlBotWind.set)                              #Link scroll to lstBotWind
#lstBotWind.config(font='Courier 12 bold')
if 1: ### Default text
   lstBotWind.insert(Tk.INSERT,"Output Window\n")
   lstBotWind.tag_add("here", "1.0", "1.40")
   lstBotWind.tag_config("here", background="green2", foreground="black")

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
Label16.grid(row=10,column=0,sticky=Tk.E)

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
Entry16.grid(row=10,column=1)

btnObj1.grid(row=btnRow,column=0)
btnObj2.grid(row=btnRow,column=1)
btnObj3.grid(row=btnRow,column=2)
btnObj4.grid(row=btnRow,column=3)
btnObj5.grid(row=btnRow,column=4)
btnQuit.grid(row=btnRow,column=5)

lstTopWind.grid(row=0,column=2,columnspan=4,rowspan=11, sticky=(Tk.E))
srlTopWind.grid(column=maxCol,row=0,rowspan=11,sticky=(Tk.W,Tk.N,Tk.S))
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
   fileMenu.add_command(label="SCPI Load", command=menu_TopWindLoad_Read)
   fileMenu.add_command(label="SCPI Clear",command=menu_TopWindClear)
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
