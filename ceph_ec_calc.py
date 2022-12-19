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
args = vars(parser.parse_args())


# *** VARS *********************

#SERVERS/OSDs
SERVER_COUNT=args["servers"]

#EC
EC_K=args["chunks"]  #number of chunks to divide object into
EC_M=args["parity"] #additional parity chunks

#DRIVES
DRIVE_SIZE=args["capacity"] #TB
DRIVE_PER_SERVER=args["drives"]

#*** CHECKS *********************

if SERVER_COUNT < 1:
   print("ERROR - SERVER_COUNT SHOULD BE > 1")
   sys.exit(1)
if EC_K < 2:
   print("ERROR - CHUNKS SHOULD BE > 2")
   sys.exit(1)
if EC_M < 1:
   print("ERROR - PARTITY SHOULD BE > 1")
   sys.exit(1)
if DRIVE_SIZE < 1:
   print("ERROR - DRIVE_SIZE SHOULD BE > 1")
   sys.exit(1)
if DRIVE_PER_SERVER < 1:
   print("ERROR - DRIVE_PER_SERVER SHOULD BE > 1")
   sys.exit(1)

if EC_M >= EC_K:
   print("ERROR - PARITY MUST BE LESS THAN CHUNKS")
   sys.exit(1)

# ***CALCULATIONS IN TB***
SERVER_SIZE=(DRIVE_SIZE*DRIVE_PER_SERVER)
RAW=(SERVER_COUNT*SERVER_SIZE)

EFFICIENCY=float(EC_K/(float(EC_K+EC_M)))

FULL_USAGE=float(SERVER_COUNT*EFFICIENCY*SERVER_SIZE)
EIGHTY_FULL_USAGE=float(0.80*FULL_USAGE)

# ***OUTPUT ***
print("----")
print("Using DRIVE_SIZE (TB) "+str(DRIVE_SIZE))
print("Using DRIVE_PER_SERVER "+str(DRIVE_PER_SERVER))
print("Results in SERVER_SIZE of "+str(SERVER_SIZE))
print("Using SERVER_COUNT "+str(SERVER_COUNT))
print("Results in RAW (TB) "+str(RAW))
print("----")
print("Using K (min copy) of "+str(EC_K))
print("Using M (resiliancy) of "+str(EC_M))
print("Results in EFFICIENCY RATIO of "+str(round(EFFICIENCY, 3)))
print("----")
print("FULL CAPACITY AT 100% **NOT RECOMMENDED!**")
print(round(FULL_USAGE, 3))
print("----")
print("80% CAPACITY - RECOMMENDED MAX FOR CEPH (SAFE CAPACITY RESERVERVATION)")
print(round(EIGHTY_FULL_USAGE, 3))
