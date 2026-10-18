"""Execute the first-stage notebook in a fresh kernel of this Python environment."""

from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parents[1]
path = root / "notebooks/01_data_preparation_and_indicators.ipynb"
notebook = nbformat.read(path, as_version=4)

manager = KernelManager(kernel_name="python3")
manager.kernel_spec.argv = [
    sys.executable,
    "-m",
    "ipykernel_launcher",
    "-f",
    "{connection_file}",
]

client = NotebookClient(
    notebook,
    timeout=600,
    km=manager,
    resources={"metadata": {"path": str(root)}},
)

try:
    client.execute()
finally:
    nbformat.write(notebook, path)

print(f"Executed all cells successfully: {path.relative_to(root)}")
