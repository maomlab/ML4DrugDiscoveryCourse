# -*- tab-width:4;indent-tabs-mode:nil;show-trailing-whitespace:t;rm-trailing-spaces:t -*-
# vi: set ts=2 noet:

import time
import os
import shutil
import joblib
import numpy as np
import pyarrow.parquet
import pyarrow as pa
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import (PCA, IncrementalPCA)
import umap
import pandas as pd
import datashader
from datashader.transfer_functions import set_background
from datashader.colors import viridis
from datashader.colors import colormap_select
from colorcet import fire




def fit_embedding(
        dataset,
        embed_dir,
        standardize_features=True,
        pca_n_components=None,
        pca_batch_size=1000,
        umap_n_components=2,
        umap_init='random',
        umap_n_neighbors=100,
        umap_min_dist=0.0,
        umap_a=None,
        umap_b=None,
        umap_negative_sample_rate=5,
        umap_metric='euclidean',
        umap_n_epochs=None,
        low_memory=False,
        save_transform=True,
        seed=None,
        verbose=True):
    """
    dataset: a feature matrix e.g. of (N, F) dimensions, used to define the embedding
    After some experimentation with chemical features of 1024 of 50k-.5M compounds,
    a reasonable embedding first reduces by PCA to 20 dimensions and then UMAP to 2 dimensions.
    UMAP parameters of 100 neighbors and min_dist of 0.0 seem to work well too. init='random'
    can help UMAP from getting stuck.
    return:
        saves embedding data to
            ../intermediate_data/embeddings/tag/embedding_info.tsv
            ../intermediate_data/embeddings/tag/pca_reducer.joblib
            ../intermediate_data/embeddings/tag/umap_reducer.joblib
    """
    if not os.path.exists(embed_dir):
        os.mkdir(embed_dir)
    else:
        print("WARNING: embed_dir already exists: {}".format(embed_dir))

    random_state = np.random.RandomState(seed=seed)

    begin_time = time.time()

    if standardize_features:
        if verbose:
            print("Standardizing dataset so each feature has zero-mean and unit variance.")
        standardizer = StandardScaler(copy=False)
        standardizer.fit(dataset)
        dataset = standardizer.transform(dataset)

    if pca_n_components is None:
        pca_n_components = min(dataset.shape[0], dataset.shape[1])
        if verbose:
            print("Setting PCA n_componets to full rank of dataset: {}".format(pca_n_components))
    elif pca_n_components > dataset.shape[1]:
        pca_n_components = dataset.shape[1]
        if verbose:
            print(f"Requesting PCA n_components of {pca_n_components} but the dataset only has {dataset.shape[1]} columns, setting pca_n_components to {dataset.shape[1]}")
    elif pca_n_components > dataset.shape[0]:
        pca_n_components = dataset.shape[0]
        if verbose:
            print(f"Requesting PCA n_components of {pca_n_components} but the dataset only has {dataset.shape[0]} rows, setting pca_n_components to {dataset.shape[0]}")

    if pca_batch_size < pca_n_components:
        if verbose:
            print(f"Adjusting PCA batch size to be at least the number of components '{pca_n_components}'")
        pca_batch_size = pca_n_components

    if verbose:
        print("Reducing the dimension by PCA from {} to {} dimensions".format(dataset.shape[1], pca_n_components))
    pca_reducer = IncrementalPCA(
        n_components=pca_n_components,
        batch_size=pca_batch_size,
        copy=False)
    pca_reducer.fit(dataset)
    pca_embedding = pca_reducer.transform(dataset)

    if verbose:
        print("Reducing the dimension by UMAP to {} dimensions".format(umap_n_components))
    umap_reducer = umap.UMAP(
        n_components=umap_n_components,
        metric=umap_metric,
        n_neighbors=umap_n_neighbors,
        min_dist=umap_min_dist,
        a=umap_a,
        b=umap_b,
        negative_sample_rate=umap_negative_sample_rate,
        init=umap_init,
        low_memory=low_memory,
        random_state=random_state,
        n_epochs=umap_n_epochs,
        verbose=True)
    umap_embedding = umap_reducer.fit_transform(pca_embedding)
    umap_embedding = pd.DataFrame(
        data=umap_embedding,
        columns=["UMAP_" + str(i+1) for i in range(umap_n_components)])
    end_time = time.time()

    if verbose:
        print("created embedding {0} runtime: {1:.2f}s".format(embed_dir, end_time-begin_time))
        print("saving embedding to {}".format(embed_dir))
    with open("{}/model_info.tsv".format(embed_dir), 'w') as f:
        f.write("key\tvalue\n")
        f.write("seed\t{}\n".format(seed))
        f.write("input_dim\t{}\n".format(dataset.shape))
        f.write("standardize_features\t{}\n".format(standardize_features))
        f.write("pca_n_component\t{}\n".format(pca_n_components))
        f.write("umap_n_component\t{}\n".format(umap_n_components))
        f.write("umap_metric\t{}\n".format(umap_metric))
        f.write("umap_n_neighbors\t{}\n".format(umap_n_neighbors))
        f.write("umap_min_dist\t{}\n".format(umap_min_dist))
        f.write("umap_a\t{}\n".format(umap_reducer._a))
        f.write("umap_b\t{}\n".format(umap_reducer._b))
        f.write("umap_negative_sample_rate\t{}\n".format(umap_negative_sample_rate))
        f.write("umap_low_memory\t{}\n".format(low_memory))
        f.write("umap_init\t{}\n".format(umap_init))
        f.write("umap_n_epochs\t{}\n".format(umap_n_epochs))

    pa.parquet.write_table(
        table=pa.Table.from_pandas(umap_embedding),
        where="{}/umap_embedding.parquet".format(embed_dir))

    if save_transform:
        if verbose:
            print("Saving transform to {}.".format(embed_dir))
        if pca_n_components is not None:
            joblib.dump(
                value=pca_reducer,
                filename="{}/pca_reducer.joblib".format(embed_dir))
        if standardize_features:
            joblib.dump(
                value=standardizer,
                filename="{}/standardizer.joblib".format(embed_dir))
        joblib.dump(
            value=umap_reducer,
            filename="{}/umap_reducer.joblib".format(embed_dir))

    return umap_embedding


