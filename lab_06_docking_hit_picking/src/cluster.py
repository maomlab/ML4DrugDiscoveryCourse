

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import numpy as np
import scanpy as sc
import igraph as ig
import leidenalg as la


def cluster_leiden(embedding_tag, resolution = 1):
    embedding = pq.read_table(
        f"intermediate_data/embedding_{embedding_tag}/umap_embedding.parquet").to_pandas().to_numpy()
    embedding = sc.AnnData(embedding)
    sc.pp.neighbors(embedding, n_neighbors=10, n_pcs=40)
    
    # see https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.leiden.html for options
    # especially resolution (default = 1), higher values lead to more clusters.
    sc.tl.leiden(
        embedding,
        resolution = resolution,
        flavor="igraph")
    clusters = pd.DataFrame({'cluster_id' : embedding.obs['leiden']})
    pq.write_table(
        pa.Table.from_pandas(clusters),
        f"intermediate_data/embedding_{embedding_tag}/clusters.parquet")
    
