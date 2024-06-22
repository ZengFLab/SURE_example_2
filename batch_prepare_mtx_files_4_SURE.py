import pandas as pd
import numpy as np
import scanpy as sc
import subprocess

import datatable as dt

from sklearn.preprocessing import OneHotEncoder

batch_size = 10000 # expected number of cells in each partitioned file
n_top_genes = 3000 # number of HVGs being used
target_sum = 1e4 # use for finding HVGs

cmd='rm *_B*_*.gz'
subprocess.call(cmd, shell=True)

print('load h5ad')
adata_ = sc.read_h5ad('GSE194122_openproblems_neurips2021_multiome_BMMC_processed.h5ad')
adata_.layers['counts'] = adata_.X.copy()

adata_.obs['Batch'] = adata_.obs['Site']
batches = adata_.obs['Batch'].value_counts().reset_index()
batches.columns = ['Batch','Value']

parts = []
conds = np.unique(batches['Batch'].tolist())
for co in conds: 
    tmp = adata_[adata_.obs.Batch.isin([co])].copy()
    total_size = tmp.shape[0]
    num_batches = int(np.ceil(total_size / batch_size))
    num_batches = num_batches if num_batches > 0 else 1
    pas = np.array_split(tmp.obs_names.tolist(), num_batches)
    parts.extend(pas)


parts_ = parts
parts = [x for x in parts_ if len(x)>0 ]


for i in np.arange(len(parts)):
    cells = parts[i]
    adata = adata_[cells].copy()
    batch='B{}'.format(i+1)

    print(f'{batch} / {len(parts)}    size ' + '{}'.format(adata.shape))
    
    sc.pp.normalize_total(adata, target_sum=target_sum)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes, subset=True)

    dt.Frame(pd.DataFrame(adata.layers['counts'].toarray(), columns=adata.var_names, dtype=np.float64)).to_csv(f'multiome_neurips21_{batch}_counts.txt.gz')

    adata.obs_names.to_frame().to_csv(f'multiome_neurips21_{batch}_cell.csv.gz', index=None)
    adata.var_names.to_frame().to_csv(f'multiome_neurips21_{batch}_gene.csv.gz', index=None)

    enc = OneHotEncoder(sparse_output=False).fit(adata.obs['DonorNumber'].to_numpy().reshape(-1,1))
    pd.DataFrame(enc.transform(adata.obs['DonorNumber'].to_numpy().reshape(-1,1)), columns=enc.categories_).to_csv(f'multiome_neurips21_{batch}_uwv.txt.gz', index=False)
