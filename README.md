Rohde&Schwarz Python SCPI Driver
=====================================================================

##Project goals:
* Example general purpose python driver
    * Vector Spectrum Analyzer, VSA
    * Vector Signal Generator, VSG
    * Vector Signal Explorer, VSE
    * Power Meter, PM
* Example code 
    * Automated test example
    * Instrument speed/repeatability evaluation
    * Proof of concept
    * Demo Code
* The package is in development.  Package API may change at any time. We recommend users "freeze" package version for your project use.

### Drivers:
* Structure: 
    * pyvisa &rarr; yaVISA.py &rarr; &lt;**instr**&gt;\_Common.py &rarr; 
        * &lt;**instr**&gt;\_&lt;OptionName&gt;\_Kxx.py
        * &lt;**instr**&gt;\_&lt;OptionName&gt;\_Kxx.py
        * &lt;**instr**&gt;\_&lt;OptionName&gt;\_Kxx.py
* yaVISA: pyvisa wrapper
    * yaVISA.jav_Open(sFileName, sLogFile): Open VISA link
    * yaVISA.write(sSCPI): Write SCPI command
    * yaVISA.query(sSCPI): Query SCPI command
    * yaVISA.jav_logscpi(): Turn on "SCPI to file"
    * yaVISA.jav_OPC_Wait(sCmd): Wait for longer commands.
    * Please see code for full list of commands.
* FSW: Vector Spectrum Analyzer
    * Developed & Tested with FSW
    * FSW & VSE share many commands.
    * Possible compatibility: VSE; FPS; FSV;
* SMW: Vector Signal Generator
    * Developed & Tested with SMW
    * Possible compatibility: SGS; SGT; SMB; SMBV
* VSE: Vector Signal Explorer SW
    * Developed & Tested with VSE
    * Drivers represent VSE commands not in FSW code
    * OFDMVSA K96 code resides here as well
    * Possible compatibility: FSW

Getting Started
=====================================================================

### Installing
```python
    python -m pip install rssd
```

### Running
* Load example files in Python\Lib\site-packages\rssd\examples
* Change IP address to match instrument(s)
* Run
* Examples Include:
    * SMW_FSW_5GNR_K144_Read  |Read SMW/FSW 5G NR Parameters
    * SMW_FSW_Sweep.py        |SMW/FSW Frequency Sweep
    * SMW_LoadArb.py          |Basic SMW commands
    * VSE_ADemod.py           |VSE/FSW Analog FM Demod
    * VSE_Debug.py            |VSE Raw SCPI
    * VSE_OFDM_1CC_K96.py     |VSE Single OFDM Carrier EVM w/ K96
    * VSE_OFDM_MultiCC_K96.py |VSE Multi  OFDM Carrier EVM w/ K96

## Versioning
=====================================================================
We use [Bitbucket](http://www.bitbucket.com/) for versioning. 

### Author
* Martin C Lim 
* Others welcome.  :-D

## License
This project is licensed under the R&S License for Royalty-Free Products- see the [LICENSE](LICENSE.txt) file for details

## References
* [SMW User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=smw+vector+user+manual&sort=relevance) https://www.rohde-schwarz.com/us/manual/smw200a/
* [FSW User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=FSW+user+manual&sort=relevance) https://www.rohde-schwarz.com/us/manual/fsw/
* [VSE User Manual](https://www.rohde-schwarz.com/us/search_63238.html?term=vse+base+user+manual) https://www.rohde-schwarz.com/us/manual/vse/

## Acknowledgments
=====================================================================

* Thanx to Nick Lalic for all his help.
* [Markdown reference](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)


