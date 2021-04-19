""" Rohde & Schwarz Automation for demonstration use."""
#pylint: disable=invalid-name
##########################################################
### User Entry
##########################################################
import socket                       #Import socket module

def sQuery(SCPI):
    """Socket Query"""
    sWrite(SCPI)
    sOut = s.recv(2048).strip().decode()    # Read socket
    print(f'Query: {sOut}')
    return sOut

def sWrite(SCPI):
    """Socket Write"""
    print(f'Write: {SCPI}')
    s.sendall(f'{SCPI}\n'.encode())         # Write SCPI

##########################################################
### Main Code
##########################################################
s = socket.socket()                 #Create a socket object
s.connect(('192.168.58.114', 5025))
s.settimeout(1)                     #Timeout in seconds

sQuery('*IDN?')
