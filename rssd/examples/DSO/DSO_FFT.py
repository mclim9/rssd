"""Digital Storage Oscilloscope FFT Example"""
#pylint: disable=E0611,E0401
################################################################################
### User Entry
################################################################################
RTO_IP      = '192.168.1.33'

################################################################################
### Code Overhead
################################################################################
from rssd.FileIO            import FileIO
from rssd.DSO.Spectrum_K18  import DSO

OFile   = FileIO().makeFile(__file__)           # Open Log file
RTO     = DSO().jav_Open(RTO_IP, OFile)         # Create RTO object & log IDN

################################################################################
### Code Start
################################################################################
rdStr = RTO.query('*IDN?')
RTO.Set_TimeScale(10e-8)
rdStr = RTO.Get_TimeScale()
RTO.Set_TimeScale(1e-8)
rdStr = RTO.Get_TimeScale()
OFile.write(rdStr)
#RTO.Set_System_Preset()
RTO.Set_ChCoupling("AC",1)
RTO.Set_SA_Math("ON",4)
RTO.Set_SA_RBW_Auto("ON",4)
RTO.Set_SA_RBW_Ratio(30,4)
RTO.Set_SA_RBW_Value(40e+3,4)
RTO.Set_SA_Center_Freq(200e+6,4)
RTO.Set_SA_Reference_Level(10,4)
RTO.Set_SA_Full_Span(4)
RTO.Set_SA_Gate_Start_Relative(25,4)
RTO.Set_SA_Gate_Stop_Relative(75,4)
RTO.Set_SA_Gate_Mode("ABS",4)
RTO.Set_SA_Gate_State("ON",4)
RTO.Set_Cursor_All_Off(1)
RTO.Set_Cursor_Source("M4",1)
RTO.Set_Cursor_State("ON",1)
RTO.Set_Cursor_Style("RHOM",1)
RTO.Set_Cursor_Max_Peak(1)
RTO.Set_Cursor_Source("C1W1",2)
RTO.Set_Cursor_State("ON",2)
