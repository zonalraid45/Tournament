import os
import nbformat
from kaggle.api.kaggle_api_extended import KaggleApi
import json

NOTEBOOK_FILENAME = "Stockfish321.ipynb"
KERNEL_TITLE = "Stockfish321"
KERNEL_SLUG = "stockfish321"
USERNAME = "utsadassharma"

# Read commands from cmd.txt
with open("cmd.txt", "r") as f:
    cmds = f.read()

# Create notebook with one code cell containing all commands
nb = nbformat.v4.new_notebook()
nb.cells.append(nbformat.v4.new_code_cell(cmds))

with open(NOTEBOOK_FILENAME, "w") as f:
    nbformat.write(nb, f)

# Prepare kernel metadata for Kaggle
metadata = {
    "id": f"{USERNAME}/{KERNEL_SLUG}",
    "title": KERNEL_TITLE,
    "code_file": NOTEBOOK_FILENAME,
    "language": "python",
    "kernel_type": "notebook",
    "is_private": "true"
}
with open("kernel-metadata.json", "w") as f:
    json.dump(metadata, f)

# Push notebook to Kaggle and execute it
api = KaggleApi()
api.authenticate()
api.kernels_push_kernel(path=".")

# Start notebook execution (automated run on Kaggle)
api.kernels_start_kernel(f"{USERNAME}/{KERNEL_SLUG}")

print(f"Notebook pushed and executed: https://www.kaggle.com/code/{USERNAME}/{KERNEL_SLUG}")
