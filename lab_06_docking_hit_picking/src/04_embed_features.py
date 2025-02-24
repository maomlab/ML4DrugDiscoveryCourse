

import numpy as np
from embedding import fit_embedding, save_embedding_plot

import yaml

with open("parameters.yaml") as parameters_file:
    parameters = yaml.safe_load(parameters_file)

D4_screen_10k_features_ecfp = np.load("intermediate_data/D4_screen_10k_features_ecfp.npy")    
D4_screen_100k_features_ecfp = np.load("intermediate_data/D4_screen_100k_features_ecfp.npy")
D4_in_vitro_features_ecfp = np.load("intermediate_data/D4_in_vitro_features_ecfp.npy")

D4_screen_10k_features_unimol2 = np.load("intermediate_data/D4_screen_10k_features_unimol2.npy")    
D4_screen_100k_features_unimol2 = np.load("intermediate_data/D4_screen_100k_features_unimol2.npy")
D4_in_vitro_features_unimol2 = np.load("intermediate_data/D4_in_vitro_features_unimol2.npy")

#################
# ECFP Features #
#################

'''
embedding_tag = "screen_10k_in_vitro_ecfp_euclidean"
dataset = np.vstack([
    D4_screen_10k_features_ecfp,
    D4_in_vitro_features_ecfp])
embedding = fit_embedding(
    dataset = dataset,
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)

embedding_tag = "screen_100k_in_vitro_ecfp_cosine"
dataset = np.vstack([
    D4_screen_100k_features_ecfp,
    D4_in_vitro_features_ecfp])
embedding = fit_embedding(
    dataset = dataset,
    umap_metric = 'cosine',
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)



embedding_tag = "screen_100k_in_vitro_ecfp_pca30_euclidean"
dataset = np.vstack([
    D4_screen_100k_features_ecfp,
    D4_in_vitro_features_ecfp])
embedding = fit_embedding(
    dataset = dataset,
    pca_n_components = 30,
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)

embedding_tag = "screen_100k_in_vitro_ecfp_pca30_cosine"
dataset = np.vstack([
    D4_screen_100k_features_ecfp,
    D4_in_vitro_features_ecfp])
embedding = fit_embedding(
    dataset = dataset,
    pca_n_components = 30,
    umap_metric = 'cosine',
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)


#########################
# 10k Uni-Mol2 features #
#########################

embedding_tag = "screen_10k_in_vitro_unimol2_euclidean"
dataset = np.vstack([
    D4_screen_10k_features_unimol2,
    D4_in_vitro_features_unimol2])
embedding = fit_embedding(
    dataset = dataset,
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)

embedding_tag = "screen_10k_in_vitro_unimol2_cosine"
dataset = np.vstack([
    D4_screen_10k_features_unimol2,
    D4_in_vitro_features_unimol2])
embedding = fit_embedding(
    dataset = dataset,
    umap_metric = 'cosine',    
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)


embedding_tag = "screen_10k_in_vitro_unimol2_pca30_euclidean"
dataset = np.vstack([
    D4_screen_10k_features_unimol2,
    D4_in_vitro_features_unimol2])
embedding = fit_embedding(
    dataset = dataset,
    pca_n_components = 30,   
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)

embedding_tag = "screen_10k_in_vitro_unimol2_pca30_cosine"
dataset = np.vstack([
    D4_screen_10k_features_unimol2,
    D4_in_vitro_features_unimol2])
embedding = fit_embedding(
    dataset = dataset,
    pca_n_components = 30,
    umap_metric = 'cosine',    
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)



##########################
# 100k Uni-Mol2 features #
##########################
dataset = np.vstack([
    D4_screen_100k_features_unimol2,
    D4_in_vitro_features_unimol2])

embedding_tag = "screen_100k_in_vitro_unimol2_euclidean"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)

embedding_tag = "screen_100k_in_vitro_unimol2_cosine"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,    
    umap_metric = 'cosine',    
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)


embedding_tag = "screen_100k_in_vitro_unimol2_pca30_euclidean"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,    
    pca_n_components = 30,   
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)

embedding_tag = "screen_100k_in_vitro_unimol2_pca30_cosine"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,    
    pca_n_components = 30,
    umap_metric = 'cosine',    
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)
'''


# Add lines to generate six embedding files that have not been generated yet
embedding_tag = "screen_10k_in_vitro_ecfp_pca30_euclidean"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,    
    pca_n_components = 30,   
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)


embedding_tag = "screen_10k_in_vitro_ecfp_cosine"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,    
    pca_n_components = 30,
    umap_metric = 'cosine',    
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)


embedding_tag = "screen_10k_in_vitro_ecfp_pca30_cosine"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,    
    pca_n_components = 30,
    umap_metric = 'cosine',    
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)


embedding_tag = "screen_100k_in_vitro_ecfp_cosine"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,    
    pca_n_components = 30,
    umap_metric = 'cosine',    
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)


embedding_tag = "screen_100k_in_vitro_unimol2_euclidean"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,    
    pca_n_components = 30,   
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)


embedding_tag = "screen_100k_in_vitro_unimol2_pca30_euclidean"
embedding = fit_embedding(
    dataset = dataset,
    standardize_features = False,    
    pca_n_components = 30,   
    embed_dir = f"intermediate_data/embedding_{embedding_tag}")
save_embedding_plot(
    embedding = embedding,
    output_fname = f"product/embedding_{embedding_tag}_{parameters['date_code']}.png",
    plot_width = 600,
    plot_height = 600)    