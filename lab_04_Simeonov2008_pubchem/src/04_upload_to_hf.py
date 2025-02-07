
import datasets
import yaml

with open("parameters.yaml") as parameters_file:
    parameters = yaml.safe_load(parameters_file)


dataset = datasets.load_dataset(
    "csv",
    data_files = f"product/Simeonov2008_compounds_sanitized_{parameters["date_code"]}.tsv",
    keep_in_memory = True,
    sep = "\t")

print(f"Pushing to {parameters["huggingface_repo"]}")
dataset.push_to_hub(
    repo_id = parameters["huggingface_repo"])

