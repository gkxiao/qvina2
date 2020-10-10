import sys,string,argparse
from optparse import OptionParser
parser = argparse.ArgumentParser(description="VS Using QuickVina2")
parser.add_argument('receptor', metavar='receptor',help="receptor in PDBQT file")
parser.add_argument('dbase', metavar='dbase', help="database in SDF file with full hydrogen")
parser.add_argument('config', metavar='configure_file', help="VINA docking configure file")
parser.add_argument('output', metavar='output', help="Docking output file in SDF format")
parser.add_argument('prefix', metavar='prefix', help="prefix for SLURM script file")
args = parser.parse_args()
receptor = args.receptor
dbase = args.dbase
config = args.config
output = args.output
prefix = args.prefix
slurmscript = prefix+'_to_run_qvina2_vs.sbatch'
slurmout = open(slurmscript,"w")
slurmout.write('#!/bin/sh \n')
slurmout.write('#SBATCH -N 1\n')
slurmout.write('#SBATCH -o '+prefix+'_out.%j\n')
slurmout.write('#SBATCH -e '+prefix+'_err.%j\n')
slurmout.write('cd  $SLURM_SUBMIT_DIR\n')
slurmout.write('source ~/bin/rdkit2020_env.sh\n')
slurmout.write('python  ~/bin/qvina2.py '+receptor+' '+dbase+' '+config+' '+output+' >>'+prefix+'_vina.log \n')
slurmout.close

