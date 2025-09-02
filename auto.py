import os
import nbformat
import subprocess
from kaggle.api.kaggle_api_extended import KaggleApi

NOTEBOOK_FILENAME = "Stockfish321.ipynb"
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
    "title": "Stockfish321",
    "code_file": NOTEBOOK_FILENAME,
    "language": "python",
    "kernel_type": "notebook",
    "is_private": "true"
}
import json
with open("kernel-metadata.json", "w") as f:
    json.dump(metadata, f)

# Authenticate API (required for CLI to work properly)
api = KaggleApi()
api.authenticate()

# Use kaggle CLI to push the notebook
subprocess.run([
    "kaggle", "kernels", "push", "-p", "."
], check=True)

print(f"Notebook pushed: https://www.kaggle.com/code/{USERNAME}/{KERNEL_SLUG}")
