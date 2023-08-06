#!/usr/bin/env python3

import logging
import math
import os
import re
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from urllib.parse import urlparse

import click
import magic
import validators

from scraparser.pdftable import (pdf_tables_to_dataframe, sanitize_items_in,
                          sort_dataframe_by)
from scraparser.csvtable import from_csv
from scraparser.googlesheet import get_credentials, overwrite_sheet
from scraparser.utils import do_scrap_csv, scrap_url


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    loglevel = logging.WARNING
    if debug:
        loglevel = logging.DEBUG

    # Declare logger with file logging
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = RotatingFileHandler('scraper.log',
            maxBytes=4000000,
            backupCount=5)
    fh.setLevel(loglevel)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


@cli.command()
@click.option('--print-filename', default=True, is_flag=True, help="Print the result filename to STDOUT.")
@click.argument('urls', nargs=-1)
@click.pass_context
def scrap(ctx, print_filename, urls):
    """Scrap any URL, add some timestamp string, then save to the "./data" folder of the install location."""

    if len(urls) == 0:
        urls = sys.stdin

    for url_input in urls:
        if not validators.url(url_input):
            raise Exception("Not a valid URL: {0}".format(url_input))

        url = urlparse(url_input)
        # Note: might support other scheme such as "file://" in the future,
        # but focus on HTTP and FTP for now.
        if url.scheme not in ["http", "https", "ftp"]:
            raise Exception("Not a supported URL scheme: {0}".format(url_input))

        # Rewrite the filename (from path) to add timestamp
        filename_basename = os.path.basename(url.path)
        timestring = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        dirname = os.path.join(
            os.getcwd(),
            "data",
        )
        filename_scraped = os.path.join(
            dirname,
            "{0}.{1}{2}".format(
                os.path.splitext(filename_basename)[0],
                timestring,
                os.path.splitext(filename_basename)[1],
            ),
        )

        # Do the scrapping
        scrap_url(
            url.geturl(),
            filename_scraped,
            mkdir=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            },
        )

        if print_filename:
            print(filename_scraped)


@cli.command()
@click.option('--leave-space', default=False, is_flag=True, help="Leave the space in scraped table cells in sanitation process.")
@click.option('--headers', default=False, help="Specify the header names, separated by commas, for replacing the overall table. Use delimited \"\\,\" if you need to use actual comma.")
@click.option('--print-filename', default=True, is_flag=True, help="Print the result CSV filename to STDOUT.")
@click.argument('files', nargs=-1)
@click.pass_context
def parse_pdf_to_csv(ctx, leave_space, headers, print_filename, files):
    """Parse the PDF file and join all the tables"""

    if len(files) == 0:
        files = sys.stdin

    for filename_input in files:
        filename_input = filename_input.strip()

        filename_basename = os.path.basename(filename_input)
        filename_csv = os.path.join(
            os.path.dirname(os.path.abspath(filename_input)),
            os.path.splitext(filename_basename)[0] + ".csv",
        )

        # Define string sanitize
        sanitize = lambda a: a.replace("\r", "").replace("\n", "").replace(" ", "")
        if leave_space:
            sanitize = lambda a: a.replace("\r", "").replace("\n", "")

        if headers != False:
            # Treat the headers input as comma separated values
            headers_list = list(map(lambda a: a.replace("\\,", ","), re.split(r'(?<!\\),', headers)))
            headers_dict = dict(enumerate(headers_list))
        else:
            headers_dict = False

        # concat all tables, which passes the "is_valid_table" test
        # into a single dataframe.
        df = pdf_tables_to_dataframe(
            filename_input,
            headers=headers_dict,
            #is_valid_table=lambda df: df[0][0] in ["個案\n編號", "Case \nno."],
            sanitize=sanitize,
        )

        # Sanitize the dataframe values
        sanitize_items_in(df, sanitize)

        # Write to CSV file
        df.to_csv(filename_csv, index=False)

        # Optionally print the result CSV filename to STDOUT for piping
        if print_filename:
            print("{0}".format(filename_csv))


@cli.command()
@click.option('--sort-as-number', default=True, is_flag=True, help="To treat the column like number for sorting. Default True")
@click.option('--column', default=0, type=int, help="The column number to sort with. Count starting with 0. Default 0")
@click.option('--in-place', default=False, is_flag=True, help="Modify the file in-place.")
@click.option('--print-filename', default=True, is_flag=True, help="Print the result CSV filename to STDOUT.")
@click.argument('files', nargs=-1)
@click.pass_context
def sort(ctx, column, sort_as_number, in_place, print_filename, files):
    """Sort the data by the specified column. By default sort by the first column."""

    if len(files) == 0:
        files = sys.stdin

    for filename_input in files:
        filename_input = filename_input.strip()
        df = from_csv(filename_input)

        # Sort the values by case id
        sort_dataframe_by(df, df.keys()[0], sort_as_number=sort_as_number)

        filename = "output.csv"
        if in_place:
            filename = filename_input
        df.to_csv(filename, index=False)

        if print_filename:
            print("{0}".format(filename))


