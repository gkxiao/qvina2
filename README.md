# qvina2
a python script to use qvina2 as docking engine to run virtual screening against a database in MDL sdf format.

#prerequisite
1. qvina is availale from current PATH
2. The full hydrogen is add in the MDL SDF file
3. python 3+
4. Openbabel 2.4+ for python
5. slurm scheduler

# installation
put the qvina.py,qvina2_vs_slurm.py and qvina2 in ~/bin which is availabe in $PATH

# usage
step 1. generate slurm batch file
<pre line="1" lang="shell">
python ~/bin/qvina2_vs_slurm.py -h
</pre>
<pre line="1" lang="shell">
usage: qvina2_vs_slurm.py [-h] receptor dbase configure_file output prefix

VS Using QuickVina2

positional arguments:
  receptor        receptor in PDBQT file
  dbase           database in SDF file with full hydrogen
  configure_file  VINA docking configure file
  output          Docking output file in SDF format
  prefix          prefix for SLURM script file

optional arguments:
  -h, --help      show this help message and exit
</pre>  

<pre line="1" lang="shell">
git clone https://github.com/gkxiao/qvina2.git
cd qvina2
python ~/bin/qvina2_vs_slurm.py 4no7_prot.pdbqt dbase.sdf config.txt qvina_vs
</pre>

step 2. submit slurm job
<pre line="1" lang="shell">
sbatch -N 1 -c 1 qvina_vs.sbatch
</pre>

# CONVERT pdbqt docking pose into sdf file
usage: 
<pre line="1" lang="shell">
python pdbqt_pose_2_sdf.py  -h 
</pre>

example：
<pre line="1" lang="shell">
python pdbqt_pose_2_sdf.py  PV-000071980170.pdbqt  PV-000071980170.sdf
</pre>

