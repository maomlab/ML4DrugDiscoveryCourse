


import pandas as pd
import numpy as np

import pyarrow as pa
import pyarrow.parquet as pq


#####################################################################
# Check that we're using the gpu and it can be found through tourch
import torch

torch.cuda.is_available()
torch.cuda.device_count()
torch.cuda.current_device()


# https://blogs.deepmodeling.com/Uni-Mol2_18_12_2024/
import unimol_tools

clf = unimol_tools.UniMolRepr(
    data_type='molecule',                  
    remove_hs=False,                  
    model_name='unimolv2', # avaliable: unimolv1, unimolv2                 
    model_size='1.1B', # work when model_name is unimolv2. avaliable: 84m, 164m, 310m, 570m, 1.1B.                 
    )

# when I ran it I was getting ~ 10 (it/s) for getting conformers
# 10k (molecules) / 10 (it/s) / 60 (s/min) => ~15 minutes
D4_screen_10k = pq.read_table("intermediate_data/D4_screen_10k.parquet").to_pandas()
D4_screen_10k_features_unimol2 = clf.get_repr(D4_screen_10k['smiles'].values.tolist())
D4_screen_10k_features_unimol2 = np.array(D4_screen_10k_features_unimol2['cls_repr'])
np.save(
    "intermediate_data/D4_screen_10k_features_unimol2.npy",
    D4_screen_10k_features_unimol2)


# 100k / 10 / 60 / 60  => ~3-5 hours
D4_screen_100k = pq.read_table("intermediate_data/D4_screen_100k.parquet").to_pandas()
D4_screen_100k_features_unimol2 = clf.get_repr(D4_screen_100k['smiles'].values.tolist())
D4_screen_100k_features_unimol2 = np.array(D4_screen_100k_features_unimol2['cls_repr'])
np.save(
    "intermediate_data/D4_screen_100k_features_unimol2.npy",
    D4_screen_100k_features_unimol2)



D4_in_vitro = pd.read_csv("data/D4_in_vitro_data.csv")
D4_in_vitro_features_unimol2 = clf.get_repr(D4_in_vitro['smiles'].values.tolist())
D4_in_vitro_features_unimol2 = np.array(D4_in_vitro_features_unimol2['cls_repr'])
np.save(
    "intermediate_data/D4_in_vitro_features_unimol2.npy",
    D4_in_vitro_features_unimol2)
