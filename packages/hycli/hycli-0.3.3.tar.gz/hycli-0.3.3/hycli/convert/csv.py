import os
import csv
from operator import itemgetter
from copy import deepcopy

from .commons import run_requests


def convert_to_csv(
    path,
    extractor_endpoint,
    vat_validator_endpoint=None,
    validation_endpoint=None,
    token=None,
    workers=6,
    probability=False,
):
    # TODO: Make different csv output for multi card
    # Get requests result
    result, single_fieldnames, multi_fieldnames, default_cols = run_requests(
        workers, path, extractor_endpoint, validation_endpoint, token,
    )
    # fieldnames = set().union(single_fieldnames, multi_fieldnames)
    processed_dir_name = os.path.normpath(path).split(os.path.sep)[-1]
    structure_result(result)

    with open(f"{processed_dir_name}_single_cardinality.csv", mode="w") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=sorted(single_fieldnames, key=itemgetter(0, -1)),
            extrasaction="ignore",
            delimiter=";",
        )
        writer.writeheader()
        for row in result:
            writer.writerow(result[row])


def structure_result(result):
    for row, row_items in deepcopy(result).items():
        for field, value in row_items.items():
            result[row][field] = value[0]
