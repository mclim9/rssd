# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Digital Storage Oscilloscope Spectrum Analysis Methods
### Author : Martin C Lim
### Date   : 2020.03.24
###
###############################################################################
from rssd.DSO.Common import DSO

class DSO(DSO):
    """ Rohde & Schwarz Digital Storage Oscilloscope Object """
    def __init__(self):
        super(DSO, self).__init__()

    #####################################################################
    ### DSO Get Functions
    #####################################################################
    def Get_SA_AcqTime(self):
        """ Seconds """
        rdStr = self.query(':TIM:RANG?')
        return rdStr

    def Get_SA_Resolution_BW(self,Ch):
        """  1 to 8 """
        rdStr = self.query(f':CALC:MATH{Ch}:FFT:BAND:RES:ADJ?')
        return rdStr

    def Get_SA_Frame_Coverage(self,Ch):
        """  1 to 8 """
        rdStr = self.query(f':CALC:MATH{Ch}:FFT:FRAM:COV?')
        return rdStr

   # def Get_SA_Timebase_Acquisition_Time(self,Ch):
   #     """  1 to 8 """
   #     rdStr = self.query(f':CALC:MATH{Ch}:FFT:FRAM:COV?')
   #     return rdStr

    #####################################################################
    ### DSO Init Functions
    #####################################################################
    def Init_SpecAn(self):
        #Configure instrument measurment
        pass

    #####################################################################
    ### DSO Set FFT Functions
    #####################################################################
    def Set_SA_AcqTime(self, sec):
        """ Seconds """
        self.write(f':TIM:RANG {sec}')

    def Set_SA_RBW_Auto(self,state,Ch):
        """  ON OFF, Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:BAND:RES:AUTO {state}')

    def Set_SA_RBW_Ratio(self,ratio,Ch):
        """  1 TO 1000 , Ch 1 TO 4"""
        self.write(f':CALC:MATH{Ch}:FFT:BAND:RES:RAT {ratio}')

    def Set_SA_RBW_Value(self,Hz,Ch):
        """ 0.01 to 160e6 Hz , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:BAND:RES:VAL {Hz}')

    def Set_SA_Windowing_Type(self, filtr, Ch):
        """ RECT HAMM HANN BLACKharris GAUSian FLATTOP2
         KAISerbessel  , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:WIND:TYPE {filtr}')

    def Set_SA_Arithmetics(self, func, Ch):
        """ OFF ENV AVER RMS MINH MAXH , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:FRAM:ARIT {func}')

    def Set_SA_Frame_Max(self,count, Ch):
        """ 1 to 10000 , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:FRAM:MAXC {count}')
        
    def Set_SA_Frame_Overlap(self,factor, Ch):
        """ 0 TO 90 , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:FRAM:OFAC {factor}')

    def Set_SA_Gate_Start_Absolute(self,time, Ch):
        """ -100E+24 to 100e+24 , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:GATE:ABS:STAR {time}')

    def Set_SA_Gate_Stop_Absolute(self,time, Ch):
        """ -100E+24 to 100e+24 , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:GATE:ABS:STOP {time}')

    def Set_SA_Gate_Start_Relative(self,percent, Ch):
        """ 0 to 100 , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:GATE:REL:STAR {percent}')

    def Set_SA_Gate_Stop_Relative(self,percent, Ch):
        """ 0 to 100 , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:GATE:REL:STOP {percent}')
    
    def Set_SA_Gate_Mode(self,mode, Ch):
        """ ABS REL , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:GATE:ABS:STAR {mode}')  

    def Set_SA_Gate_State(self,state, Ch):
        """ ON OFF , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:GATE:STAT {state}') 

    def Set_SA_Reference_Level(self,dB,Ch):
        """ -1E15 to 1E15 dB , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:MAGN:LEV {dB}')

    #def Set_SA_Vertical_Range(self,dB, Ch):#NOT WORKING
    #    """ 1 to 500 dB , Ch 1 TO 4 """
    #    self.write(f':CALC:MATH{Ch}:FFT:MAGN:RANGE {dB}') 

    def Set_SA_Math(self,state,Ch):
        """  ON OFF , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:STAT {state}')

    def Set_SA_Center_Freq(self,Hz, Ch):
        """ 0 to 2E12 Hz, Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:CFR {Hz}')

    def Set_SA_Full_Span(self,Ch):
        """ 0 to 2E12 Hz , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:FULL')

    def Set_SA_Span(self,Hz,Ch):
        """ 1 to 4E12 Hz , Ch 1 TO 4 """
        self.write(f':CALC:MATH{Ch}:FFT:SPAN {Hz}')

    #def Set_SA_Vertical_Scale(self,unit,Ch):#CNOT WORKING
    #    """ LIN DBM DB DBUV DBV , Ch 1 TO 4 """
    #    self.write(f':CALC:MATH{Ch}:FFT:MAGN:SCAL {unit}') 

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    DSO_Inst = DSO().jav_Open("192.168.1.100")
    DSO_Inst.jav_IDN()
    DSO_Inst.jav_ClrErr()
