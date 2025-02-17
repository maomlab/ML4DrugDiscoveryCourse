
### Train
data_train_moldata <- arrow::read_parquet(
   "intermediate_data/data_train_moldata.parquet")
data_train_lp <- arrow::read_parquet(
   "intermediate_data/data_train_lp.parquet")
data_train_features <- arrow::read_parquet(
   "intermediate_data/data_train_features.parquet")


data_train_lp_wide <- data_train_lp |>
   dplyr::mutate(
     pred_score = ifelse(pred, pred_proba, 1 - pred_proba)) |>
   dplyr::distinct(smiles, model, .keep_all = TRUE) |>
   dplyr::select(
     SMILES = smiles, model, pred_score) |>
   tidyr::pivot_wider(
     id_cols = SMILES,
     names_from = model,
     values_from = pred_score)

names(data_train_features) <- paste0(
  "feature_", names(data_train_features))


data_train <- data_train_moldata |>
   dplyr::left_join(
     data_train_lp_wide,
     by = "SMILES") |>
   dplyr::mutate(
     dplyr::across(
       dplyr::everything(),
       ~tidyr::replace_na(.x, 0))) |>
   dplyr::bind_cols(
     data_train_features) 

data_train |>
  arrow::write_parquet(
    "intermediate_data/data_train.parquet")


#### Validation

data_validation_moldata <- arrow::read_parquet(
   "intermediate_data/data_validation_moldata.parquet")
data_validation_lp <- arrow::read_parquet(
   "intermediate_data/data_validation_lp.parquet")
data_validation_features <- arrow::read_parquet(
   "intermediate_data/data_validation_features.parquet")


data_validation_lp_wide <- data_validation_lp |>
   dplyr::mutate(
     pred_score = ifelse(pred, pred_proba, 1 - pred_proba)) |>
   dplyr::distinct(smiles, model, .keep_all = TRUE) |>
   dplyr::select(
     SMILES = smiles, model, pred_score) |>
   tidyr::pivot_wider(
     id_cols = SMILES,
     names_from = model,
     values_from = pred_score)

names(data_validation_features) <- paste0(
  "feature_", names(data_validation_features))


data_validation <- data_validation_moldata |>
   dplyr::left_join(
     data_validation_lp_wide,
     by = "SMILES") |>
   dplyr::mutate(
     dplyr::across(
       dplyr::everything(),
       ~tidyr::replace_na(.x, 0))) |>
   dplyr::bind_cols(
     data_validation_features) 

data_validation |>
  arrow::write_parquet(
    "intermediate_data/data_validation.parquet")


### Test

data_test_moldata <- arrow::read_parquet(
   "intermediate_data/data_test_moldata.parquet")
data_test_lp <- arrow::read_parquet(
   "intermediate_data/data_test_lp.parquet")
data_test_features <- arrow::read_parquet(
   "intermediate_data/data_test_features.parquet")


data_test_lp_wide <- data_test_lp |>
   dplyr::mutate(
     pred_score = ifelse(pred, pred_proba, 1 - pred_proba)) |>
   dplyr::distinct(smiles, model, .keep_all = TRUE) |>
   dplyr::select(
     SMILES = smiles, model, pred_score) |>
   tidyr::pivot_wider(
     id_cols = SMILES,
     names_from = model,
     values_from = pred_score)

names(data_test_features) <- paste0(
  "feature_", names(data_test_features))


data_test <- data_test_moldata |>
   dplyr::left_join(
     data_test_lp_wide,
     by = "SMILES") |>
   dplyr::mutate(
     dplyr::across(
       dplyr::everything(),
       ~tidyr::replace_na(.x, 0))) |>
   dplyr::bind_cols(
     data_test_features) 

data_test |>
  arrow::write_parquet(
    "intermediate_data/data_test.parquet")

