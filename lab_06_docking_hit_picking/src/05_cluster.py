
from cluster import cluster_leiden

#cluster_leiden("screen_10k_in_vitro_ecfp_euclidean") 
cluster_leiden("screen_10k_in_vitro_ecfp_pca30_euclidean")
cluster_leiden("screen_10k_in_vitro_ecfp_cosine")
cluster_leiden("screen_10k_in_vitro_ecfp_pca30_cosine")

#cluster_leiden("screen_100k_in_vitro_ecfp_euclidean")
#cluster_leiden("screen_100k_in_vitro_ecfp_pca30_euclidean")
cluster_leiden("screen_100k_in_vitro_ecfp_cosine")
#cluster_leiden("screen_100k_in_vitro_ecfp_pca30_cosine")


#cluster_leiden("screen_10k_in_vitro_unimol2_euclidean")
#cluster_leiden("screen_10k_in_vitro_unimol2_pca30_euclidean")
#cluster_leiden("screen_10k_in_vitro_unimol2_cosine")
#cluster_leiden("screen_10k_in_vitro_unimol2_pca30_cosine")

cluster_leiden("screen_100k_in_vitro_unimol2_euclidean")
cluster_leiden("screen_100k_in_vitro_unimol2_pca30_euclidean")
#cluster_leiden("screen_100k_in_vitro_unimol2_cosine")
#cluster_leiden("screen_100k_in_vitro_unimol2_pca30_cosine")
