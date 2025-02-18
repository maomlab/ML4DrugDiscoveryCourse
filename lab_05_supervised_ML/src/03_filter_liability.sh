
# Predict liabilities
# output columns
#   smiles: copy of input SMILES column
#   model: name of the model e.g. 'Firefly Luciferase interference'
#   pred_proba: Probability of the prediction in [0.5, 1]
#   pred: 0/1 Prediction
   
# train
python \
    src/predict_liability.py \
    --infile intermediate_data/data_train_moldata.parquet \
    --outfile intermediate_data/data_train_lp.parquet \
    --models_path src/LiabilityPredictor/LiabilityPredictor/models/assay_inter/ \
    --smiles_col 'SMILES' \
    --verbose

# validation
python \
    src/predict_liability.py \
    --infile intermediate_data/data_validation_moldata.parquet \
    --outfile intermediate_data/data_validation_lp.parquet \
    --models_path src/LiabilityPredictor/LiabilityPredictor/models/assay_inter/ \
    --smiles_col 'SMILES' \
    --verbose

# test
python \
    src/predict_liability.py \
    --infile intermediate_data/data_test_moldata.parquet \
    --outfile intermediate_data/data_test_lp.parquet \
    --models_path src/LiabilityPredictor/LiabilityPredictor/models/assay_inter/ \
    --smiles_col 'SMILES' \
    --verbose

