#Rohde&Schwarz Python Code Examples
---
Example automation code for general purpose R&S equipment.  

### Drivers:
* Structure: pyvisa --> yaVISA --> [instr]_Common --> [instr]_Name_Kxx
* FSW: Vector Spectrum Analyzer
    * Base for FSW & VSE drivers
    * Possible compatibility: VSE; FPS; FSV;
* SMW: Vector Signal Generator
    * Possible compatibility: SGS; SGT; SMB; SMBV
* VSE: Vector Signal Explorer SW
    * FSW & VSE shares many SCPI commands.
    * Drivers represent VSE commands not in FSW code.
    * Possible compatibility: FSW

##Getting Started

### Prerequisites
```python
python -m pip install pyvisa
```

### Installing
* Install prerequisites
* Unzip code into desired directory

### Running
* Load example files in top directory
* Change IP address to match instrument(s)
* Run
* Examples Include:
    * Socket_Example.py		:Socket connection w/o VISA
    * VSE_ADemod.py			:VSE/FSW Analog FM Demod
    * VSE_Debug.py          :VSE Raw SCPI
    * VSE_MultiCC_K96.py    :VSE Multi component carrier EVM w/ K96

## _Versioning_
We use [Bitbucket](http://www.bitbucket.com/) for versioning.

### Authors
* Martin C Lim - *Initial work* 
* Others welcome.  :-D

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Thanx to Nick Lalic for all his help.
* [Markdown reference](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)


