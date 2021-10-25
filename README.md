# Ray's Design Library

## What will you find?
1. A KLayout `p-cell` library - written in Python - of photolithography utilities
2. PCB Board Design Files
3. Devices Layout
4. Layouts used for past fabrication runs

## Naming Convention
All the files the library follows a specific naming convention consisting of 5 descriptors separated by a single underscore.

|# |Descriptor   | Example   |
|---|---|---|
|1| Start with your initials  | RS  |
|2| The main project that the design is relevant for  | GaAs, RC, MISC,...  |
|3| The name of the design   | EtchTest, Mesa, Hallbar, ...  |
|4| The design dimension, in mm  | 6x7, 6x6, W4in, NA...  |
|5| The date, in MMDDYY  | October 15, 2021 represented as 101521  |

Every project in the library is given a 2 to 4 alphabet code. 
| Project  | Code  |
|---|---|
| Ohmic contacts to 2DES in GaAs heterostructures | [2DEG](#2deg) |
| Distributed broadband filter on Si | [RC](#rc) |
| Other Designs (utilities, test patterns) | [MISC](#misc) |

## 2DEG

| Filename | Description | Preview |
|---|---| --- |
| `RS_2DEG_Hallbar+OhmicsTest_6x6_101821`  | Four hall bar mesas + ohmic contacts. In addition to the hall bars, there are also plenty of free ohmic contacts that can be used for testing. |  |


## RC


## MISC

| Filename | Description | Preview |
|---|---|---|
| `RS_MISC_TLMEtchTest_6x6_101821`  | 300 um squares with spacing equal to 100, 200, 300, 400, 500, 600, 700 um.  | |
| `RS_MISC_TLMTemplate_NA_101821`  | 2.2 mm long rectangular mesa, with square Ohmic contacts forming a grid. | |
| `RS_MISC_EtchTest_5x5_101821`  | Etch test involving a variety of squares, circles, and test patterns.  | |
| `RS_MISC_EtchTestFlattened_5x5_101821` | Identical to `RS_MISC_EtchTest_5x5_101821`, but all PCells are flattened and merged together | |
| `RS_MISC_LineEtchTest_6x6_081821`  | Rows of vertical lines with varying thicknesses. Each line has a label indicating its thickness.  | |

