
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
 

## Steps

To use the gpu on great lakes set `--partition=gpu` and add `--gres=gpu:1` to srun:

    srun --verbose --nodes=1 --cpus-per-task=5 --account=maom99 --partition=gpu --gres=gpu:1 --mem-per-cpu=30GB --time 04:00:00 --pty /bin/bash -li


