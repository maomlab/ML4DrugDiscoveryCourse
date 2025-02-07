
# Analysis workflow to curate autofluorescence data from (Simeonov 2008)

## Goal of the lab:
Curate data from PubChem and create a hugging face dataset ready for machine learning. The dataset comes from

  Simeonov A, Jadhav A, Thomas CJ, Wang Y, Huang R, Southall NT, Shinn P, Smith J, Austin CP, Auld DS, Inglese J.
  Fluorescence spectroscopic profiling of compound libraries.
  J Med Chem. 2008 Apr 24;51(8):2363-71. DOI: 10.1021/jm701301m. Epub 2008 Mar 26. PMID: 18363325.

Abstract:

  Chromo/fluorophoric properties often accompany the heterocyclic
  scaffolds and impurities that comprise libraries used for
  high-throughput screening (HTS). These properties affect assay outputs
  obtained with optical detection, thus complicating analysis and
  leading to false positives and negatives. Here, we report the
  fluorescence profile of more than 70,000 samples across spectral
  regions commonly utilized in HTS. The quantitative HTS paradigm was
  utilized to test each sample at seven or more concentrations over a
  4-log range in 1,536-well format. Raw fluorescence was compared with
  fluorophore standards to compute a normalized response as a function
  of concentration and spectral region. More than 5% of library members
  were brighter than the equivalent of 10 nM 4-methyl umbelliferone, a
  common UV-active probe. Red-shifting the spectral window by as little
  as 100 nm was accompanied by a dramatic decrease in
  autofluorescence. Native compound fluorescence, fluorescent
  impurities, novel fluorescent compounds, and the utilization of
  fluorescence profiling data are discussed.


Key learning objectives:
 1) Login and set up Great-lakes environment
 2) Developing a data analysis workflow
 3) Practice working with large-scale data from PubChem
 4) Data exploratory data analysis with R
 5) Creation of HuggingFace datasets


## Analysis:



### Make a copy of the analysis template
To do the analysis you need to have a local version of it.

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
  huggingface_repo: path to HuggingFace Database e.g. for "https://huggingface.co/datasets/maom/Simeonov2008"
    use "maom/Simeonov2008"


Note: All code should be run from this directory not the 'src' directory

## Run scripts line by line

  00.1) src/00.1_install_R_libraries.R
     Install R packages

  00.2) src/00.2_install_python_packages.py
     Install python libraries

  1) src/01_load_data_from_pubchem.R
     Outputs:
       intermediate_data/pubchem/pubchem_bioactivities.parquet
       intermediate_data/pubchem/pubchem_bioassays.parquet    
       intermediate_data/pubchem/pubchem_same_project.parquet 
       
     Description:
       Using wget, download same_project, bioassays, and bioactivities data from ftp.ncbi.nlm.nih.gov
       
   2) src/02_load_Simeonov2008.R
      Outputs:
        intermediate_data/Simeonov2008_CIDs.tsv
	intermediate_data/Simeonov2008_compounds.tsv
	intermediate_data/Simeonov2008_pubchem.smi
	
      Description:
        Filter and join just the active compounds together. Since the full set of pubchem structures
	is very large, in this script we will interactively use the web-interface to look up the ones
	we need for this study.

    3) src/03_sanitize_molecules.py
       Outputs:
         product/Simeonov2008_compounds_sanitized_{date_code}.tsv

       Description:
         Use MolVS to santitize molecules


    4) src/upload_to_hf.py
       Output:
          Adds data to the HuggingFace Repository specified in parameters.yaml

       Description:
          After creating a huggingface.co dataset, push data.
	  See https://docs.google.com/document/d/16E6D06eT18Qb7eDpnTjW6MQXhuq55DkTdTU2YWA7XaI/edit?usp=sharing
	  for a detailed guide on creating HuggingFace datasets
