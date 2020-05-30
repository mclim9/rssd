# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 22:01:25 2019

@author: RAMIAN

Description:
# Python code to convert from one IQ format to another.
  - Supported formats: iq.tar; wv; iqw

# Functions
  - self.iqData: Complex IQ Data
  - self.read<format>
    - Reads data into self.iqData
    - Sets self.fSamplingRate
    - Sets self.NumberOfSamples
    self.write<format>  Writes self.iqData into <format>
"""

import os
import re
import math
import time
# import array                            # dataConvert
import struct
from datetime import datetime           # writeXml, writeWv
import tarfile                          # readIqTar, writeIqTar
import xml.etree.ElementTree as ET      # readIqTar

class IQ(object):
    """ Util IQ Converting Object """
    def __init__(self):
        self.iqData = [complex(1,1)]                #Complex IQ Data
        self.iiqqList = []
        self.iqiqList = []
        self.NumberOfSamples = 0
        self.fSamplingRate = 0

    def __iqiq2complex__(self, iqiq):
        """iqiq list --> complex list, self.iqData """
        if len(iqiq) % 2 > 0:
            print("Expecting IQIQIQ order, input vector has odd number of samples!")
            return
        self.NumberOfSamples = len(iqiq) // 2
        self.iqData = [ complex(iqiq[2*n], iqiq[2*n+1]) for n in range(self.NumberOfSamples)]

    def __iiqq2complex__(self, iiqq):
        """Returns a complex list of I/Q samples from a single list containing IIIQQQ values"""
        if len(iiqq) % 2 > 0:
            print("Expecting IIIQQQ order, input vector has odd number of samples!")
            return
        self.NumberOfSamples = len(iiqq) // 2
        self.iqData = [ complex(iiqq[n], iiqq[n+self.NumberOfSamples]) for n in range(self.NumberOfSamples)]

    def __complex2iqiq__(self):
        """Returns a list of I/Q samples from a complex list.
        iqiqlist = __complex2iqiq__(complexList)"""
        f= lambda iq,i: iq.real if i==0 else iq.imag
        self.iqiqList = [ f(iq,i) for iq in self.iqData for i in range(2)]

        return self.iqiqList

    # def __complex2iiqq__(self):
    #     """Returns a list of I/Q samples from a complex list.
    #     iiqqList = __complex2iiqq__(complexList)"""
    #     self.iiqqList = [ iq.real for iq in self.iqData]
    #     self.iiqqList.append([ iq.imag for iq in self.iqData])
    #     return self.iiqqList

    def writeIqw(self, FileName):               # Verified 2020.0115
        """writes an IQW file (file of binary floats).
        self.iqData can be a list of complex or list of floats.
        Note: IIIQQQ is a deprecated format, don't use it for new files.
        writtenSamples = writeIqw(iqList, "MyFile.wv")"""

        #check if self.iqData is complex
        if isinstance(self.iqData[0], complex):
            self.__complex2iqiq__()
        self.NumberOfSamples = len(self.iqiqList) // 2
        try:
            file = open(FileName, "wb")
            file.write(struct.pack("f"*len(self.iqiqList),*self.iqiqList))
            file.close()
        except:
            print("File (" + FileName +") write error!" )
            return 0
        return self.NumberOfSamples

    def readIqw(self, FileName, iqiq = True):                                  # Verified 2020.0115
        """Reads an IQW (iiqq or iqiq) file--> self.__iXXq2complex__ --> self.iqData
         - If iqiq is True, samples are read pairwise (IQIQIQ)
         - else, samples are read, i first then q (IIIQQQ)
        Note: IIIQQQ is a deprecated format, don't use it for new files. """

        print("*.IQW file does not have sampling rate.  Please add to output")
        BytesPerValue = 4
        try:
            file = open(FileName, "rb")
            data = file.read()
            file.close()
        except:
            print("File open error ("+ FileName+")!")

        ReadSamples = len(data) // BytesPerValue
        data = list(struct.unpack("f"*ReadSamples, data))
        if iqiq:
            self.__iqiq2complex__(data)
        else:
            self.__iiqq2complex__(data)

    def writeWv(self, FileName):                # Verified 2020.0115
        """writes a WV file.
        self.iqData can be a list of complex or list of floats (iqiqiq format)."""

        #check if self.iqData is complex
        if isinstance(self.iqData[0], complex):
            self.__complex2iqiq__()

        self.NumberOfSamples = len(self.iqiqList) // 2

        #Find maximum magnitude and scale for max to be FullScale (1.0)
        power = []
        for n in range(self.NumberOfSamples):
            power.append(abs(self.iqiqList[2*n]**2 + self.iqiqList[2*n+1]**2))
        scaling = math.sqrt(max(power))

        # normalize to magnitude 1
        self.iqiqList = [iq / scaling for iq in self.iqiqList]
        #calculate rms in dB (below full scale)
        rms = math.sqrt(sum(power)/self.NumberOfSamples)/scaling
        rms = abs(20*math.log10(rms))
        # Convert to int16
        self.iqiqList = [math.floor(iq * 32767 +.5) for iq in self.iqiqList]

        try:
            file = open(FileName, "wb")
            file.write("{TYPE: SMU-WV,0}".encode("ASCII"))
            file.write("{COMMENT: R&S WaveForm, TheAE-RA}".encode("ASCII"))
            file.write(("{DATE: " + str(datetime.today())+ "}").encode("ASCII"))
            file.write(("{CLOCK:" +str(self.fSamplingRate) + "}").encode("ASCII"))
            file.write(("{LEVEL OFFS:" +  "{:2.4f}".format(rms) + ",0}").encode("ASCII"))
            file.write(("{SAMPLES:" + str(self.NumberOfSamples) + "}").encode("ASCII"))
        #    if(m1start > 0 && m1stop > 0)
        #        %Control Length only needed for markers
        #        fprintf(file_id,'%s',['{CONTROL LENGTH:' num2str(data_length) '}']);
        #        fprintf(file_id,'%s',['{CLOCK MARKER:' num2str(fSamplingRate) '}']);
        #        fprintf(file_id,'%s',['{MARKER LIST 1: ' num2str(m1start) ':1;' num2str(m1stop) ':0}']);
        #    end
            file.write(("{WAVEFORM-" +  str(4*self.NumberOfSamples+1) + ": #").encode("ASCII"))
            file.write(struct.pack("h"*len(self.iqiqList),*self.iqiqList))
            file.write("}".encode("ASCII"))
            file.close()
        except:
            print("File (" + FileName +") write error!" )
            return 0
        return self.NumberOfSamples

    def readWv(self,FileName):                  # Verified 2020.0115
        """Reads a WV file --> self.__iqiq2complex__ --> self.iqData"""
        try:
            file = open(FileName, "rb")
            data = file.read()
            file.close()
        except:
            print("File open error ("+ FileName+")!")
            return

        binaryStart = 0
        tags = ""
        Counter = 0
        ConverterSize = 20
        while (binaryStart == 0) & (Counter < len(data)):
            tags += data[Counter:Counter+ConverterSize].decode("ASCII","ignore")
            Counter += ConverterSize
            res = re.search("WAVEFORM.{0,20}:.{0,3}#",tags)
            if res is not None:
                binaryStart = res.span()[1]

        if (Counter > len(data)) & (binaryStart == 0):
            print("Required tags not found, potentially incompatible file format!")
            return

        res = re.search("SAMPLES[ ]*:[ ]*(?P<NumberOfSamples>[0-9]*)",tags)
        self.NumberOfSamples = int(res.group("NumberOfSamples"))
        res = re.search("CLOCK[ ]*:[ ]*(?P<SamplingRate>[0-9]*)",tags)
        self.fSamplingRate = float(res.group("SamplingRate"))
        data = list(struct.unpack("h"*self.NumberOfSamples*2, data[binaryStart:-1]))    #MMM data: IQ arry
        data = list(map( lambda x: x/32767.0, data ))                                   #MMM consumes a lot of time
        self.__iqiq2complex__(data)

    def writeXml(self, filenameiqw, filenamexml):                                       # Verified  2020.0115
        """Function to write the xml part of the iq.tar"""
        xmlfile = open (filenamexml, "w")
        xmlfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        xmlfile.write("<?xml-stylesheet type=\"text/xsl\" href=\"open_IqTar_xml_file_in_web_browser.xslt\"?>\n")
        xmlfile.write("<RS_IQ_TAR_FileFormat fileFormatVersion=\"2\" xsi:noNamespaceSchemaLocation=\"http://www.rohde-schwarz.com/file/RsIqTar.xsd\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n")
        xmlfile.write("<Name>Python iq.tar writer (self.iqData.py)</Name>\n")       #Optional
        xmlfile.write("<Comment>RS WaveForm, TheAE-RA</Comment>\n")                 #Optional
        xmlfile.write("<DateTime>"+ datetime.now(None).isoformat() +"</DateTime>\n")
        xmlfile.write("<Samples>" + str(self.NumberOfSamples) + "</Samples>\n")
        xmlfile.write("<Clock unit=\"Hz\">" + str(self.fSamplingRate) + "</Clock>\n")
        xmlfile.write("<Format>complex</Format>\n")
        xmlfile.write("<DataType>float32</DataType>\n")
        xmlfile.write("<ScalingFactor unit=\"V\">1</ScalingFactor>\n")              #Optional
        xmlfile.write("<NumberOfChannels>1</NumberOfChannels>\n")                   #Optional
        xmlfile.write("<DataFilename>" + filenameiqw+ "</DataFilename>\n")
        # xmlfile.write("<UserData></UserData>\n")                                  #Optional
        xmlfile.write("</RS_IQ_TAR_FileFormat>\n")
        xmlfile.close()
        return 1

    def writeIqTar(self, FileName):             # Verified 2020.0115  #pylint: disable=R1710
        """writes an iq.tar file. Complex self.iqData values are interpreted as Volts.
        self.iqData can be a list of complex or list of floats (iqiqiq format)."""
        path,filename = os.path.split(FileName)                                     #pylint: disable=W0612

        #Create binary file
        binaryfile = re.sub("iq.tar", "complex.1ch.float32", filename, flags=re.IGNORECASE)
        self.writeIqw(os.path.join(path, binaryfile))
        if self.NumberOfSamples == 0:
            return 0
        # xsltfilename = "open_IqTar_xml_file_in_web_browser.xslt"                  #xslt is optional
        xmlfilename = binaryfile + '.xml'
        self.writeXml(binaryfile, os.path.join(path, xmlfilename))

        try:
            tar = tarfile.open(FileName, "w")
            tar.add(os.path.join(path, binaryfile), arcname=binaryfile)
            #tar.add(os.path.join(path, xsltfilename), arcname=xsltfilename)         #xslt is optional
            tar.add(os.path.join(path, xmlfilename), arcname=xmlfilename)
            tar.close()
            os.remove(os.path.join(path, binaryfile))
            os.remove(os.path.join(path, xmlfilename))
        except:
            print("IqTar (" + FileName +") write error!" )
            return 0

    def readIqTar(self,FileName):               # Verified 2020.0115
        """Reads an iq.tar file --> self.iqData"""
        path,filename = os.path.split(FileName)                         #pylint: disable=W0612
        self.fSamplingRate = 0

        try:
            tar = tarfile.open(FileName, "r:")
            a=tar.getnames()
            xmlfile = [filename for filename in a if ".xml" in filename.lower()]
            xmlfile = xmlfile[0]
            tar.extract(xmlfile)
            tree = ET.parse(xmlfile)
            root = tree.getroot()
            binaryfilename = root.find("DataFilename").text
            self.fSamplingRate = float(root.find("Clock").text)
            helper = root.find("ScalingFactor")
            scaling = 1
            if helper:
                if helper.get("unit")!="V":
                    print("Only (V)olts scaling factor supported - assuming 1V!")
                else:
                    scaling = float(root.find("ScalingFactor").text)
            os.remove(xmlfile)
            del root
            tar.extract(binaryfilename)
            tar.close()
            self.readIqw(binaryfilename)
            os.remove(binaryfilename)
        except:
            print("IqTar (" + FileName +") read error!" )

        self.iqData = [sample * scaling for sample in self.iqData]                      #Apply scaling factor


    def main(self):
        #for testing only
        filename = "C:\\Users\\lim_m\\ownCloud\\ATE\\AA_Code\\DSP_python\\DSP_python\\SampleWv\\CW_10tones_32MHz_100usec.iq.tar"

        ### Read data
        if '.wv' in filename:
            self.readWv(filename)
        elif '.iq.tar' in filename:
            self.readIqTar(filename)
        elif '.iqw' in filename:
            self.readIqw(filename)
        else:
            print('Filetype not supported')

        start = time.time()
        self.writeIqTar(filename + '.iq.tar')
        self.writeWv(   filename + '.wv')
        self.writeIqw(  filename + '.iqw')
        duration = time.time() - start
        speed = self.NumberOfSamples/1e6/duration
        print("Total: %d samples in %2.2f ms. writeSpeed: %f MSamples/s"%(self.NumberOfSamples,duration*1e3,speed))

def dataConvert():
    ''' binary to float32 conversion '''
    # numpy.frombuffer dtype=float32()
    sampledata = b'\x0E\x78\x94\xB7'
    print('Data %s %d'%(sampledata,len(sampledata)))
    print("Float=",struct.unpack("<f",sampledata)) #Little Endian
    print("Float=",struct.unpack("<f",sampledata)) #Little Endian
    # print("Float=",array.frombytes(sampledata)) #Little Endian

if __name__ == "__main__":
    # execute only if run as a script
    # IQ().main()
    dataConvert()
