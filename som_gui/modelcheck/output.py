import os
import sqlite3

import openpyxl
from openpyxl.worksheet.table import Table,TableStyleInfo
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter

from . import sql

HEADER = ["Datum","GUID", "Beschreibung", "Typ","Name", "PropertySet", "Attribut", "Datei", "Bauteilklassifikation"]


def save_workbook(workbook, path):
    try:
        workbook.save(path)
    except PermissionError:
        print("-" * 60)
        print(f"folgende Datei ist noch geöffnet: {path} \n Datei schließen und beliebige Taste Drücken")
        input("Achtung! Datei wird danach überschrieben!")
        save_workbook(workbook, path)

def create_issues(db_name, path):
    def get_max_width():
        col_widths = [0 for _ in range(worksheet.max_column)]
        for row_index, row in enumerate(worksheet,start = 1):
            for col_index,cell in enumerate(row):
                length = len(str(cell.value))
                if length > col_widths[col_index]:
                    col_widths[col_index] = length
        return col_widths


    print(db_name)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.mkdir(directory)

    issues = sql.query_issues(cursor)

    conn.commit()
    conn.close()

    print(f"{len(issues)} Fehler gefunden!")

    if len(issues) == 0:
        print("Modelle fehlerfrei!")
        return

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    for col_index, value in enumerate(HEADER, start=1):
        worksheet.cell(1, col_index, value)

    last_cell = worksheet.cell(1,8)

    for row_index, column in enumerate(issues, start=2):
        for column_index, value in enumerate(column, start=1):
            last_cell = worksheet.cell(row_index, column_index, value)  # remove Whitespace


    table_zone = f"A1:{last_cell.coordinate}"
    tab = Table(displayName="Issues",ref=table_zone)
    style = TableStyleInfo(name= "TableStyleMedium9",showFirstColumn=False,showLastColumn=False,showRowStripes=True,showColumnStripes=True)
    tab.tableStyleInfo = style
    worksheet.add_table(tab)

    max_widths = get_max_width()


    #autoFit Column
    dim_holder = DimensionHolder(worksheet=worksheet)
    for col in range(worksheet.min_column, worksheet.max_column + 1):
        dim_holder[get_column_letter(col)] = ColumnDimension(worksheet, min=col, max=col, width=max_widths[col-1]*1.1)
    worksheet.column_dimensions = dim_holder

    save_workbook(workbook, path)
    print("Done")