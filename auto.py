import nbformat

NOTEBOOK_FILENAME = "Stockfish321.ipynb"

# Read commands from cmd.txt
with open("cmd.txt", "r") as f:
    cmds = f.read()

# Create notebook with one code cell containing all commands
nb = nbformat.v4.new_notebook()
nb.cells.append(nbformat.v4.new_code_cell(cmds))

# Save notebook (overwrites existing file)
with open(NOTEBOOK_FILENAME, "w") as f:
    nbformat.write(nb, f)
