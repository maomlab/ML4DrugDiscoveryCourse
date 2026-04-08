# Binder Design
In this lab you will analyze proteins designed to bind small molecules. 





### Learning Objectives

  * Better understand the use of molecular foundation models can work together for protein design
  
  
### References

  * Stark, H, et al., BoltzGen: Toward Universal Binder Design
    https://doi.org/10.1101/2025.11.20.689494
  
## Steps

### 2 Run BoltzGen to design binders to a small molecule ligand

Follow the instructions on the [BoltzGen Github](https://github.com/HannesStark/boltzgen) to sample 3-5
proteins designed to bind to a small molecule of your choice.

This should take ~1 minute per sample, and can be run interactively on a GPU node on the cluster
In a production run, the recomendation is to generate 10,000-60,000 samples using SLURM to distribute
the jobs into e.g. 10-60 tasks of 1000 samples each. For the sake of time, we'll just generate a few example
samples to see how it works, and then use pre-generated samples in the next step.


  * Install BoltzGen with `pip install boltzgen`
  * Create `$LAB_PATH/intermediate/$RUN_ID/spec.yaml` where `$LAB_PATH` is the path to the lab directory
    `$RUN_ID` is e.g. the name of the small molecule and `$SMILES` is the smiles for the small molecule

        entities:
          # Designed protein with between 80 and 140 residues 
          # (The length is randomly sampled)
          - protein: 
            id: B
            sequence: 80..140

          - ligand:
            id: A
            smiles: '$SMILES'

   * Run `boltzgen run` to generate a few sample designs
   
          boltzgen run "intermediate/$RUN_ID/spec.yaml" \
            --output "$LAB_PATH/intermediate/$RUN_ID/merged/task-outputs" \
            --num_designs 5 \
		    --protocol protein-small_molecule \
		    --cache $LAB_PATH/.cache \
		    --reuse
		  
### 3 Inspect the pre-computed final designs
In `$LAB_PATH/intermediate` on github there are the final results for
designing binders to 4 target mu opioid receptor ligands

  * Inspect the
    `$LAB_PATH/intermediate/$RUN_ID/merged/final_ranked_designs/results_overview.pdf`
    for the four target ligands.
	* What was the most stringent filtering criteria?
	* Do you notice any big differences in between the targets?
	Is the predicted quality of the designs high, are there enough samples?
	
  * Open the all the final designs for one of the target ligands in pymol and inspect the diversity of the designs
    you can use the `extra_fit resn LIG1` command to align all the designed structures on the ligand.
	* Are there common folds (e.g. helical bundles)?
	* How similar are the interactions with the ligand, do you see any highly similar designs?
	* Pick a design that you like and show generate a high-quality ray traced view of the interaction

  * Are the designs similar to any existing proteins? From PyMOL you can generate a fasta file of the
    designs with `save /tmp/output.fasta, all`. Then run this in through [BlastP](https://blast.ncbi.nlm.nih.gov/Blast.cgi).
	For the design that you picked, run the `.cif` file through [FoldSeek](https://search.foldseek.com/search).
	Are there any significant hits?
	
### 4 Cross Dock the target ligands
Use Boltz-2 each of the four target ligands into each of the 30 designs for each ligand, so 30 * 4 total docking runs.

  * Follow a similar protocol as for lab 11 for how to setup and run Boltz-2. The sequences for each designs obtained from `final_designs_metrics_30.csv`. Be sure to compute the affinity, e.g. in the `spec.yaml` for Boltz-2,
  
        sequences:
          - protein:
            id: A
            sequence: $DESIGN_SEQUENCE
          - ligand:
            id: B
            smiles: '$SMILES'
        properties:
          - affinity:
            binder: B
  
  * Collate receptor/ligand docking results into a summary table getting receptor metadata from `final_designs_metrics_30.csv` and the Boltz-2 results from `affinity_$COMPLEX_ID.json` for the receptor/ligand pair. Specifically, create table with columns 
	* receptor_id
	* ligand_id
	* receptor_design_ligand_id
	* receptor_design_rank
	* receptor_design_design_to_target_iptm
	* receptor_design_min_design_to_target_pae
    * boltz2_affinity_probability_binary
	* boltz2_affinity_pred_value
  * As array of scatter plots for each pair of ligands comparing the affinity probability binary
    all the designs for one ligand vs. the other, coloring the designs by the ligand that it was
	designed to bind. Do you see any patterns of off-target activities between designs for different ligands?
	
### 5 Cluter designs by sequence and structure
For the sake of time, this step is optional. If you don't do it briefly describe what you would do, and the hypotheses
questions you would consider.

  * To cluster by sequence, for each design compute ESM-2 embeddings for each sequence and use UMAP to visualize. You can use the `src/embed_ESM2.py` script.
  * To cluster by structure, for each designed compute PLIP interaction fingerprints between the receptor and the ligand summing interactions for each interaction type over all residues.
  * Do you see clustering across folds or designed ligand targets?

  
