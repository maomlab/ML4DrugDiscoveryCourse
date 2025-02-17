

import datasets
import yaml

import pyarrow as pa
import pyarrow.parquet as pq


with open("parameters.yaml") as parameters_file:
    parameters = yaml.safe_load(parameters_file)


data_moldata = datasets.load_dataset(
    "maomlab/MolData",
    name = "MolData")

data_train_moldata = data_moldata['train'].to_pandas()
data_train_moldata = data_train_moldata[
    data_train_moldata.AID.isin(parameters['target_AIDs'])]
pq.write_table(
    pa.Table.from_pandas(data_train_moldata),
    "intermediate_data/data_train_moldata.parquet")

data_validation_moldata = data_moldata['validation'].to_pandas()
data_validation_moldata = data_validation_moldata[
    data_validation_moldata.AID.isin(parameters['target_AIDs'])]
pq.write_table(
    pa.Table.from_pandas(data_validation_moldata),
    "intermediate_data/data_validation_moldata.parquet")

data_test_moldata = data_moldata['validation'].to_pandas()
data_test_moldata = data_test_moldata[
    data_test_moldata.AID.isin(parameters['target_AIDs'])]
pq.write_table(
    pa.Table.from_pandas(data_test_moldata),
    "intermediate_data/data_test_moldata.parquet")
