from openbabel import *
from pybel import *
import tempfile
import os

def vina_pose_to_sdf(ifile,ofile):
    """
    Convert Vina Docking Output PDBQT file into SDF file with pose id and vina docking score.
    Usage: vina_pose_to_sdf("input.pdbqt","output.sdf")
    """
    output = Outputfile("sdf",ofile,overwrite=True)
    poses = list(readfile("pdbqt",ifile))
    for i in range(len(poses)):
        poseid = poses[i].data['MODEL']
        del poses[i].data['MODEL']
        vinascore = poses[i].data['REMARK'].split()[2]
        del poses[i].data['REMARK']
        del poses[i].data['TORSDO']
        poses[i].data['POSE_ID'] = poseid
        poses[i].data['VINA_SCORE'] = vinascore
        output.write(poses[i]) 

import sys,string,argparse
from optparse import OptionParser
parser = argparse.ArgumentParser(description="convert PDBQT pose to sdf")
parser.add_argument('input', metavar='input',help="PDBQT pose file")
parser.add_argument('output', metavar='output', help="output file in SDF format")
args = parser.parse_args()
input = args.input
output = args.output
vina_pose_to_sdf(input,output)
