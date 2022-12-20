#!/usr/bin/env python3

#Author David Simpson, 2022

import argparse
import sys

parser = argparse.ArgumentParser(description="Ceph EC calculator",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", "--servers", type=int, default=6, help="number of servers")
parser.add_argument("-d", "--drives", type=int, default=12, help="drives per server")
parser.add_argument("-c", "--capacity", type=int, default=12, help="drive capacity (TB)")
parser.add_argument("-k", "--chunks", type=int, default=4, help="EC chunks")
parser.add_argument("-m", "--parity", type=int, default=2, help="EC parity chunks")
parser.add_argument("-t", "--table", action='store_true', help="Print in tabulate form")
args = vars(parser.parse_args())


# *** VARS *********************

#SERVERS/OSDs
SERVER_COUNT=args["servers"]

#EC
EC_K=args["chunks"]  #number of chunks to divide object into
EC_M=args["parity"] #additional parity chunks
EC_TOTAL=EC_K+EC_M #total chunks, added for check only

#DRIVES
DRIVE_SIZE=args["capacity"] #TB
DRIVE_PER_SERVER=args["drives"]

#*** CHECKS *********************

if SERVER_COUNT < 1:
   print("ERROR - SERVER_COUNT SHOULD BE > 1")
   sys.exit(1)
if EC_K < 2:
   print("ERROR - K CHUNKS SHOULD BE > 2")
   sys.exit(1)
if EC_M < 1:
   print("ERROR - M PARTITY SHOULD BE > 1")
   sys.exit(1)
if DRIVE_SIZE < 1:
   print("ERROR - DRIVE_SIZE SHOULD BE > 1")
   sys.exit(1)
if DRIVE_PER_SERVER < 1:
   print("ERROR - DRIVE_PER_SERVER SHOULD BE > 1")
   sys.exit(1)

if EC_M >= EC_K:
   print("ERROR - M PARITY MUST BE LESS THAN K CHUNKS")
   sys.exit(1)

if EC_TOTAL > SERVER_COUNT:
   print("ERROR - SERVER_COUNT SHOULD BE >= EC CHUNK TOTAL (K+M)")
   print("SERVER_COUNT WAS "+str(SERVER_COUNT))
   print("K WAS "+str(EC_K))
   print("M WAS "+str(EC_M))
   print("EC CHUNK TOTAL WAS "+str(EC_TOTAL))
   sys.exit(1)

# ***CALCULATIONS IN TB***
SERVER_SIZE=(DRIVE_SIZE*DRIVE_PER_SERVER)
RAW=(SERVER_COUNT*SERVER_SIZE)

EFFICIENCY=float(EC_K/(float(EC_K+EC_M)))

FULL_USAGE=float(SERVER_COUNT*EFFICIENCY*SERVER_SIZE)
EIGHTY_FULL_USAGE=float(0.80*FULL_USAGE)

if args["table"] != True:

   # ***OUTPUT ***
   print("----")
   print("-c "+str(DRIVE_SIZE)+" | Using DRIVE_SIZE (TB) "+str(DRIVE_SIZE))
   print("-d "+str(DRIVE_PER_SERVER)+" | Using DRIVE_PER_SERVER "+str(DRIVE_PER_SERVER))
   print("-s "+str(SERVER_COUNT)+" | Using SERVER_COUNT "+str(SERVER_COUNT))
   print("----")
   print("Results in SERVER_SIZE (TB) "+str(SERVER_SIZE))
   print("Results in RAW (TB) "+str(RAW))
   print("----")
   print("-k "+str(EC_K)+" | Using K (min copy) of "+str(EC_K))
   print("-m "+str(EC_M)+" | Using M (resiliancy) of "+str(EC_M))
   print("----")
   print("EFFICIENCY RATIO")
   print(str(round(EFFICIENCY, 3)))
   print("----")
   print("FULL CAPACITY (TB) AT 100% **NOT RECOMMENDED!**")
   print(round(FULL_USAGE, 3))
   print("----")
   print("80% CAPACITY (TB) - RECOMMENDED MAX FOR CEPH (SAFE CAPACITY RESERVERVATION)")
   print(round(EIGHTY_FULL_USAGE, 3))

if args["table"] == True:
   from tabulate import tabulate
   table_output=[[str(DRIVE_SIZE),str(DRIVE_PER_SERVER),str(SERVER_COUNT),str(EC_K),str(EC_M),str(round(EFFICIENCY, 3)),str(round(FULL_USAGE, 3)),str(round(EIGHTY_FULL_USAGE, 3))]]
   headers =['DriveSize(TB)','Drives','Servers','K','M','EFFICIENCY RATIO','100% CAPACITY (TB)','80% CAPACITY (TB)']
   print(tabulate(table_output, headers, tablefmt="heavy_grid"))

