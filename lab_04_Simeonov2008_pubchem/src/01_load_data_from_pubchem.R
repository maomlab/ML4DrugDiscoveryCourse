#!/usr/bin Rscript

library(httr)
library(arrow)

# where we'll download the data to
if (!dir.exists("data/pubchem")) {
   cat("Creating 'data/pubchem'\n")
   dir.create("data/pubchem", recursive = TRUE)
}

# where we'll write out the loaded data
if (!dir.exists("intermediate_data/pubchem")) {
   cat("Creating 'intermediate_data/pubchem'\n")
   dir.create("intermediate_data/pubchem", recursive = TRUE)
}


########################
# PubChem same project #
########################
# This table links assays within the same project

cat("Downloading same_project data from PubChem ...\n")
system(paste0(
  "cd data/pubchem && ",
  "wget https://ftp.ncbi.nlm.nih.gov/pubchem/Bioassay/AssayNeighbors/",
  "pcassay_pcassay_same_assay_project.gz"))

pubchem_same_project <- readr::read_tsv(
    "data/pubchem/pcassay_pcassay_same_assay_project.gz",
    col_names = c("aid_id_1", "aid_id_2"),
    show_col_types = FALSE) |>
    dplyr::mutate(
        aid_id_1 = aid_id_1 |>
            stringr::str_replace("AID", "") |>
            as.numeric(),
        aid_id_2 = aid_id_2 |>
            stringr::str_replace("AID", "") |>
            as.numeric())    

pubchem_same_project |>
    arrow::write_parquet("intermediate_data/pubchem/pubchem_same_project.parquet")

#####################
# PubPhem Bioassays #
#####################
cat("Downloading bioassays data from PubChem (42M) ...\n")
system(paste0(
  "cd data/pubchem && ",
  "wget https://ftp.ncbi.nlm.nih.gov/pubchem/Bioassay/Extras/bioassays.tsv.gz"))

pubchem_bioassays <- readr::read_tsv(
  "data/pubchem/bioassays.tsv.gz",
  show_col_types = FALSE)

pubchem_bioassays <- pubchem_bioassays |>
  dplyr::mutate(
    source_name_label = dplyr::case_when(
      `Source Name` == "ChEMBL" ~ "ChEMBL",
      `Source Name` == "BindingDB" ~ "BindingDB",
      `Source Name` == "IUPHAR/BPS Guide to PHARMACOLOGY" ~ "IUPHAR/BPS",
      `Source Name` == 
        "National Center for Advancing Translational Sciences (NCATS)" ~
        "NCATS",
      `Source Name` ==
        "The Scripps Research Institute Molecular Screening Center" ~
        "Scripps",
      `Source Name` == "Broad Institute" ~ "Broad",
      `Source Name` == "Burnham Center for Chemical Genomics" ~ "BCCC",
      `Source Name` == "NMMLSC" ~ "NMMLSC",
      TRUE ~ "other"),
    assay_type = ifelse(
      source_name_label %in% c("ChEMBL", "IUPHAR/BPS", "BindingDB"),
      "Literature",
      "Screen"),
    is_toxicity = ifelse(
        is.na(`BioAssay Types`),
        FALSE,
        `BioAssay Types` |> stringr::str_detect("Toxicity")))

pubchem_bioassays |>
    arrow::write_parquet("intermediate_data/pubchem/pubchem_bioassays.parquet")

#########################
# PubChem Bioactivities #
#########################

cat("Downloading bioactivities data from PubChem (2.8G) ...\n")
system(paste0(
  "cd data/pubchem && ",
  "wget https://ftp.ncbi.nlm.nih.gov/pubchem/Bioassay/Extras/",
  "bioactivities.tsv.gz"))

pubchem_bioactivities <- readr::read_tsv(
  "data/pubchem/bioactivities.tsv.gz",
  show_col_types = FALSE)

pubchem_bioactivities |>
  arrow::write_parquet("intermediate_data/pubchem/pubchem_bioactivities.parquet")
