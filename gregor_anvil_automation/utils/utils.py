from pathlib import Path

from openpyxl import Workbook, load_workbook

from .types import Sample


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
            if all(cell.value is None for cell in row_cells):
                continue
            sample = {
                header: (
                    ""
                    if row_cells[idx].value is None
                    else str(row_cells[idx].value).strip()
                )
                for idx, header in enumerate(headers)
            }
            samples.append(sample)
        table_samples[sheet_name] = samples
    return table_samples
