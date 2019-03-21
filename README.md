# Rohde&Schwarz Python SCPI Driver

## Project goals:

* Example python drivers
  * FSW, Vector Spectrum Analyzer
  * SMW, Vector Signal Generator
  * NRP, Power Sensor
  * VSE, Vector Signal Explorer
  * VST, Vectro Signal Transciever (FSW/SMW calls)
  * OSP, Switch Driver
  * NRQ, Frequency Selective Power Sensor

* Example code
  * Automated test example
  * Instrument speed/repeatability evaluation
  * Proof of concept/Demo code

* RSSD is in development.  
  - Package APIs **may** change. 
  - We recommend users "freeze/save" package version prior to use.

### Drivers Structure:

* Driver Structure:
  * Common Driver Call: pyvisa &rarr; yaVISA.py &rarr; &lt;**instr**&gt;\_Common.py &rarr;
  * Instrument Options: pyvisa &rarr; yaVISA.py &rarr; &lt;**instr**&gt;\_Common.py &rarr; &lt;**instr**&gt;\_&lt;OptionName&gt;\_Kxx.py
* yaVISA: pyvisa wrapper
  * **yaVISA.jav_Open(sFileName, sLogFile)**: Open VISA link
  * **yaVISA.write(sSCPI)**: Write SCPI command
  * **yaVISA.query(sSCPI)**: Query SCPI command
  * **yaVISA.jav_logscpi()**: Turn on "SCPI to file"
  * **yaVISA.jav_OPC_Wait(sCmd)**: Wait for longer commands.
  * Please see **yaVISA.py** for full list of commands.

### Instrument Drivers:

* FSW: Vector Spectrum Analyzer
  * Developed & Tested with FSW
  * FSW & VSE share many commands.
  * Possible compatibility: VSE; FPS; FSV;
* SMW: Vector Signal Generator
  * Developed & Tested with SMW
  * Possible compatibility: SGS; SGT; SMB; SMBV
* NRP: Power Sensor
  * Developed & Tested with NRPxxS/SN sensors
* VSE: Vector Signal Explorer SW
  * Developed & Tested with VSE
  * Drivers represent VSE commands not in FSW code
  * OFDMVSA K96 code resides here as well
  * Possible compatibility: FSW
* VST: Vector Signal Transceiver
  * Code that calls both SMW & FSW
  * Typically protocol such as: LTE & 5GNR
* OSP: Open Switch and Control Platform
  * Developed & TEsted with OSP120

# Getting Started

### Installing

```python
    python -m pip install rssd
```

### Running

* Load example files in &lt;Python Install Directory&gt;\Lib\site-packages\rssd\examples
* Change IP address to match instrument(s)
* Run

### Example Code:

FileName                | Descriptions                       
------------------------|------------------------------------
FSW_ACLR_Timing         | ACLR in Spectral Mode              
FSW_ACLR_IQ_Timing      | ACLR in IQ Analyzer                
FSW_CCDF                | CCDF in Spectral Mode              
FSW_IQCaptureTime       | IQ Capture time looping Fs         
NRP_BufferedContAvg     | Bufferened NRP measurement         
SMW_LoadArb.py          | Load Arb file into SMW             
OSP_Debug               | Generic OSP example                
VSE_ADemod.py           | VSE/FSW Analog FM Demod            
VSE_Debug.py            | VSE Raw SCPI                       
VSE_OFDM_1CC_K96.py     | VSE Single OFDM Carrier EVM w/ K96 
VSE_OFDM_MultiCC_K96.py | VSE Multi  OFDM Carrier EVM w/ K96 
VST_5GNR_EVMSpeed       | FSW K144 speed tests               
VST_5GNR_K144_Read      | Read SMW/FSW 5G NR Parameters      
VST_Sweep.py            | SMW/FSW Frequency Sweep            

# Project 

* Code Repository: [GitHub](https://github.com/mclim9/rssd) 
* Author: Martin C Lim
* License: This project is licensed under the R&S License for Royalty-Free Products- see the [LICENSE](LICENSE.txt) file for details

## References

Driver     | Description | User Manual | Models 
-----------|-------------|-------------|--------------
SMW | Vector Signal Generator   | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=smw+vector+user+manual&sort=relevance) | [SMW](https://www.rohde-schwarz.com/us/product/smw200a); [SMBV](https://www.rohde-schwarz.com/us/product/smbv100b); [SGT](https://www.rohde-schwarz.com/us/product/sgt100A); [SGS](https://www.rohde-schwarz.com/us/product/sgs100A); [SMA](https://www.rohde-schwarz.com/us/product/sma100b) | 
FSW | Vector Signal Analyzer    | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=FSW+user+manual&sort=relevance) | [FSW](https://www.rohde-schwarz.com/us/product/fsw); [FSVA](https://www.rohde-schwarz.com/us/product/fsva); 
VSE | Vector Analysis Software  | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=vse+base+user+manual) | [VSE](https://www.rohde-schwarz.com/us/product/vse)
CMW | Basestation Emulator      | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=cmw+user+manual) | [CMW500](https://www.rohde-schwarz.com/us/product/CMW500); [CMW100](https://www.rohde-schwarz.com/us/product/CMW100)
NRP | Three Path Power Sensor   | [User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=nrp_s_sn+user+manual) | [NRP](https://www.rohde-schwarz.com/us/product/nrp_s_sn); [NRPM](https://www.rohde-schwarz.com/us/product/nrpm)
NRQ | Freq Selective Pwr Sensor | [User Manual](https://www.rohde-schwarz.com/us/manual/nrq6/) | [NRQ](https://www.rohde-schwarz.com/us/product/nrq6)
OSP | Switch Matrix             | [User Manual](https://www.rohde-schwarz.com/us/manual/osp/) | [OPS1xx](https://www.rohde-schwarz.com/us/product/osp); [OPS2xx](https://www.rohde-schwarz.com/us/product/osp-n)
VNA | Network Analyzer          | [User Manual](https://www.rohde-schwarz.com/us/manual/zva/) | [ZVA](https://www.rohde-schwarz.com/us/product/zva); [ZNA](https://www.rohde-schwarz.com/us/product/zna); [ZNB](https://www.rohde-schwarz.com/us/product/ZNB)

Acknowledgments
=====================================================================

## Acknowledgments
- Thanx to [Nick Lalic](https://pypi.org/project/rohdeschwarz/) for all his help.
- [Markdown reference](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

