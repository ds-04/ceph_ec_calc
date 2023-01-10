#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser(description="Ceph EC calculator - calculate EC using servers,drives,capacity OR osds,capacity",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", "--servers", type=int, default=6, help="number of servers")
parser.add_argument("-d", "--drives", type=int, default=12, help="drives per server, where each is an OSD")
parser.add_argument("-o", "--osds", type=int, default=0, help="total number of OSDs, this supersedes usage of servers*drives, capacity should still be used")
parser.add_argument("-c", "--capacity", type=int, default=12, help="drive capacity (TB) - AKA OSD size")
parser.add_argument("-k", "--chunks", type=int, default=4, help="EC chunks")
parser.add_argument("-m", "--parity", type=int, default=2, help="EC parity chunks")
parser.add_argument("-t", "--table", action='store_true', help="Print in tabulate form")
args = vars(parser.parse_args())


# *** VARS *********************

#SERVERS/OSDs
SERVER_COUNT=args["servers"]
OSD_COUNT=args["osds"]

#EC
EC_K=args["chunks"]  #number of chunks to divide object into
EC_M=args["parity"] #additional parity chunks
EC_TOTAL=EC_K+EC_M #total chunks, added for check only

#DRIVES
DRIVE_SIZE=args["capacity"] #TB
DRIVE_PER_SERVER=args["drives"]

#*** CHECKS *********************

if OSD_COUNT < 0:
   print("ERROR - CANT HAVE NEGATIVE OSD COUNT")
   sys.exit(1)
if OSD_COUNT == 1:
   print("ERROR - CANT HAVE OSD COUNT OF 1")
   sys.exit(1)
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

if (EC_TOTAL > SERVER_COUNT and OSD_COUNT <= 0) or (EC_TOTAL > OSD_COUNT and OSD_COUNT > 1):
   print("ERROR - SERVER_COUNT OR OSD_COUNT SHOULD BE >= EC CHUNK TOTAL (K+M)")
   print("K WAS "+str(EC_K))
   print("M WAS "+str(EC_M))
   print("EC CHUNK TOTAL WAS "+str(EC_TOTAL))
   sys.exit(1)


# ***CALCULATIONS **
EFFICIENCY=float(EC_K/(float(EC_K+EC_M)))

# ***CALCULATIONS CONT. (IN TB)***
#use OSD count if specified
if OSD_COUNT > 1:
   RAW=(OSD_COUNT*DRIVE_SIZE)
else:
#if OSD_COUNT NOT USED, USE SERVER+DRIVES COUNTS
   SERVER_SIZE=(DRIVE_SIZE*DRIVE_PER_SERVER)
   RAW=(SERVER_COUNT*SERVER_SIZE)

FULL_USAGE=float(EFFICIENCY*RAW)
EIGHTY_FULL_USAGE=float(0.80*FULL_USAGE)

if args["table"] != True:
   # ***OUTPUT ***
   if OSD_COUNT == 0:
      print("----")
      print("**** Using --servers NOT --osds ****")
      print("----")
      print("-c "+str(DRIVE_SIZE)+" | Using DRIVE|OSD_SIZE (TB) "+str(DRIVE_SIZE))
      print("-d "+str(DRIVE_PER_SERVER)+" | Using DRIVE|OSD_PER_SERVER "+str(DRIVE_PER_SERVER))
      print("-s "+str(SERVER_COUNT)+" | Using SERVER_COUNT "+str(SERVER_COUNT))
      print("Results in SERVER_SIZE (TB) "+str(SERVER_SIZE))
   if OSD_COUNT > 1:
      print("----")
      print("**** Using --osds NOT --servers ****")
      print("----")
      print("-c "+str(DRIVE_SIZE)+" | Using DRIVE|OSD_SIZE (TB) "+str(DRIVE_SIZE))
      print("-o "+str(OSD_COUNT)+" | Using OSD_COUNT "+str(OSD_COUNT))
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
   if OSD_COUNT == 0:
      table_output=[[str(DRIVE_SIZE),str(DRIVE_PER_SERVER),str(SERVER_COUNT),str(EC_K),str(EC_M),str(round(EFFICIENCY, 3)),str(round(FULL_USAGE, 3)),str(round(EIGHTY_FULL_USAGE, 3))]]
      headers =['Drive|OSD Size(TB)','Drives|OSD Per Server','Servers','K','M','EFFICIENCY RATIO','100% CAPACITY (TB)','80% CAPACITY (TB)']
   if OSD_COUNT > 1:
      table_output=[[str(DRIVE_SIZE),str(OSD_COUNT),str(EC_K),str(EC_M),str(round(EFFICIENCY, 3)),str(round(FULL_USAGE, 3)),str(round(EIGHTY_FULL_USAGE, 3))]]
      headers =['Drive|OSD Size(TB)','nOSDs','K','M','EFFICIENCY RATIO','100% CAPACITY (TB)','80% CAPACITY (TB)']
   print(tabulate(table_output, headers, tablefmt="heavy_grid"))
