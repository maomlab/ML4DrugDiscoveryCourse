
import pandas as pd
import numpy as np

import pyarrow as pa
import pyarrow.parquet as pq
import yaml

import h2o
from h2o.automl import H2OAutoML

with open("parameters.yaml") as parameters_file:
    parameters = yaml.safe_load(parameters_file)


# Start the H2O cluster (locally)
h2o.init()


data_train = pq.read_table(
    "intermediate_data/data_train.parquet").to_pandas()

