########################################################################
# Title: Rohde & Schwarz Automation Starter
# Description:
#
########################################################################
# User Input Settings
########################################################################

########################################################################
### Code Import
########################################################################
from datetime                      import datetime
try:        #Python2 naming
    import Tkinter              as     Tk
    import ttk
    import tkFileDialog
    import tkSimpleDialog
except:    #Python3 naming
    import tkinter              as      Tk
    from    tkinter             import  ttk
    import tkinter.filedialog   as      tkFileDialog
    import tkinter.simpledialog as      tkSimpleDialog

END = Tk.END
GUI = Tk.Tk()                                                  #Create GUI object

########################################################################
### Class
########################################################################
class rssdGUI(Tk):
    def __init__(self):
        super(rssdGUI, self).__init__()
        self.btnWid = 11
        self.Col0Wid = 15                                                    #Text Labels
        self.Col1Wid = 15                                                    #Text Input
        self.ColxWid = 3*(btnWid+4) -4
        self.BotWindWid = Col0Wid+Col1Wid+ColxWid
        self.maxCol = 6
        self.btnRow = 20
        self.EntTxtFg     = "green2"
        self.EntTxtBg     = "black"                                        #gray30
        self.LblTxtFg     = 'white'
        self.BtnTxtFg     = "white"
        self.ColorCurs    = "white"
        self.ClrAppBg     = "grey30"

    def method1(self):
        pass


if __name__ == "__main__":
    ### this won't be run when imported
    instGUI = rssdGUI()
    instGUI.mainloop()