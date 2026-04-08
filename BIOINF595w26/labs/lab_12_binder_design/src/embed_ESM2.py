
import tqdm
import numpy as np
import pandas as pd
import torch
from esm import FastaBatchedDataset, pretrained

def extract_embeddings(
    model_name,
    fasta_file,
    tokens_per_batch = 4096,
    seq_length = 1022,
    repr_layers=[33],
    verbose=False):

    """
    Adapted from https://www.kaggle.com/code/viktorfairuschin/extracting-esm-2-embeddings-from-fasta-files
    """

    if verbose:
        print(f"Embedding {fasta_file} using {model_name} ...")
    
    model, alphabet = pretrained.load_model_and_alphabet(model_name)
    model.eval()

    if torch.cuda.is_available():
        print("Cuda is available")
        model = model.cuda()
    else:
        print("Cuda is not available")
        

    dataset = FastaBatchedDataset.from_file(fasta_file)
    batches = dataset.get_batch_indices(tokens_per_batch, extra_toks_per_seq=1)

    data_loader = torch.utils.data.DataLoader(
        dataset,
        collate_fn=alphabet.get_batch_converter(seq_length),
        batch_sampler=batches)


    ids = []
    embeddings = []

    with torch.no_grad():
        for batch_idx, (labels, strs, toks) in tqdm.tqdm(enumerate(data_loader)):
            if torch.cuda.is_available():
                toks = toks.to(device="cuda", non_blocking=True)

            out = model(toks, repr_layers=repr_layers, return_contacts=False)

            logits = out["logits"].to(device="cpu")
            representations = {
                layer: t.to(device="cpu")
                for layer, t in out["representations"].items()}

            for i, label in enumerate(labels):
                entry_id = label.split()[0]
                truncate_len = min(seq_length, len(strs[i]))

                result = {"entry_id": entry_id}
                result["mean_representations"] = {
                        layer: t[i, 1 : truncate_len + 1].mean(0).clone()
                        for layer, t in representations.items()
                    }
                ids.append(entry_id)
                embeddings.append(result["mean_representations"][33].numpy())

    dataset = pd.DataFrame(
        data = np.stack(embeddings),
        columns = [f"ESM2_{i}" for i in range(len(embeddings[0]))])
    dataset.insert(0, "id", ids)
    
    return dataset

