

import pandas as pd
import numpy as np

import pyarrow as pa
import pyarrow.parquet as pq

from molfeat.calc import FPCalculator
from molfeat.trans import MoleculeTransformer



calc = FPCalculator("ecfp")
mol_transf = MoleculeTransformer(calc, n_jobs=10)

D4_screen_10k = pq.read_table("intermediate_data/D4_screen_10k.parquet").to_pandas()
D4_screen_10k_features_ecfp = mol_transf(D4_screen_10k['smiles'].values)
np.save(
    "intermediate_data/D4_screen_10k_features_ecfp.npy",
    D4_screen_10k_features_ecfp)

D4_screen_100k = pq.read_table("intermediate_data/D4_screen_100k.parquet").to_pandas()
D4_screen_100k_features_ecfp = mol_transf(D4_screen_100k['smiles'].values)
np.save(
    "intermediate_data/D4_screen_100k_features_ecfp.npy",
    D4_screen_100k_features_ecfp)


D4_in_vitro = pd.read_csv("data/D4_in_vitro_data.csv")
D4_in_vitro_features_ecfp = mol_transf(D4_in_vitro['smiles'].values)
np.save(
    "intermediate_data/D4_in_vitro_features_ecfp.npy",
    D4_in_vitro_features_ecfp)



