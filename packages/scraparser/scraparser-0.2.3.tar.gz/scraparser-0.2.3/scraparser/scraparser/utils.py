import csv
import io
import os
import os.path
from pathlib import Path
import urllib.request
import magic


def scrap_url(url, filename, mkdir=True, headers={}):
    if os.path.exists(filename):
        raise Exception("File already exists: {0}".format(filename))

    req = urllib.request.Request(
        url,
        data=None,
        headers=headers,
    )
    response = urllib.request.urlopen(req)
    with open(filename, "wb") as file:
        file.write(response.read())


def ensure_file_or_url(file, url, mkdir=True, headers={}):

    # if supplied with a file flag
    if not os.path.exists(file):

        # Create data folder, if not exists
        if mkdir == True:
            dirname = os.path.dirname(file)
            Path(dirname).mkdir(parents=True, exist_ok=True)

        # Download the PDF file
        req = urllib.request.Request(
            url,
            data=None,
            headers=headers,
        )
        response = urllib.request.urlopen(req)
        with open(file, "wb") as file:
            file.write(response.read())



def do_scrap_csv(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    response = urllib.request.urlopen(req)
    f = io.StringIO(response.read().decode('utf-8'))
    return csv.reader(f)
