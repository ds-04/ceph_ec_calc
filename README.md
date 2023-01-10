# ceph_ec_calc

<h1>Introduction</h1>

Ceph erasure coding calculator python3 
<br><br>
**USE AT OWN RISK: TESTING, IMPROVEMENTS, COMMENTS WELCOME**
<br><br>
- run with no args to produce example output 
- ```-t``` for tabulate 
- ```--help``` to see help


<h1>Example outputs</h1>

Two equivalent calculations are shown below. The EC scheme and resultant numbers are just for an example here...

<h2>OSD based calculation</h2>


```
----
**** Using --osds NOT --servers ****
----
-c 12 | Using DRIVE|OSD_SIZE (TB) 12
-o 72 | Using OSD_COUNT 72
Results in RAW (TB) 864
----
-k 4 | Using K (min copy) of 4
-m 2 | Using M (resiliancy) of 2
----
EFFICIENCY RATIO
0.667
----
FULL CAPACITY (TB) AT 100% **NOT RECOMMENDED!**
576.0
----
80% CAPACITY (TB) - RECOMMENDED MAX FOR CEPH (SAFE CAPACITY RESERVERVATION)
460.8
```

The same with ```-t```

```
Drive|OSD Size(TB)    nOSDs    K    M    EFFICIENCY RATIO    100% CAPACITY (TB)    80% CAPACITY (TB)
--------------------  -------  ---  ---  ------------------  --------------------  -------------------
                  12       72    4    2               0.667                   576                460.8
```

<h2>Server based calculation - where assumption is servers*drives = osd count</h2>

```
----
**** Using --servers NOT --osds ****
----
-c 12 | Using DRIVE|OSD_SIZE (TB) 12
-d 12 | Using DRIVE|OSD_PER_SERVER 12
-s 6 | Using SERVER_COUNT 6
Results in SERVER_SIZE (TB) 144
Results in RAW (TB) 864
----
-k 4 | Using K (min copy) of 4
-m 2 | Using M (resiliancy) of 2
----
EFFICIENCY RATIO
0.667
----
FULL CAPACITY (TB) AT 100% **NOT RECOMMENDED!**
576.0
----
80% CAPACITY (TB) - RECOMMENDED MAX FOR CEPH (SAFE CAPACITY RESERVERVATION)
460.8
```

The same with ```-t```

```
Drive|OSD Size(TB)    Drives|OSD Per Server    Servers    K    M    EFFICIENCY RATIO    100% CAPACITY (TB)    80% CAPACITY (TB)
--------------------  -----------------------  ---------  ---  ---  ------------------  --------------------  -------------------
                  12                       12          6    4    2               0.667                   576                460.8
```
