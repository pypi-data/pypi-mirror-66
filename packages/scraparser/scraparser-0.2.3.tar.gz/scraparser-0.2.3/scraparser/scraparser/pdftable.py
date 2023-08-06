import sys

import camelot
import pandas as pd

def pdf_tables_to_dataframe(filepath, headers=False, pages='all', is_valid_table=False, sanitize=False):
    """Read all tables in a given PDF then concat all into one dataframe"""

    # Read all tables in a PDF to frames
    tables = camelot.read_pdf(filepath=filepath, pages=pages)
    frames = []

    # define a header sanitier
    sanitize_header = lambda a: a
    if sanitize != False:
        sanitize_header = lambda d: dict(map(lambda kv: (kv[0], sanitize(kv[1])), d.items()))

    firstHeaders = sanitize_header(tables[0].df.iloc[0].to_dict())

    if is_valid_table == False:
        # If no validator function, set it to check if the first headers are identical
        is_valid_table = lambda a: sanitize_header(a.iloc[0].to_dict()) == firstHeaders

    # loop through all tables, determine if they are valid for concat,
    # then put it into the "frames" slice for concating
    for i in range(0, tables.n):
        if is_valid_table(tables[i].df):
            frames.append(tables[i].df[1:])

    # assign the first table header to be the overall header
    # if none is provided
    if headers == False:
        headers = firstHeaders

    # concat all data frames into a single one
    return pd.concat(frames, ignore_index=True, sort=False).rename(columns=headers)


def sort_dataframe_by(df, column_index, sort_as_number=True):
    """Sort data by the specified column (expect it to be numeric)"""
    # Sort the values by case id
    if sort_as_number:
        df[column_index] = pd.to_numeric(df[column_index])
    df.sort_values(by=column_index, inplace=True)


def sanitize_items_in(df, sanitize):
    """Sanitize the dataframe values if it has EOL or space in it"""
    # Sanitize the dataframe values
    for i, row in df.iterrows():
        for key, value in row.iteritems():
            if type(value) != str:
                continue
            if "\n" in value or " " in value:
                df.at[i, key] = sanitize(value)
