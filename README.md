#Rohde&Schwarz Python SCPI Driver
=====================================================================
Example automation code for general purpose R&S equipment.  Project   
aims to provide a python driver for use in other projects.
 

### Drivers:
* Structure: 
    * pyvisa &rarr; yaVISA.py &rarr; &lt;**instr**&gt;\_Common.py &rarr; 
        * &lt;**instr**&gt;\_&lt;OptionName&gt;\_Kxx.py
        * &lt;**instr**&gt;\_&lt;OptionName&gt;\_Kxx.py
        * &lt;**instr**&gt;\_&lt;OptionName&gt;\_Kxx.py
* yaVISA: pyvisa wrapper
    * yaVISA.VISA_Open()
    * yaVISA.write()
    * yaVISA.logSCPI() to record SCPI commands to file
    * yaVISA.VISA_OPC_Wait(sCmd) for longer time commands
* FSW: Vector Spectrum Analyzer
    * Base for FSW & VSE drivers
    * Possible compatibility: VSE; FPS; FSV;
* SMW: Vector Signal Generator
    * Possible compatibility: SGS; SGT; SMB; SMBV
* VSE: Vector Signal Explorer SW
    * FSW & VSE shares many SCPI commands.
    * Drivers represent VSE commands not in FSW code
    * OFDMVSA K96 code resides here as well
    * Possible compatibility: FSW

##Getting Started
=====================================================================
### Installing
```python
    python -m pip install rssd
```

### Running
* Load example files in &lt;Python&gt;\Lib\site-packages\rssd\examples
* Change IP address to match instrument(s)
* Run
* Examples Include:
    * SMW_LoadArb.py          |Basic SMW commands
    * VSE_ADemod.py           |VSE/FSW Analog FM Demod
    * VSE_Debug.py            |VSE Raw SCPI
    * VSE_OFDM_1CC_K96.py     |VSE Single OFDM Carrier EVM w/ K96
    * VSE_OFDM_MultiCC_K96.py |VSE Multi  OFDM Carrier EVM w/ K96

## Versioning
=====================================================================
We use [Bitbucket](http://www.bitbucket.com/) for versioning. 


### Author
* Martin C Lim - *Initial work* 
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