@cli.command()
@click.option('--in-place', default=False, is_flag=True, help="Modify the file in-place.")
@click.option('--print-filename', default=True, is_flag=True, help="Print the result CSV filename to STDOUT.")
@click.argument('files', nargs=-1)
@click.pass_context
def fix_empty_rows(ctx, in_place, print_filename, files):
    """Treat rows with only 1 cell to be a parser mistake. Concat that cell content to the one above it."""

    if len(files) == 0:
        files = sys.stdin

    for filename_input in files:
        filename_input = filename_input.strip()
        df = from_csv(filename_input)

        rows_to_drop = []

        for i, row in df.iterrows():
            num_empty_field = 0
            non_empty_cell_key = -1

            for key, value in row.iteritems():
                if type(value) == float and math.isnan(value):
                    num_empty_field += 1
                else:
                    non_empty_cell_key = key

            # If the row has only 1 field defined
            if num_empty_field == len(row) - 1 and i > 0:
                df.at[i-1, non_empty_cell_key] += df.at[i, non_empty_cell_key]
                rows_to_drop.append(i)

        df = df.drop(rows_to_drop)

        filename = "output.csv"
        if in_place:
            filename = filename_input
        df.to_csv(filename, index=False)

        if print_filename:
            print("{0}".format(filename))


@cli.command()
@click.option('--column', type=int, help="To treat the column with empty value. Begins with 0. Required.")
@click.option('--in-place', default=False, is_flag=True, help="Modify the file in-place.")
@click.option('--print-filename', default=True, is_flag=True, help="Print the result CSV filename to STDOUT.")
@click.argument('files', nargs=-1)
@click.pass_context
def fix_column_underflow(ctx, column, in_place, print_filename, files):
    """Fix the empty values which content spilled over to the last column."""

    if len(files) == 0:
        files = sys.stdin

    for filename_input in files:
        filename_input = filename_input.strip()
        df = from_csv(filename_input)
        keys = df.keys()
        accepted_values = list(filter(lambda a: type(a) == str, df[keys[column]].unique()))

        for i, row in df.iterrows():
            if type(row.iat[column]) == float and math.isnan(row.iat[column]):
                for accepted_value in accepted_values:
                    if row.iat[column-1].endswith(accepted_value):
                        df.iat[i, column-1] = row.iat[column-1][:-len(accepted_value)]
                        df.iat[i, column] = accepted_value

        filename = "output.csv"
        if in_place:
            filename = filename_input
        df.to_csv(filename, index=False)

        if print_filename:
            print("{0}".format(filename))


@cli.command()
@click.option('--column', type=int, help="To treat the column with empty value. Begins with 0. Required.")
@click.option('--date-format', type=str, default="DD/MM/YYYY", help="Specify the format of the date string. Default: DD/MM/YYYY.")
@click.option('--in-place', default=False, is_flag=True, help="Modify the file in-place.")
@click.option('--print-filename', default=True, is_flag=True, help="Print the result CSV filename to STDOUT.")
@click.argument('files', nargs=-1)
@click.pass_context
def fix_date_column_underflow(ctx, column, date_format, in_place, print_filename, files):
    """Fix the empty values of date column, which content spilled over to the last column."""

    if len(files) == 0:
        files = sys.stdin

    # parse date format into regex
    pattern = re.escape(date_format).upper()
    pattern = pattern.replace("YYYY", "\\d{4}")
    pattern = pattern.replace("YY", "\\d{2}")
    pattern = pattern.replace("MM", "\\d{2}")
    pattern = pattern.replace("DD", "\\d{2}")
    pattern = "^(.+?)({0})$".format(pattern)

    for filename_input in files:
        filename_input = filename_input.strip()
        df = from_csv(filename_input)
        #keys = df.keys()

        for i, row in df.iterrows():
            if type(row.iat[column]) == float and math.isnan(row.iat[column]):
                match = re.match(pattern, str(row.iat[column-1]))
                if match is not None:
                    df.iat[i, column-1] = match.group(1)
                    df.iat[i, column] = match.group(2)

        filename = "output.csv"
        if in_place:
            filename = filename_input
        df.to_csv(filename, index=False)

        if print_filename:
            print("{0}".format(filename), file=sys.stdout)


@cli.group()
@click.option('-c', '--credentials', 'credentials_file', type=str, default="credentials.json")
@click.option('-p', '--pickle', 'pickle_file', type=str, default="token.pickle")
@click.argument('googlesheet_id')
@click.pass_context
def googlesheet(ctx, credentials_file, pickle_file, googlesheet_id):
    """Manipulate of Google Sheet data"""
    ctx.obj["googlesheet_id"] = googlesheet_id
    ctx.obj["credentials"] = get_credentials(
        [
            'https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/spreadsheets',
        ],
        credentials_file=credentials_file,
        pickle_file=pickle_file,
    )


@googlesheet.command("update")
@click.option('-f', '--from', 'filename_from', type=str, help="Specify the CSV filename for input.")
@click.option('-h', '--include-headers', is_flag=True, default=False, help="Include the header label as first row of the data.")
@click.option('-r', '--range', 'range_name', type=str, required=True, help="Specify the range to update.")
@click.pass_context
def googlesheet_update(ctx, filename_from, include_headers, range_name):
    """Update google sheet"""

    files = []
    if filename_from is not None:
        files = [filename_from]

    if len(files) == 0:
        files = sys.stdin

    for filename_input in files:
        filename_input = filename_input.strip()
        print(filename_input)
        df = from_csv(filename_input)

        # convert dataframe into 2-dimensional slice
        values = list(map(lambda a: a.tolist(), df.values))

        if include_headers:
            new_values = [list(df.keys())]
            new_values.extend(values)
            values = new_values

        overwrite_sheet(
            ctx.obj["credentials"],
            values=values,
            spreadsheetId=ctx.obj["googlesheet_id"],
            range=range_name,
            valueInputOption='RAW',
        )
