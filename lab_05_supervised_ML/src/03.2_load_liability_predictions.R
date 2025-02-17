

data_train_small <- readr::read_csv(
  "intermediate_data/data_train_small.csv",
  show_col_types = FALSE)
  
data_train_small_lp <- readr::read_csv(
  "intermediate_data/data_train_small_lp.csv",
  show_col_types = FALSE)
	
data_train_small_false_positives_pred <- data_train_small |>
  dplyr::filter(Y == 1) |>
  dplyr::inner_join(
    data_train_small_lp |>
      dplyr::filter(pred == 1) |>
      dplyr::filter(pred_proba > 0.8),
    by = c("SMILES" = "smiles"))



