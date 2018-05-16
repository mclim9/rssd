#Rohde&Schwarz Python SCPI Driver & Examples
---
Example automation code for general purpose R&S equipment.  Project   
also aims to provide a functional python driver for use in other projects.
 

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
---
### Prerequisites
```python
    python -m pip install pyvisa
```

### Installing
* Install prerequisites
* Unzip code into desired directory

### Running
* Load example files in &lt;Python27&gt;\Lib\site-packages\rssd\examples
* Change IP address to match instrument(s)
* Run
* Examples Include:
    * Socket_Example.py    :Socket connection w/o VISA
    * VSE_ADemod.py        :VSE/FSW Analog FM Demod
    * VSE_Debug.py         :VSE Raw SCPI
    * VSE_MultiCC_K96.py   :VSE Multi component carrier EVM w/ K96

## Versioning
---
We use [Bitbucket](http://www.bitbucket.com/) for versioning.

### Authors
* Martin C Lim - *Initial work* 
* Others welcome.  :-D

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details

## Acknowledgments
---
* Thanx to Nick Lalic for all his help.
* [Markdown reference](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)


