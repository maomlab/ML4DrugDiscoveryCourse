
#######################
# D4 Screening Scores #
#######################
D4_screen <- readr::read_csv(
    "data/D4_screen_table.csv.gz",
    show_col_types = FALSE)

# If the compound fails to dock, then it ends up with a NA value for the score
# but we can assume it is a "very bad" score, so set it to 500
D4_screen <- D4_screen |>
    dplyr::mutate(dockscore = ifelse(is.na(dockscore), 500, dockscore))
   
D4_screen |> arrow::write_parquet(
    "intermediate_data/D4_screen.parquet")

D4_screen_10k <- D4_screen |>
    dplyr::sample_n(size = 10000)
D4_screen_10k |> arrow::write_parquet(
    "intermediate_data/D4_screen_10k.parquet")


D4_screen_100k <- D4_screen |>
    dplyr::sample_n(size = 100000)
D4_screen_100k |> arrow::write_parquet(
    "intermediate_data/D4_screen_100k.parquet")


##########################
# D4 in vitro activities #
##########################

D4_in_vitro <- readr::read_csv(
    "data/D4_in_vitro_data.csv",
    show_col_types = FALSE)

