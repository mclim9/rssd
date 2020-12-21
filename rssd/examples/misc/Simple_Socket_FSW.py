""" Rohde & Schwarz Automation for demonstration use."""
#pylint: disable=E0611,E0401
#pylint: disable=invalid-name
##########################################################
### User Entry
##########################################################
import socket                       #Import socket module
host = '192.168.58.109'             #Instrument IP address
port = 5025                         #Instrument control port

##########################################################
### Code Begin
##########################################################
def sQuery(SCPI):
    """Socket Query"""
    print(f'Write: {SCPI}')
    out = SCPI + "\n"
    s.sendall(out.encode())         #Write 'cmd'
    sOut = s.recv(2048).strip()     #read socket
    sOut = sOut.decode()
    print(f'Query: {sOut}')
    return sOut

def sWrite(SCPI):
    """Socket Write"""
    print(f'Write: {SCPI}')
    out = SCPI + "\n"
    s.sendall(out.encode())         #Write 'cmd'

##########################################################
### Main Code
##########################################################
s = socket.socket()                 #Create a socket object
s.connect((host, port))
s.settimeout(1)                     #Timeout in seconds

sQuery('*IDN?')
