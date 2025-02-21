
# Docking Hit Picking

Investigating representing chemical space for large-scale virtual screening


we will leverage data from lsd.docking.org/

    Jiankun Lyu, Sheng Wang, Trent E. Balius, Isha Singh, Anat Levit,
    Yurii S. Moroz, Matthew J. O’Meara, Tao Che, Enkhjargal Algaa,
    Kateryna Tolmachova, Andrey A. Tolmachev, Brian K. Shoichet, Bryan
    L. Roth & John J. Irwin (2019). Ultra-large library docking for
    discovering new chemotypes. Nature, 566(7743), 224-229.


representations from Uni-Mol2


    Uni-Mol2: Exploring Molecular Pretraining Model at Scale
    Xiaohong Ji, Zhen Wang, Zhifeng Gao, Hang Zheng, Linfeng Zhang, Guolin Ke, Weinan E
    2024, https://arxiv.org/abs/2406.14969


visualizaiton through UMAP


    UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction
    Leland McInnes, John Healy, James Melville
    2018, https://arxiv.org/abs/1802.03426


## Learning objectives

 * Learn how to use the GPU cluster queue
 * use Uni-mol2 embeddings
 * visualize chemical space using UMAP and clustering
 

## Notes

* To use the gpu on great lakes set `--partition=gpu` and add `--gres=gpu:1` to srun:

    srun --verbose --nodes=1 --cpus-per-task=5 --account=maom99 --partition=gpu --gres=gpu:1 --mem-per-cpu=30GB --time 04:00:00 --pty /bin/bash -li

* Run the molecule_embedding.ipynb in the great-lakes Jupyter Lab web instance from https://greatlakes.arc-ts.umich.edu

* Note that computing the Uni-Mol2 features may take 3-5 hours to run. The results are already in the intermediate data directory if you have trouble doing this.

* The zipped downloaded screen data is ~ 1.8G, converted into the parquet file is ~3.1G

### Questions


1) How are the ECFP and Uni-Mol2 representations similar or different? Consider
    a) What aspects of the molecule are considered?
    b) How might the training data/task for Uni-Mol2 affect the representation?
    c) What are the dimensions of the representations?
    d) How clumpy/smooth are they and how can this be evaluated?

2) For the embeddings
     a) How does preprocessing the data with PCA or using different kernel (euclidean vs. cosine) work?
     b) How does this affect the resulting embeddings?
     c) Using the molecule_embedding.ipynb app, Can you find examples compounds that are close together in the embedding that look chemically similar or chemically very different?

3) For the D4 screen and in vitro data
     a) Do the representations lead a local enrichment of
            a) Heavy atom count
            b) Componds tested vs. not tested
	    c) Binder vs not Binder
     
   



