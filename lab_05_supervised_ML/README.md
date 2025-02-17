
# Supervised Machine Learning

Training supervised machine learning to predict outcomes of PubChem bioactivity screens taking into account assay interference mechanisms

We will leverage MolData, which is a curation of bioactivity data from PubChem

    Keshavarzi Arshadi, A., Salem, M., Firouzbakht, A. et al. MolData, a
    molecular benchmark for disease and target based machine learning. J
    Cheminform 14, 10 (2022). https://doi.org/10.1186/s13321-022-00590-y

and LiabilityPredictor a set of models to predict assay intereference mechanisms.

    Alves VM, Yasgar A, Wellnitz J, Rai G, Rath M, Braga RC, Capuzzi SJ,
    Simeonov A, Muratov EN, Zakharov AV, Tropsha A. Lies and Liabilities:
    Computational Assessment of High-Throughput Screening Hits to Identify
    Artifact Compounds. J Med Chem. 2023 Sep 28;66(18):12828-12839. doi:
    10.1021/acs.jmedchem.3c00482. Epub 2023 Sep 7. PMID: 37677128; PMCID:
    PMC11724736.

featurization from DataMol / molfeat

    datamol-io/molfeat: 0.9.4 (2023)
    https://zenodo.org/records/8373019
    

and H2O an AutoML platform for supervised prediction 

## Learning objectives

Practice a workflow for loading data, training and evaluating machine
learning models, and assessing the results. 

##  Analysis

### Make a local copy of the analysis template

#### Local copy
  If copying from a network drive to somewhere local, E.g. to move it from
  the maomlab turbo to your home directory:

    cd ..
    cp -r lab_04_Simeonov2008_pubchem ~/
    cd ~/lab_04_Simeonov2008_pubchem

#### Download a copy from github
    
    git clone https://github.com/maomlab/ML4DrugDiscoveryCourse


### Set up

### Inspect parameters.yaml and modify for the current analysis
  
    date_code: use the format YYYYMMDD so sorting alphabetically sorts chronologically

    target_AIDs: use for the format "activity_<AID>" from the subset that MolData includes in their curation
    
For template, I've randomly picked three assays

    AID: 1479
    Total Fluorescence Counterscreen for Inhibitors of the Interaction of Thyroid Hormone Receptor and Steroid Receptor Coregulator 2
    Tested Compounds:
       All (276,265)
       Active (806)
       Inactive (272,177)
    
    
    AID: 624291
    qHTS for Activators of Integrin-Mediated Alleviation for Muscular Dystrophy (bioassay)
    Tested Compounds:
       All (345,855)
       Active (222)
       Inactive (331,819)
    
    AID: 1347033
    Human pregnane X receptor (PXR) small molecule agonists: Summary
    Tested Compounds:
       All (7,671)
       Active (1,724)
       Inactive (5,054)


### Install packages
Continuing from the environment set up in lab 4, additionally install h2o and datamol, see `01_install_packages.sh`.


## Run scripts line by line
Notes:
  1) All code should be run from this directory not the 'src' directory
  2) Look at the extension to figure out where to run the code
     * `.sh` -> shell
     * `.R` -> R
     * `.py` -> python

  01) src/01_install_packages.sh
    Install python libraries

  02) src/02_load_data

    Outputs:
      intermediate_data/data_train_moldata.parquet
      intermediate_data/data_validation_moldata.parquet
      intermeidate_data/data_test_moldata.parquet

    Description:
      Download PubChem bioactivity data -> MolData -> HuggingFace
      from `https://huggingface.co/datasets/maomlab/MolData`
      Filter to assays defined in `parameters.yaml`


  03) src/03_filter_liability.sh

    Outputs:
      intermediate_data/data_train_lp.parquet
      intermediate_data/data_validation_lp.parquet      
      intermediate_data/data_test_lp.parquet

    Description:
      Run 6 LiabilityPredictor models over the data

  04) src/04_datamol.py

    Outputs:
      intermediate_data/data_train_features.parquet
      intermediate_data/data_validation_features.parquet
      intermediate_data/data_test_features.parquet

    Descrpition:
      Use molfeat from the DataMol package to compute molecular
      fingerprint features

  05) src/05_join_data.R

    Outputs:
      intermediate_data/data_train.parquet
      intermediate_data/data_validation.parquet
      intermediate_data/data_test.parquet

    Description:
      Join the MolData, LiabilityPredictor, and DataMol together


  06) src/06_predict_outcomes.py

    Outputs:
      intermediate_data/models.pkl
      intermediate_data/data_train_<model>_pred.parquet
      intermediate_data/data_validion_<model>_pred.parquet
      intermediate_data/data_test_<model>_pred.parquet

    Use H2O to predict outcomes based on LiabilityPredictor features
    and DataMol features


  07) src/07_explain_models.py

    Outputs:
      product/<model>_shap_<date_code>.pdf

    Description:
      Use SHAP analysis to assess if LiabilityPredictor features
      are explanatory for the reported outcomes

 
####

Questions:

1) Given an example of a compound that is a hit, in one of the screens that is predicted to be a liability. What fraction of the reported hits are liabilities at the 0.8 probability threshold?

2) For each assay, train a H20 AutoML predictor and evalute using SHAP analysis if any of the liability scores are in the top explanatory features.



