from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import SimilarityMaps
from scipy.spatial.distance import cdist
import numpy as np

import warnings
import glob
import os
import pickle
import io
import matplotlib.pyplot as plt

import pandas as pd

import pyarrow as pa
import pyarrow.parquet as pq



MODEL_DICT = {
    'Firefly_Luciferase_counter_assay_training_set_curated_model.pkl': 'Firefly Luciferase interference',
    'Nano_Luciferase_counter_assay_training_set_curated_model.pkl': 'Nano Luciferase interference',
    'Redox_training_set_curated_model.pkl': 'Redox interference',
    'Thiol_training_set_curated_model.pkl': 'Thiol interference',
    'agg_betalac_model.pkl': 'AmpC β-lactamase aggregation',
    'agg_cruzain_model.pkl': 'Cysteine protease cruzain aggregation'
}

if __name__ == "__main__":
    import argparse
    import csv
    from io import StringIO
    from rdkit.Chem import MolFromSmiles
    from tqdm import tqdm

    parser = argparse.ArgumentParser()
    parser.add_argument("--models_path", type=str, required=True,
                        help="folder with model .pkl files")
    parser.add_argument("--infile", type=str, required=True,
                        help="location to csv of SMILES")
    parser.add_argument("--outfile", type=str, default=os.path.join(os.getcwd(), "liability_output.csv"),
                        help="location and file name for output")
    parser.add_argument("--smiles_col", type=str, default="SMILES",
                        help="column name containing SMILES of interest"),
    parser.add_argument("--verbose", action="store_true",
                        help="verbose logging")

    args = parser.parse_args()

    if not os.path.exists(args.infile):
        warnings.warn(f"Input path '{args.infile}' doesn't exist.")
    else:
        if args.verbose:
            print(f"Reading from '{args.infile}'")

    if os.path.exists(args.outfile):
        warnings.warn(f"Output path '{args.infile}' already exist.")
    else:
        if args.verbose:
            print(f"Writing to '{args.infile}'")
            

    if args.infile.endswith(".csv"): 
        smiles_list = pd.read_csv(args.infile)[args.smiles_col].to_list()
    elif args.infile.endswith(".parquet"):
        smiles_list = pq.read_table(args.infile).to_pandas()[args.smiles_col].to_list()
    else:
        warnings.warn(f"Unrecognized input file type '{args.infile}'")

    if args.verbose:
        print(f"Computing Liability scores for {len(smiles_list)} compounds.")
    
    if args.verbose:
        print(f"Loading models {len(MODEL_DICT)} models...")
        
    models = {}
    for model_fname, model_name in MODEL_DICT.items():
        model_path = os.path.join(args.models_path, model_fname)
        with open(model_path, 'rb') as f:
            model = pickle.load(f)        
        models[model_name] = model

    if args.verbose:
        print(f"computing Liability scores for {len(models.keys())} models")

    values = []
    for index, smiles in enumerate(tqdm(smiles_list)):
        molecule = MolFromSmiles(smiles)
        if molecule is None:
            if args.verbose:
                print(f"Failed to parse {index} molecule with smiles '{smiles}'")
            continue
                
        fp = np.zeros((2048, 1))
        _fp = AllChem.GetMorganFingerprintAsBitVect(
            molecule, radius=3, nBits=2048)
        DataStructs.ConvertToNumpyArray(_fp, fp)

        for model_name, model in models.items():
            pred_proba = model.predict_proba(fp.reshape(1, -1))[:, 1]
            pred = 1 if pred_proba > 0.5 else 0

            if pred == 0:
                pred_proba = 1-pred_proba
            values.append({
                'smiles': smiles,                
                'model': model_name,
                'pred_proba' : pred_proba[0],
                'pred' : pred})
    
    values = pd.DataFrame(values)

    if args.outfile.endswith(".csv"):
        values.to_csv(args.outfile, index = False)
    elif args.outfile.endswith(".parquet"):
        pq.write_table(
            pa.Table.from_pandas(values),
            args.outfile)