def embed(
        dataset,
        embed_dir,
        ref_embed_dir,
        standardize_features=None,
        batch_size=None,
        n_epochs=None,
        verbose=True):
    """
    Given a previously defined embedding, embed a new dataset into it
    """

    if not os.path.exists(embed_dir):
        os.mkdir(embed_dir)
    else:
        print("WARNING: embed_dir already exists: {}".format(embed_dir))

    begin_time = time.time()
    if standardize_features:
        if verbose:
            print("Standardizing dataset so each feature has zero-mean and unit variance.")
        standardizer = StandardScaler(copy=False)
        standardizer.fit(dataset)
        dataset = standardizer.transform(dataset)
    elif standardize_features is None:
        if verbose:
            print("Loading standardizer from embed_dir {} ...".format(ref_embed_dir))
        try:
            standardizer = joblib.load(filename="{}/standardizer.joblib".format(ref_embed_dir))
        except:
            standardizer = None
            if verbose:
                print("Standardizer not found at '{}/standardizer.joblib', assume no-prestandardization is needed".format(ref_embed_dir))
    else:
        standardizer = None

    if verbose:
        print("Loading reference PCA->UMAP reducer from embed_dir {} ...".format(ref_embed_dir))
    try:
        pca_reducer = joblib.load(filename="{}/pca_reducer.joblib".format(ref_embed_dir))
    except:
        if verbose:
            print("PCA Reducer not found at '{}/pca_reducer.joblib', assume no pre-dimensionality reduction by PCA".format(ref_embed_dir))
        pca_reducer = None

    umap_reducer = joblib.load(filename="{}/umap_reducer.joblib".format(ref_embed_dir))
    umap_reducer.n_epochs = n_epochs

    if batch_size is None:
        n_batches = 1
    else:
        n_batches = np.floor(dataset.shape[0]/batch_size)
    umap_embedding = []
    for batch_index, batch in enumerate(np.array_split(dataset, n_batches)):
        if verbose:
            print("Transforming batch {} of {}".format(batch_index+1, n_batches))
        if standardizer:
            batch = standardizer.transform(batch)
        if pca_reducer:
            pca_embedding = pca_reducer.transform(batch)
        else:
            pca_embdding = batch
        umap_embedding.append(umap_reducer.transform(pca_embedding))
    umap_embedding = np.vstack(umap_embedding)
    umap_embedding = pd.DataFrame(
        data=umap_embedding,
        columns=["UMAP_" + str(i+1) for i in range(umap_embedding.shape[1])])
    end_time = time.time()
    if verbose:
        print("embedded data onto {0} runtime: {1:.2f}s".format(embed_dir, end_time-begin_time))

    if verbose:
        print("Copying model info from reference embed dir.")

    try:
        shutil.copyfile(
            src="{}/model_info.tsv".format(ref_embed_dir),
            dst="{}/model_info.tsv".format(embed_dir))
    except:
        print("WARNING: Failed to copy reference model info from '{}/model_info.tsv' to '{}/model_info.tsv'".format(ref_embed_dir, embed_dir))

    with open("{}/model_info.tsv".format(embed_dir), 'a') as f:
        f.write("ref_embed_dir\t{}\n".format(ref_embed_dir))
        f.write("n_epochs\t{}\n".format(n_epochs))

    pa.parquet.write_table(
        table=pa.Table.from_pandas(umap_embedding),
        where="{}/umap_embedding.parquet".format(embed_dir))
    return umap_embedding

def save_embedding_plot(
        embedding,
        output_fname,
        inv_color=False,
        color_pallet=viridis,
        background_color="",
        plot_width=400,
        plot_height=400):
    canvas = datashader.Canvas(
        plot_width=plot_width,
        plot_height=plot_height).points(embedding, 'UMAP_1', 'UMAP_2')
    canvas = datashader.transfer_functions.shade(canvas, cmap=color_pallet)
    if (background_color is None) and not inv_color:
        canvas = datashader.transfer_functions.set_background(canvas, background_color)
    canvas.to_pil().convert('RGB').save(output_fname)
