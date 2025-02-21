
D4_screen_100k <- arrow::read_parquet("intermediate_data/D4_screen_100k.parquet")
D4_in_vitro <- readr::read_csv("data/D4_in_vitro_data.csv",show_col_types = FALSE)


embedding_tag <- "screen_100k_in_vitro_unimol2_cosine"
embedding_label <- "UMAP Embedding of D4 screen 100k and in vitro cosine"

clusters <- arrow::read_parquet(
    paste0("intermediate_data/embedding_", embedding_tag, "/clusters.parquet"))
embedding <- arrow::read_parquet(
    paste0("intermediate_data/embedding_", embedding_tag, "/umap_embedding.parquet"))

        
data <- D4_screen_100k |>
    dplyr::mutate(binder = NA) |>
    dplyr::bind_rows(
        D4_in_vitro |>
        dplyr::select(
            zincid,
            smiles,
            dockscore = score,
            hac,
            binder = Binder))
data <- data |>
    dplyr::bind_cols(clusters) |>
    dplyr::bind_cols(embedding)


plot <- ggplot2::ggplot() +
    ggplot2::theme_bw() +
    ggplot2::ggtitle(embedding_label) +
    ggrastr::rasterize(
        ggplot2::geom_point(
            data = data,
            mapping = ggplot2::aes(
                x = UMAP_1,
                y = UMAP_2,
                color = hac),
            alpha = 0.3,
            size = 0.2,
            shape = 16),
        dpi = 800) +
    ggplot2::geom_point(
        data = data |>
            dplyr::filter(
                !is.na(binder),
                binder == 0),
        mapping = ggplot2::aes(
            x = UMAP_1,
            y = UMAP_2),
        color = "brown",
        size = 1,
        shape = 16) +
    ggplot2::geom_point(
        data = data |>
            dplyr::filter(
                !is.na(binder),
                binder == 1),
        mapping = ggplot2::aes(
            x = UMAP_1,
            y = UMAP_2),
        color = "darkblue",
        size = 1,
        shape = 16) +
    ggplot2::coord_fixed() +
    viridis::scale_color_viridis("Heavy Atom Count") +
    ggplot2::theme(legend.position = "bottom")

ggplot2::ggsave(
    filename = paste0("product/embedding_", embedding_tag, "_hac_binder.pdf"),
    width = 10,
    height = 10,
    useDingbats = FALSE)
