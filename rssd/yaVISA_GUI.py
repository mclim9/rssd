from __future__ import division         #int div to float
########################################################################
# Title: Rohde & Schwarz Simple ATE example GUI
########################################################################
# User Input Settings
########################################################################
btnWid = 11
Col0Wid = 10                            #Text Labels
Col1Wid = 14                            #Text Input
ColxWid = 4*(btnWid+4) -4
BotWindWid = Col0Wid+Col1Wid+ColxWid
maxCol = 6
btnRow = 20
ClrTxtBg     = "black"                  #gray30
ClrTxtFg     = "green2"
BtnTxtFg     = "white"
ColorCurs    = "white"
ClrAppBG     = "grey30"

########################################################################
### Code Import
########################################################################
try:        #Python2 naming
    import Tkinter              as      Tk
    import ttk
    import tkFileDialog
except:    #Python3 naming
    import tkinter              as      Tk
    from    tkinter             import  ttk
    import tkinter.filedialog   as      tkFileDialog
END = Tk.END

#Code specific libraries
import  copy
from    datetime  import datetime
from    yaVISA     import jaVisa

########################################################################
### Functions
########################################################################
class GUIData(object):
    def __init__(self):
        self.Title  = "Rohde&Schwarz VISA Utility"
        self.EntTxt1= "Instrument IP"
        self.Entry1 = "127.0.0.1"
        self.EntTxt2= "SCPI String"
        self.Entry2 = "*IDN?"
        self.EntTxt3= "Entry 3"
        self.Entry3 = ""
        self.EntTxt4= "Entry 4"
        self.Entry4 = ""
        self.List1  = ['*IDN?','*OPT?']
        self.BtnTxt1= 'VISA Scan'
        self.BtnTxt2= 'SCPI List'
        self.BtnTxt3= '*IDN?'
        self.BtnTxt4= 'Query'
        self.BtnTxt5= 'Write'

def ArrayInput(stringIn):
    OutputList = []
    InputList = stringIn.split(",")
    for i in InputList:
        i = i.strip()
        OutputList.append(i)
    return OutputList

def btn_Clear():
    # posi = lstBotWind.curselection()
    lstBotWind.delete(0.0,END)

def btn1():
    """Scan VISA"""
    windowLowerWrite("[Resource List]")
    K2 = jaVisa()
    InstrList = K2.jav_reslist()
    for i in InstrList:
        windowLowerWrite("    " + i)
    K2.jav_Close()

def btn2():
    """Send SCPIList in TopWindow"""
    windowLowerWrite("[SCPI LIST]")
    K2 = jaVisa()
    K2.jav_Open(Entry1.get())
    SCPIList = lstTopWind.get("1.0",END).split('\n')
    OutList = K2.jav_scpilist(SCPIList)
    try:
        windowLowerWrite('  Err:' + ''.join(K2.jav_Close()))
    except:
        pass

    for Ostr in OutList:
        windowLowerWrite("  " + Ostr)

def btn3():
    """*IDN Query"""
    windowLowerWrite("--> *IDN?")
    K2 = jaVisa()
    K2.jav_Open(Entry1.get())
    readStr = K2.query("*IDN?")
    windowLowerWrite("<-- " + readStr)
    K2.jav_Close()

def btn4():
    """Query SCPI String"""
    windowLowerWrite("--> " + Entry2.get())
    K2 = jaVisa()
    K2.jav_Open(Entry1.get())
    readStr = K2.query(Entry2.get())
    windowLowerWrite("<-- " + readStr)
    K2.jav_Close()

def btn5():
    """Write SCPI """
    windowLowerWrite("--> " + Entry2.get())
    K2 = jaVisa()
    K2.jav_Open(Entry1.get())
    K2.write(Entry2.get())
    K2.jav_Close()

def dataLoad():
    OutObj = GUIData()
    try:
        try:          #Python3
            f = open(__file__ + ".csv","rt")
        except:      #Python2
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
    # posi = lstBotWind.curselection()
    lstBotWind.delete(0.0,END)

def windowLowerWrite(inStr):
    sDate = datetime.now().strftime("%y%m%d-%H%M%S.%f") #Date String
    try:
        lstBotWind.insert(Tk.INSERT,"%s %s\n"%(sDate[:-3],inStr))   #Text moves down
        # lstBotWind.insert(END,"%s %s\n"%(sDate[:-3],inStr))         #Text moves up
        # lstBotWind.see(END)                                         #Text moves up
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
    # global GUI
    dataSave()
    GUI.quit()
    GUI.destroy()
    print("Program End")

def menu_Open():
    asdf = tkFileDialog.askopenfilename()
    print(asdf)

def menu_Save():
    dataSave()

def mnu_TopWindLoad_Files():
    lstTopWind.delete(0,END)
    filez = tkFileDialog.askopenfilenames()
    for i in list(filez):
        lstTopWind.insert(END,i)
    lstTopWind.see(END)

def mnu_TopWindLoad_Read():
    lstTopWind.delete(0,END)
    filez = tkFileDialog.askopenfilename()
    windowLowerWrite(filez)
    for i in list(filez):
        lstTopWind.insert(END,i)
    lstTopWind.see(END)

def mnu_TopWindClear():
    # posi = lstTopWind.curselection()
    lstTopWind.delete(0.0,END)

def mnu_SaveCond():
    dataSave()

