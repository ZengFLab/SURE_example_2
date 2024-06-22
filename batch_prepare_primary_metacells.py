import subprocess 
import glob
import pandas as pd
import scanpy as sc

cmd='rm prepare_metacell_B*.ipynb; rm *_B*metacells.h5ad'
subprocess.call(cmd, shell=True)

files = glob.glob('*_B*_counts.txt.gz')
n_batches = len(files)

for i in range(n_batches):
    mc = f'prepare_metacell_B{i+1}.ipynb'
    cmd1 = f'cp bk_prepare_primary_metacell_B1.ipynb {mc}'
    cmd2 = f'sed -i "s/B1/B{i+1}/g" {mc}'
    subprocess.call(f'{cmd1};{cmd2}', shell=True)
    

for i in range(n_batches):
    mc = f'prepare_metacell_B{i+1}.ipynb'
    subprocess.call(f'jupyter nbconvert --execute --to=notebook --inplace {mc}', shell=True)
    
    
# combine all
files = glob.glob('*_B*_metacells.h5ad')

adata_list = []

for fl in files:
    tmp = sc.read_h5ad(fl)
    adata_list.append(tmp)
    
adata = sc.concat(adata_list)
adata.write_h5ad('multiome_neurips21_primary_metacells.h5ad')