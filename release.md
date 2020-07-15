# Release History
=====================================================================

## RSSD 2020.06.3
### Driver
- NRP chg  state 0,'0','Off' for all
- NRQ chg  state 0,'0','Off' for all
- VSG
  - Chg Set_5GNR_BBState from jav_OPC_Wait to jav_Wait
- RST
  - GPRF functions moved to COMMON
  - NR5G_K601 chg from query('MMM').split() to queryFloatArr
    - allows testing

### Examples
- Add SMW_5GNR_HARQ_Setup.py
- Add ZVA_ATSx800_Cal
- Add VSG_Power_Sensor_Sweep
- Add AAA_SCPI_2_File.py

### Test-90%
- NRP Add coverage
- NRQ Add coverage
- ATS1000 Add coverage
- RCT_5GNR add coverage
- RCT_Common add coverage
- VSA_5GNR add coverage
- VSA_Common add coverage
  - Add Mkr tests
  - Add Equalizer tests
  - Add Auto RBW; VBW; tests
- VSA_CommonIQ add coverage
- test_SW_yaVISA_socket test added
- test_SW_yaVISA test added

## RSSD 2020.06.2
- OTA
  - ATS1800 weblink added.
- VSA
  - NF refactored for clarity and testing
  - Common:
    - Del Freq_Step, Get_Params_EVM
    - Add Get_Params_MkrBand
  - LTE: Minor updates.
  - VSA_K70:
    - Chg query to queryFloat
    - Fix VSA_Result_Length
    - Add Get_VSA_Capture_Length
  - WLAN_K91 add A,B,G Get/Set_WLAN_Standard
- VNA
  - Chg dChan input --> self.dChan
- jaVISA
  - Add support for pyvisa py

### Examples
- VSA_BWMarker updated w/ RSI.Timer.

### Test
- NPR & NRQ tests added
- OTA tests added
- OSP tests added
- RCT.5GNR add Phase competnstaion and TransPrecoding tests.
- VSA
  - Common add ACLR tests
  - Add VSA.VSA_K70 tests 
  - Add VSA.WLAN tests
  - Add VSA.Transient_K60 tests
- VSG 
  - Chg javisa.jav_OpenTest()
- VST tests added.
- VNA tests added
- iqData tests added

## RSSD 2020.06.1
- Test
  - Integrated GitHub Action Lint & Test
  - Integrated Coveralls into github Actions
- VNA
  - Refactor from test.
  - Chg " to '
## RSSD 2020.06.0
- 5GNR methods streamlined between VSG; VSA; RCT
- VSA
  - 5GNR
    - Add Set_5GNR_BWP_Ch_DMRS methods
    - Add self.cc check in Set_5GNR_CC_Capture and Set_5GNR_Result_View
    - Add Set_5GNR_FrameCount
- VSG
  - Common
    - Add Get_OS_ methods
    - Add Set_OptimizeNow_ methods
  - 5GNR
    - add self.SubF
    - add self.Get_5GNR_BWP_Ch_PTRS_State check to PTRS methods
    - chg Get_5GNR_FreqRange to return HIGH MIDD LOW
- RCT
  - NR5G_KM601.py
    - Verified against CMP200 w/ RRH
    - add self.scs
    - chg Get_5GNR_Params_EVM
    - del Set_5GNR_Periodicity
    - add Set_5GNR_BWP_Frame_Periodicity 
    - add Set_5GNR_BWP_Frame_SlotConfig
    - add Set_5GNR_BWP_SubSpace
    - add Set_5GNR_EVM_MeasOnExcept
- Examples
  - Add VSA_IQAutolevel.py
  - Add VSA_On flag for VST_NR5G_4CC_Config
  - Created mock classes in rssd.test
- SW Tests
  - test_HW_VSA_xxx
  - test_HW_VSG_xxx
  - Alpha Examples directory test
  - test_HW_RCT_5GNR.py alpha
  - coverage and coveralls integration
  - Add github.ci Action pythonpackage.yml

## RSSD 2020.04.0
- VSA
  - Common alphebetize and cleanup
## RSSD 2020.03.2
- DSO
  - Add DSO_example.py
  - Add DSO.Spectrum_K18.py
  - Add DSO.Common comments
- VSA
  - Chg all SCPI to f-String
  - Chg mssing :CC1: to :CC{self.cc}:

## RSSD 2020.03.0
- VSG
  - Common add System Config Read cmds
  - NR5G_K144
    - Add self.cc; chg methods to use self.cc
    - Chg all string to f-strings
- VSA
  - NR5G_K144
    - Add self.cc; chg methods to use self.cc
  - Common chg from Get_xxxParams to Get_Params_xxx
  - VSA_K70 add 'OQPSK' support.

## RSSD 2020.02.0
- Add Proto VSG.CustomDigMod.py
- VSA
  - Add NR5G_K144 ACLR & SEM measurements
  - Add VSA_5GNR Example
  - Chg Init_xxx methods ability to name ch at creation
  - Add VSA_K70 functions
  - Common
    - add Set/Get_Trace_ methods
    - add Header output to Get_AmpSettings; Get_SweepParams; Get_TraceSettings
    - chg comments
    - add Get_System_Params
    - chg Set_SweepTime to chg to auto if 0
    - add Set_Trace_Mode
- Examples chg FSW_ to VSA_

## RSSD 2019.12.0
- VSA
  - Common
    - Get/Set Ch Name
    - Update Init_mmm w/ name input
    - add Set_ChannelSelect()
  - VSA_K70
    - Add Set_VSA_Mod()
    - Add Get_VSA_Meas_Params()
  - 5GNR fix typos
