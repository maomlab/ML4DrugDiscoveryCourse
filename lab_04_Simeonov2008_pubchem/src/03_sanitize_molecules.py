


import rdkit
import pandas as pd
import molvs
import yaml

with open("parameters.yaml") as parameters_file:
    parameters = yaml.safe_load(parameters_file)

data = pd.read_csv(
    filepath_or_buffer = "intermediate_data/Simeonov2008_compounds.tsv",
    sep = "\t")

standardizer = molvs.Standardizer()
fragment_remover = molvs.fragment.FragmentRemover()

def sanitize_smiles(smiles_raw):
    mol = rdkit.Chem.MolFromSmiles(smiles_raw)
    mol = standardizer.standardize(mol)
    mol = fragment_remover.remove(mol)
    smiles = rdkit.Chem.MolToSmiles(mol)
    return smiles

data['smiles'] = data['smiles'].apply(sanitize_smiles)

data.to_csv(
    path_or_buf = f"product/Simeonov2008_compounds_sanitized_{parameters["date_code"]}.tsv",
    sep = "\t",
    index = False)
