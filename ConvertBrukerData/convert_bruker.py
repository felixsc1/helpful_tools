#!/usr/bin/python3

#usage: run script within main scan folder, e.g. /17,  where the method file resides.  No arguments required

#read the parametes from bruker files to convert EPI scans using to3d
# WARNING: Only tested with normal 2D EPI.
# currently assuming zero interslice distance. 

import os   #assuming this script is run from the scan folder
import re  #regular expressions, to search the text.
import subprocess #see manual https://docs.python.org/3/library/subprocess.html


#os.chdir('D:\\MRDATA\\20171222_FSc_iso\\16')

cwd = os.getcwd()

#####Part 1: read the parameters from method file


method = open(os.path.join(cwd,'method')) #using os methods for script to work under windows&linux

method_fulltext = method.read()


TR1 = re.compile(r'##\$PVM_RepetitionTime=(\d+)')
Matrix1 = re.compile('##\$PVM_Matrix=\\( 2 \\)\s(\d+)\s(\d+)')
Repetitions1 = re.compile(r'##\$PVM_NRepetitions=(\d+)')
Slices1 = re.compile('##\$PVM_SPackArrNSlices=\\( 1 \\)\s(\d+)')
Slice_thickness1 = re.compile(r'##\$PVM_SliceThick=(\d+\.\d+)')
FOV1 = re.compile('##\$PVM_Fov=\\( 2 \\)\s(\d+)\s(\d+)')
Segments1 = re.compile(r'##\$NSegments=(\d+)')

TR = TR1.search(method_fulltext)
TR = TR.group(1)

Matrix = Matrix1.search(method_fulltext)
Matrix = Matrix.group(1,2)

Repetitions = Repetitions1.search(method_fulltext)
Repetitions = Repetitions.group(1)

Slices = Slices1.search(method_fulltext)
Slices = Slices.group(1)

Slice_thickness = Slice_thickness1.search(method_fulltext)
Slice_thickness = Slice_thickness.group(1)

FOV = FOV1.search(method_fulltext)
FOV = FOV.group(1,2)

Segments = Segments1.search(method_fulltext)
Segments = Segments.group(1)

if int(Repetitions) == 1:
	print('WARNING! Scan has only one repetition!')

####part 2: calculate parameters and create the to3d command

filename = os.path.basename(cwd)
os.chdir(os.path.join(cwd,'pdata','1'))

#example
#to3d -epan -view orig -prefix $argv[1] -time:zt 9 960 1500 alt+z -xFOV 8L-R -yFOV 6A-P -zSLAB 2.25I-S 3D:0:0:128:96:8640:"$argv[1].2dseq"

TR = str(int(TR)*int(Segments)) #for multi-shot EPI
xFOV = str(float(FOV[0])/2)
yFOV = str(float(FOV[1])/2)
zSLAB = str(float(Slices)*float(Slice_thickness)/2)
read = Matrix[0]
phase = Matrix[1]
images = str(int(Repetitions)*int(Slices))

to3d = 'to3d -epan -view orig -prefix E' + filename + ' -time:zt ' \
        + Slices + ' '      \
        + Repetitions + ' ' \
        + TR + ' alt+z -xFOV ' \
        + xFOV + 'L-R -yFOV '  \
        + yFOV + 'A-P -zSLAB ' \
        + zSLAB + 'I-S 3D:0:0:'\
        + read + ':' + phase + ':' \
        + images + ':' + '"2dseq"'
        
print(to3d)
#to3d= 'to3d -epan -view orig -prefix ' + filename + ' -time:zt ' + Slices 960 1500 alt+z -xFOV 8L-R -yFOV 6A-P -zSLAB 2.25I-S 3D:0:0:128:96:8640:"$argv[1].2dseq"



#####part3: run AFNI to3d

subprocess.run(to3d,shell=True, check=True) #test later if shell=true can be removed.


if int(Repetitions) == 1:
	print('WARNING! Scan has only one repetition!')