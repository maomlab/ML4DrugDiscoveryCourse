
# Fluorescence Spectroscopic Profiling of Compound Libraries
# Anton Simeonov, Ajit Jadhav, Craig J. Thomas, Yuhong Wang, Ruili
# Huang, Noel T. Southall, Paul Shinn, Jeremy Smith, ChristopOBher
# P. Austin, Douglas S. Auld, and James Inglese*
# Cite this: J. Med. Chem. 2008, 51, 8, 2363–2371
# Publication Date:March 26, 2008
# https://doi.org/10.1021/jm701301m

pubchem_bioactivities <- arrow::read_parquet(
    file = "intermediate_data/pubchem/pubchem_bioactivities.parquet")

Simeonov2008 <- pubchem_bioactivities |>
    dplyr::filter(
        AID %in% c(587, 588, 590, 591, 592, 593, 594)) |>
    dplyr::filter(`Activity Outcome` == "Active") |>
    dplyr::filter(!is.na(CID))
# 7152

# The full database of all pubchem compounds is very large, so
# instead we'll use the list of CIDs to look up SMILES from pubchem website

Simeonov2008 |>
    dplyr::select(CID) |>
    readr::write_tsv(
        file = "intermediate_data/Simeonov2008_CIDs.tsv",
        col_names = FALSE)



Simeonov2008_smi <- readr::read_tsv(
    file = "intermediate_data/Simeonov2008_pubchem.smi",
    col_names = c("smiles", "CID"),
    show_col_types = FALSE)

Simeonov2008 <- Simeonov2008 |>
    dplyr::inner_join(
        Simeonov2008_smi,
        by = "CID")


Simeonov2008 <- Simeonov2008 |>
    dplyr::distinct()


Simeonov2008 |>
    dplyr::rename(screen_aid = AID) |>   
    dplyr::group_by(CID) |>
    dplyr::summarize(
        smiles = smiles[1],
        .groups = "drop") |>
    readr::write_tsv(
        file = "intermediate_data/Simeonov2008_compounds.tsv")
