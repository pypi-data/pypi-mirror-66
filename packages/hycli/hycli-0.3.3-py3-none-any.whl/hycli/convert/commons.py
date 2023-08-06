import os
from concurrent.futures import ThreadPoolExecutor as Executor
from pathlib import Path

import click
from filetype import guess

from ..services.requests import extract_invoice, validation


def read_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf:
        pdf = pdf.read()

    return (pdf_path, pdf)


class InvoiceExtractorException(Exception):
    """Raised when the Invoice Extractor service returns an error."""

    pass


def run_requests(
    workers, path, extractor_endpoint, validation_endpoint, token,
):
    types = ("*.pdf", "*.tif", "*.tiff", "*.png", "*.jpg")
    file_count = 0
    single_fieldnames = {
        "file_name": (None, None, None),
        "error_message": (None, None, None),
    }
    multi_fieldnames = {
        "file_name": (None, None, None),
        "row_number": (None, None, None),
    }
    default_cols = set().union(single_fieldnames.keys(), multi_fieldnames.keys())
    result = {}

    with Executor(max_workers=workers) as exe:
        for file_type in types:
            full_path = os.path.join(os.getcwd(), path)
            files = Path(full_path).rglob(file_type)

            # TODO: Put validation request inside of IE request job.
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
                    file_path = None
                    try:
                        file_path, extracted_invoice = job.result(timeout=300)

                        # TODO: Move this to extract_invoice function.
                        if "error" in extracted_invoice["infos"]:
                            error = extracted_invoice["infos"]["error"]
                            raise InvoiceExtractorException(
                                f"Error in Invoice Extractor: {error}"
                            )

                        if validation_endpoint:
                            validated_invoice = validation(
                                extracted_invoice, validation_endpoint
                            )
                        else:
                            validated_invoice = None

                        result[file_count] = flatten_invoice(
                            extracted_invoice, validated_invoice,
                        )
                    except Exception as e:
                        result[file_count] = {}
                        result[file_count]["error_message"] = (repr(e), None, None)
                    finally:
                        file_name = file_path.split("/")[-1] if file_path else None
                        result[file_count]["file_name"] = (file_name, None, None)

                    collect_column_names(
                        result[file_count], single_fieldnames, multi_fieldnames
                    )

                    file_count += 1
    if not result:
        quit(f"No files of extension: {types} found in path")

    return result, single_fieldnames, multi_fieldnames, default_cols


def flatten_invoice(invoice, validation):
    return_dict = dict()
    entities = invoice["entities"]
    probabilities = invoice["probabilities"]

    def traverse_items(entities, probabilities, validation, _dict, *prefix):
        for k, v in entities.items():
            if isinstance(v, dict):
                traverse_items(
                    entities[k],
                    probabilities[k],
                    validation[k][0] if validation and k in validation else None,
                    return_dict,
                    k,
                )
            elif isinstance(v, list):
                for counter, list_item in enumerate(v):
                    # TODO: fix terms and ibanAll
                    if k != "terms" and k != "ibanAll":
                        temp_dict = {}
                        for item, value in list_item.items():
                            temp_dict[f"{k}_{item}_{counter}"] = value
                        traverse_items(
                            temp_dict,
                            probabilities[k][counter],
                            validation[k][0][str(counter)][0]
                            if validation
                            and k in validation
                            and str(counter) in validation[k][0]
                            else None,
                            return_dict,
                        )
            else:
                try:
                    # dirty solution, assumes no invoice extractor response field got underscore
                    original_k = k.split("_")[-2]
                except IndexError:
                    original_k = k

                if prefix:
                    field_name = f"{prefix[0]}_{k}"
                else:
                    field_name = k

                if original_k in probabilities:
                    if probabilities[original_k]:
                        _dict[field_name] = (v, probabilities[original_k], None)
                    else:
                        _dict[field_name] = (v, None, None)
                else:
                    _dict[field_name] = (v, None, None)
                if validation:
                    if original_k in validation:
                        _dict[field_name] = (v, None, validation[original_k])

    traverse_items(entities, probabilities, validation, return_dict)
    return return_dict


def collect_column_names(extracted_invoice, single_fieldnames, multi_fieldnames):
    """Iterate through extracted invoice and write fieldnames to single or multi
    cardinality

    Arguments:
        extracted_invoice {[type]} -- [description]
        multi_fieldnames {[type]} -- [description]
        single_fieldnames {[type]} -- [description]
    """
    for col_name in extracted_invoice.keys():
        if col_name[-1].isdigit():
            label = "_".join(col_name.split("_")[:-1])
            multi_fieldnames[label] = (None, None, None)
        else:
            single_fieldnames[col_name] = (None, None, None)
