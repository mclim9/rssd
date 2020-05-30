# -*- coding: future_fstrings -*-
#####################################################################
### Title : RSSD utility
### Author: Martin C Lim
### Date  : 2019.05.01
#####################################################################
import argparse
import sys
import os
import rssd
from rssd.yaVISA_socket import jaVisa

def main():
    parser = argparse.ArgumentParser(description='RSSD Helper')
    parser.add_argument('-i','--idn', required=False, help='IDN from ip address')
    parser.add_argument('-b','--bar', required=False, help='Description for bar argument')
    args = parser.parse_args()          #Dictionary of args

    print(f'RSSD Examples@ {os.path.dirname(rssd.__file__)}\\examples')
    os.chdir(os.path.dirname(rssd.__file__)+'\\examples')

    if args.idn:
        try:
            instr = jaVisa()
            instr.jav_Open(args.idn)
            instr.jav_Close()
        except:
            print(f'Could not open {args.idn}')

    if args.bar:
        print(f'BBar is: {args.bar}')

    # print(f'Number of arguments: {len(sys.argv)} arguments.')
    # print(f'Argument List:{str(sys.argv)}')

if __name__ == "__main__":
    main()
    sys.exit(0)
