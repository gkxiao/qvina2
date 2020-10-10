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

def dock(receptor,ligand,configfile,vinaout,vinalog):
    #receptor: receptor file with PDBQT format
    #ligand: vina pdbqt file for ligand
    #configfile: vina docking configure file
    #Output: output pdbqt file
    cmdline = 'qvina2 --receptor '+receptor+' --ligand '+ligand+' --out '+vinaout+' --log '+vinalog+' --config '+configfile 
    os.system(cmdline)


def vs(receptor,dbase,configfile,output):
    #receptor: receptor file with PDBQT format
    #dbase: multiple ligand sdf file
    #configfile: vina docking configure file
    # Output: output sdf file
    docking_dir = tempfile.mkdtemp(suffix=None, prefix='qvina2_', dir=None)
    dbase = list(readfile("sdf", dbase))
    w = Outputfile("sdf",output,overwrite=True)
    for mol in dbase:
        title = mol.title
        id = title
        ofile = docking_dir+'/'+id+'.pdbqt'
        vinalog = docking_dir+'/'+id+'_vina.log'
        vinaout = docking_dir+'/'+id+'_vina.pdbqt'
        vinaoutsdf = docking_dir+'/'+id+'_vina.sdf'
        mol.write("pdbqt",ofile, overwrite=True)
        dock(receptor,ofile,configfile,vinaout,vinalog)
        os.system('rm -f '+ofile)
        os.system('rm -f '+vinalog)
        vina_pose_to_sdf(vinaout,vinaoutsdf)
        os.system('rm -f '+vinaout)
        os.system('cat '+vinaoutsdf+' >>'+output)
        os.system('rm -f '+vinaoutsdf)
    os.system('rm -fr '+docking_dir)

import sys,string,argparse
from optparse import OptionParser
parser = argparse.ArgumentParser(description="VS Using QuickVina2")
parser.add_argument('receptor', metavar='receptor',help="receptor in PDBQT file")
parser.add_argument('dbase', metavar='dbase', help="database in SDF file with full hydrogen")
parser.add_argument('config', metavar='configure_file', help="VINA docking configure file")
parser.add_argument('output', metavar='output', help="output file in SDF format")
args = parser.parse_args()
receptor = args.receptor
dbase = args.dbase
config = args.config
output = args.output
vs(receptor,dbase,config,output)
