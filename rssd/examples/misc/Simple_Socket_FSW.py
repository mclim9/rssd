""" Rohde & Schwarz Automation for demonstration use."""
#pylint: disable=E0611,E0401
##########################################################
### User Entry
##########################################################
host = '192.168.58.109'          #Instrument IP address
port = 5025                      #Instrument control port

##########################################################
### Code Begin
##########################################################
import socket                    #Import socket module

def sQuery(SCPI):
   out = SCPI + "\n"
   s.sendall(out.encode())       #Write 'cmd'
   sOut = s.recv(2048).strip()   #read socket
   return sOut.decode()

def sWrite(SCPI):
   out = SCPI + "\n"
   s.sendall(out.encode())       #Write 'cmd'
   
##########################################################
### Main Code
##########################################################
s = socket.socket()              #Create a socket object
s.connect((host, port))
s.settimeout(1)                  #Timeout in seconds

sWrite(':INP:FILE:PATH "C:\LTE-TM11-20MHz.iq.tar"')
sWrite(':INP:SEL FIQ')
