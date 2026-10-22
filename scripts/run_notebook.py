"""Execute both notebooks in order, each in a fresh kernel of this environment."""

from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parents[1]
notebooks = []
for name in [
    "01_data_preparation_and_indicators.ipynb",
    "02_statistical_inference_and_trends.ipynb",
]:
    path = root / "notebooks" / name
    notebook = nbformat.read(path, as_version=4)

    # Catch source errors in either notebook before regenerating any outputs.
    for number, cell in enumerate(notebook.cells, start=1):
        if cell.cell_type == "code":
            compile(cell.source, f"{name}, cell {number}", "exec")
            cell.outputs = []
            cell.execution_count = None
    nbformat.validate(notebook)
    notebooks.append((path, notebook))

for path, notebook in notebooks:
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
