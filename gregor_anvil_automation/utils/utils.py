from pathlib import Path
import csv

import addict
import yaml
from openpyxl import Workbook, load_workbook

from .types import Sample
from .mappings import TABLE_NAME_MAPPINGS


def get_table_samples(input_file: Path) -> dict[str, list[Sample]]:
    """Reads the given excel file path and gets the sample directories"""
    workbook: Workbook = load_workbook(input_file)
    table_samples = {}
    for _, sheet_name in enumerate(workbook.sheetnames):
        sheet = workbook[sheet_name]
        max_column = sheet.max_column
        samples = []
        headers = []
        for i in range(1, max_column + 1):
            if header := sheet.cell(row=1, column=i).value:
                headers.append(header.strip().lower().replace(" ", "_"))
        for row_cells in sheet.iter_rows(min_row=2):
            if all(
                cell.value is None or cell.value.strip() == "" for cell in row_cells
            ):
                continue
            sample = {
                header: (
                    ""
                    if row_cells[idx].value is None
                    else str(row_cells[idx].value).strip()
                )
                for idx, header in enumerate(headers)
            }
            sample["row_number"] = row_cells[0].row
            samples.append(sample)
            sheet_name = TABLE_NAME_MAPPINGS.get(sheet_name) or sheet_name.lower()
        table_samples[sheet_name] = samples
    return table_samples


def parse_yaml(yaml_path: Path) -> addict.Dict:
    """Parses a yaml file and return Iterator"""
    with open(yaml_path, encoding="utf-8") as fin:
        return addict.Dict(yaml.safe_load(fin.read()))


def generate_file(
    file_path: Path, data_headers: list[str], data: list[dict[str, str]], delimiter: str
):
    """Generates either a csv or tsv file depending on the passed in delimiter"""
    # MT: Lets just assume they are giving us these items.
    # https://stackoverflow.com/questions/11360858/what-is-the-eafp-principle-in-python
    if file_path and data_headers and data:
        with open(file_path, "w", encoding="utf-8") as file:
            writer = csv.DictWriter(
                f=file, fieldnames=data_headers, delimiter=delimiter
            )
            writer.writeheader()
            writer.writerows(data)  # This could be an problem for issues
            """
            writerows requires Iterable[Mapping[Any, Any]].
            data is a list[dict[str, str]] which works.
            issues is a list[Issue] which is a list of a class.
            However, that class is essentially just a dict which is a Map
            meaning issues could be considered a list[dict[Any, Any]].
            The question remains if it really does count as a Map.
            If this errors out then this is probably the issue.
            Would either have to adjust what data expects to take in to be more general
            or have no specifics on it and just only account for those two instances in
            the code itself, throwing out all others.
            It looks like classes are a Map, just will have to see if that's right.

            Turns out the Issue object is not an Iterable so aren't even into Map yet.
            Also need to fill out issues_control way want to
            """