########################################################################
### Main Code
########################################################################
RSVar = copy.copy(dataLoad())
GUI = Tk.Tk()                                                           #Create GUI object
GUI.title(RSVar.Title)                                                  #GUI Title
#GUI.iconbitmap('RSIcon.ico')
GUI.resizable(0,0)
GUI.config(bg=ClrAppBG)

########################################################################
### Define GUI Widgets
Label1 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt1)   #Create Label
Entry1 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg, insertbackground=ColorCurs)
Entry1.insert(END,RSVar.Entry1)                                         #Default Value
Label2 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt2)   #Create Label
Entry2 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg, insertbackground=ColorCurs)
Entry2.insert(END,RSVar.Entry2)                                         #Default Value
Label3 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt3)   #Create Label
Entry3 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg, insertbackground=ColorCurs)
Entry3.insert(END,RSVar.Entry3)                                         #Default Value
Label4 = Tk.Label(GUI,width=Col0Wid, bg=ClrAppBG, text=RSVar.EntTxt4)   #Create Label
Entry4 = Tk.Entry(GUI,width=Col1Wid, bg=ClrTxtBg, fg=ClrTxtFg, insertbackground=ColorCurs)
Entry4.insert(END,RSVar.Entry4)                                         #Default Value
btnObj1 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt1,command = btn1)
btnObj2 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt2,command = btn2)
btnObj3 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt3,command = btn3)
btnObj4 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt4,command = btn4)
btnObj5 = Tk.Button(GUI,width=btnWid,bg=ClrAppBG,fg=BtnTxtFg,text=RSVar.BtnTxt5,command = btn5)
btnQuit = Tk.Button(GUI,width=btnWid,bg='red'   ,fg=BtnTxtFg,text="Quit",       command = menu_Exit)

########################################################################
### List Boxes
########################################################################
lstBotWind = Tk.Text(GUI, width=BotWindWid, bg=ClrTxtBg, fg=ClrTxtFg,\
                            wrap=Tk.CHAR, height=15)
srlBotWind = ttk.Scrollbar(GUI, orient=Tk.VERTICAL, command=lstBotWind.yview)   #Create scrollbar
lstBotWind.config(wrap='none')
lstBotWind.config(yscrollcommand=srlBotWind.set)                                #Link scroll to lstBotWind
lstBotWind.insert(Tk.INSERT,"Output Window\n")
lstBotWind.tag_add("here", "1.0", "1.40")
lstBotWind.tag_config("here", background="yellow", foreground="blue")

lstTopWind = Tk.Text(GUI,bg=ClrTxtBg, fg=ClrTxtFg, width=ColxWid,height=10)
srlTopWind = ttk.Scrollbar(GUI, orient=Tk.VERTICAL,command=lstTopWind.yview)   #Create scrollbar
for item in RSVar.List1:
    lstTopWind.insert(END, item + '\n')
lstTopWind.config(yscrollcommand=srlTopWind.set)                               #Link scroll to lstTopWind

########################################################################
### Draw Widgets w/ Grid
########################################################################
Label1.grid(row=0,column=0,sticky=Tk.E)
Label2.grid(row=1,column=0,sticky=Tk.E)
#Label3.grid(row=2,column=0,sticky=Tk.E)
#Label4.grid(row=3,column=0,sticky=Tk.E)
Entry1.grid(row=0,column=1)
Entry2.grid(row=1,column=1)
#Entry3.grid(row=2,column=1)
#Entry4.grid(row=3,column=1)
btnObj1.grid(row=btnRow,column=0)
btnObj2.grid(row=btnRow,column=1)
btnObj3.grid(row=btnRow,column=2)
btnObj4.grid(row=btnRow,column=3)
btnObj5.grid(row=btnRow,column=4)
btnQuit.grid(row=btnRow,column=5)

lstTopWind.grid(row=0,       column=2,      columnspan=4,rowspan=4, sticky=(Tk.E))
srlTopWind.grid(row=0,       column=maxCol, rowspan=4,              sticky=(Tk.W,Tk.N,Tk.S))
lstBotWind.grid(row=btnRow-1,column=0,      columnspan=(maxCol),    sticky=Tk.E)
srlBotWind.grid(row=btnRow-1,column=maxCol,                         sticky=(Tk.W,Tk.N,Tk.S))

########################################################################
# Define menu
########################################################################
menu = Tk.Menu(GUI)                                                 #create GUI dropdown
GUI.config(menu=menu)                                               #define GUI's menu

fileMenu = Tk.Menu(menu)                                            #create dropdown menu
fileMenu.add_command(label="Open",command=menu_Open)
fileMenu.add_command(label="Save",command=menu_Save)
fileMenu.add_separator()
fileMenu.add_command(label="SCPI Load", command=mnu_TopWindLoad_Read)
fileMenu.add_command(label="SCPI Clear",command=mnu_TopWindClear)
fileMenu.add_separator()
fileMenu.add_command(label="Exit",command=menu_Exit)
menu.add_cascade(label="File",menu=fileMenu)                        #add dropdown menu

editMenu = Tk.Menu(menu)                                            #create dropdown menu
editMenu.add_command(label="Edit",command=menu_Open)
menu.add_cascade(label="Edit",menu=editMenu)                        #add dropdown menu

########################################################################
# Start Program
########################################################################
GUI.mainloop()         #Display window