- VSG
  - Add CustomDigMod.py
  - 5GNR fix typos
- Examples
  - Add VSA_5GNR.py
  - 
## RSSD 2019.11.0

## RSSD 2019.10.0 **Code Break**
- Add 5GNR
  - PTRS settings to FSW/SMW
  - Improved DMRS settings
- Add Proto Drivers
  - PNA (phase noise analyzer)
  - RCT (Radio Comm Tester:CMW; CMP)
- CODE BREAK
  - Instrument drivers in separate directories
  - Chg from Instr_Opt -> Instr.Opt format
  - Chg from FSW_xxx   -> VSA.xxx
  - Chg from SMW_xxx   -> VSG.xxx
  - Chg from 5GNR      -> NR5G

## RSSD 2019.6.0
- SMW_5GNR Set_5GNR_BWP_SubSpace update.
- Add RSI_Memory.py
- Add VSA Harmonics
- Add SMW list mode
- Add RTO_Common.py proto
- Del UnityK144
- Add Examples
  - VSA_NoiseFloor
  - VSA_Harmonics

## RSSD 2019.5.3
  - Add Example links to readme.md

## RSSD 2019.5.2
- Add rssd cmd line script
- Fixed FSW_Common typo in 5.1

## RSSD 2019.5.1
- Administrative
  - README.md: Moved instrument & example tables to top.
  - Version number now date
  - Add .travis.yml
    - Testing FileIO; RSSD Module load; Basic ya_VISA
    - Testing Python 2.7; 3.6; 3.7
- FSW_Common-ACLR/EVM time optimization
  - Add Get_Mkr_BandACLR
  - Add Get_Freq
  - Chg Get_Mkr_Band output to Float
  - Add Set_IQ_ACLR
  - Add Set_IQ_Adv_* methods
  - Chg Set_IQ_SpectrumWindow
  - Add Set_Mkr_BandDelta
  - Add Set_Param_Couple_All
  - Add Set_AutoOpt_FSx_Level

## RSSD 0.1.13
- ALCR
  - Chg methods in WLAN; FSW_Common; FSW_ACLR_Timing;
  - Add to examples/FSW_ACLR_IQ_Timing & FSW_ACLR_Timing
    - Power sweep; sweep modes; Alt; test times added.
- Add yaVISA_VISA(21MB) and yaVISA_socket (0MB)
  - add jav_fileout
  - add EOL character
  - add except in jav_ClrErr
  - add except in jav_IDN
  - add port number to jav_Open
- FSW_Common.py:
  - Chg Alphebetized methods
  - Add Set_AttnAuto()
  - Fix Set_ACLR_NumAdj()
- Add Examples:
  - VST_LTE_EVM.py
  - FSW_ACLR_Methods_Timing.py
- __init__.py imports
- Updated Test cases

## RSSD 0.1.12
- Add FSW/SMW/VST LTE commands
- Chg Example\VST_5GNR_EVM.py
- Add iqdata.py
- Add Pwrcal to VNA_Common.py
- Add WLAN FSW/SMW/VST/Example

## RSSD 0.1.11
- Created VST_5GNR_K144 instrument
  - Updated examples
  - Updated Unity w/ VST_5GNR_K144 Object
- Validate VNA_Common.py
- CCDF added to FSW_Common and example

## RSSD 0.1.10
- Add _init_.py to Unity directory
- Changed repository to github

## RSSD 0.1.9
- Unity_K144.py
- yavisa.py open_xxx methods can turn of IDN print.
- minor changes to FSW_5GNR_K144.py
- Add RB Offset settings
- FSW_SMW_Sweep.py add XML output

## RSSD 0.1.8
- Unity_K144.py added to control FSW & SMW
  - SMW_FSW_5GNR_K144_Set.py and SMW_FSW_5GNR_K144_Get.py Callable
- FSW/SMW-K144:api break
  - Chg methods from _slot_ to _ch_
  - Chg methods from _DMRS_ to _BWP_Ch_DMRS_
  - Methods alphabetized
- Add FSW_ADemod_K7
- VNA
  - Add prototype for future use
- Chg Object creation in examples

## RSSD 0.1.7
- FSW
  - Validate FSW_5GNR_K144.py
  - Add FSW_NoiseFigure_K30.py
  - Add FSW Marker methods include window input.
  - Add FSW_Trigger methods
-SMW
  - Validate FSW_5GNR_K144.py
  - NRP_Common Add trigger methods
- Examples
  - Add SMW_FSW_5GNR_EVMSpeed.py
  - Add FSW_ACLR_Timing.py
  - Add FSW_ACLR_IQ_Timing.py

## RSSD 0.1.6
- Fix Import references to rssd.
- Fix SMW/FSW 5G NR methods.  Added methods.
- Add Test_rssd.py to validate drivers
- Add NRP_Common.py

## RSSD 0.1.5
- Add AAA_Common.py instrument template
- Add FSW/SMW_5GNR_144 read functions
- Add FSW_Transient_K60.py
- Add NRQ_Common.py
- Fix OSP_Common.Get_SW_SPDT
- Chg README.md

## RSSD 0.1.4
- Chg FSW_Common.py Bug fix
- Add test_RSSD.py
- Add test_SMW_Basic.py
- Add OSP_Common.py
- Examples
  - Add SMW_FSW_Sweep.py
  - Add SMB_SMZ_Mixer.py
  - Chg CMW_GPRF_Loopback.py

## RSSD 0.1.3
- Chg yaVISA_GUI.py
- Chg yaVISA.py method names
- Chg __init__ function in class definition
- Add CMW_GPRF.py

## RSSD 0.1.2
## RSSD 0.1.1
## RSSD 0.1
- Initial release
