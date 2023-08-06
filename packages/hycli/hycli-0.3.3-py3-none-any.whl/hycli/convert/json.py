import os
import json

from concurrent.futures import ThreadPoolExecutor as Executor
from pathlib import Path

import click
from filetype import guess

from ..services.requests import extract_invoice
from .commons import read_pdf


def convert_to_json(path, extractor_endpoint, token, workers):
    types = ("*.pdf", "*.tif", "*.tiff", "*.png", "*.jpg")

    with Executor(max_workers=workers) as exe:
        for file_type in types:
            full_path = os.path.join(os.getcwd(), path)
            files = Path(full_path).rglob(file_type)
            jobs = [
                exe.submit(
                    extract_invoice,
                    read_pdf(str(filename)),
                    extractor_endpoint,
                    guess(str(filename)).mime,
                    token,
                )
                for filename in files
                if guess(str(filename)).mime
            ]
            label = f"Converting {len(jobs)} invoices with {file_type} extension"
            with click.progressbar(jobs, label=label) as bar:
                for id, job in enumerate(bar):
                    try:
                        filename, response = job.result(timeout=300)

                    except Exception as e:
                        print(f"Error: {e}")

                    with open(filename.split(".")[0] + ".json", "w") as f:
                        json.dump(response, f)
