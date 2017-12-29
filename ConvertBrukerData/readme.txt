Although there are several tools available to convert Bruker 2dseq files into a more standard format, each of the has some advantages and disadvantages.

For most applications I would recommend this well maintained tool on https://github.com/neurolabusc/Bru2Nii

However, I found that it does not read the parameter #Segments for multi-shot EPIs, which results in a NIFTI file with wrong time resolution.

The simple python script provided here reads the necessary parameters from the "method" file of the scan-folder from which it is called, and executes AFNI's "to3D" program to create a .BRIK and .HEAD file.

The code is very simple and easy to edit. Some parameters are hardcoded so that it probably only works for 2D EPI scans. Use at your own risk.
