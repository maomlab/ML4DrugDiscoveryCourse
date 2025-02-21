
import pandas as pd
import numpy as np

import pyarrow as pa
import pyarrow.parquet as pq

from molfeat.calc import FPCalculator
from molfeat.trans import MoleculeTransformer



calc = FPCalculator("ecfp")
mol_transf = MoleculeTransformer(calc, n_jobs=10)


data_train_moldata = pq.read_table("intermediate_data/data_train_moldata.parquet").to_pandas()
data_train_features = mol_transf(data_train_moldata['SMILES'].values)
data_train_features = np.stack(data_train_features)
data_train_features = pd.DataFrame(data_train_features)
pq.write_table(
    pa.Table.from_pandas(data_train_features),
    "intermediate_data/data_train_features.parquet")


data_validation_moldata = pq.read_table("intermediate_data/data_validation_moldata.parquet").to_pandas()
data_validation_features = mol_transf(data_validation_moldata['SMILES'].values)
data_validation_features = np.stack(data_validation_features)
data_validation_features = pd.DataFrame(data_validation_features)
pq.write_table(
    pa.Table.from_pandas(data_validation_features),
    "intermediate_data/data_validation_features.parquet")


data_test_moldata = pq.read_table("intermediate_data/data_test_moldata.parquet").to_pandas()
data_test_features = mol_transf(data_test_moldata['SMILES'].values)
data_test_features = np.stack(data_test_features)
data_test_features = pd.DataFrame(data_test_features)
pq.write_table(
    pa.Table.from_pandas(data_test_features),
    "intermediate_data/data_test_features.parquet")

