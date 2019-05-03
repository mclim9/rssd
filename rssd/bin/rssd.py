# -*- coding: future_fstrings -*-
#####################################################################
### Title : RSSD utility
### Author: Martin C Lim
### Date  : 2019.05.01
#####################################################################
from rssd.yaVISA_socket import jaVisa
import argparse
import rssd
import sys

def main():
    parser = argparse.ArgumentParser(description='RSSD Helper')
    parser.add_argument('-i','--idn', required=False, help='IDN from ip address')
    parser.add_argument('-b','--bar', required=False, help='Description for bar argument')
    args = parser.parse_args()          #Dictionary of args

    print(f'RSSD@ {rssd.__file__}')
    if args.idn:
        try:
            instr = jaVisa()
            instr.jav_Open(args.idn)
            instr.jav_Close()
        except:
            print(f'Could not open {args.idn}')

    if args.bar:
        print(f'Bar is: {args.bar}')

    # print(f'Number of arguments: {len(sys.argv)} arguments.')
    # print(f'Argument List:{str(sys.argv)}')

if __name__ == "__main__":
    main()
    sys.exit(0)