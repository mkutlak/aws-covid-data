#!/usr/bin/python3
"""
MIT License

Copyright (c) 2020 Martin Kutlak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description:

Simple data scraper for covid-19 data from https://github.com/CSSEGISandData/COVID-19

Pulls COVID-19 data from the current day and filters data by COUNTRY (default 'Czechia').
"""

import pandas as pd
import dominate
from dominate import tags
from dominate.util import raw
from datetime import datetime as dt
from datetime import timedelta
from pathlib import Path
from urllib.parse import urljoin
from urllib.error import HTTPError

# Bootstrap resources
BS_CSS_LINK=r'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css'
BS_JQ_LINK=r'https://code.jquery.com/jquery-3.5.1.slim.min.js'
BS_POP_LINK=r'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js'
BS_BS_LINK=r'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js'

# Date
DATE_FORMAT='%m-%d-%Y'
DATE_TODAY=dt.today().strftime(DATE_FORMAT)
DATE_YESTERDAY=(dt.today()-timedelta(days=1)).strftime(DATE_FORMAT)

# Table operation
COLUMN_FILTER='Country_Region'
DEFAULT_COUNTRY='Czechia'
GH_COVID_RAW=r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'


def get_covid_data():
    """
    Pulls COVID data (in CSV) from today from the referenced GH repo,
    filters by country (by default 'Czechia') and returns pandas.DataFrame.

    Ref link: https://github.com/CSSEGISandData/COVID-19
    """
    todays_data = pd.DataFrame()
    todays_filename = f"{DATE_YESTERDAY}.csv"
    csv_url = urljoin(GH_COVID_RAW, todays_filename)

    try:
        todays_data = pd.read_csv(csv_url, index_col=0)
    except HTTPError as ex:
        if ex.code == 404:
            print(f"COVID data for {DATE_YESTERDAY} are not available.")
        else:
            raise ex

    return todays_filename, todays_data


def filter_by_country(data, country=DEFAULT_COUNTRY):
    """
    Filter provided data by country (defaults to Czechia).

    data: pandas.DataFrame
    country: str
    """
    # Filter data by COUNTRY
    return data[data[COLUMN_FILTER] == country]
    

def update_csv(orig_csv, new_data):
    """
    Updates CSV file with new data and returns the updated data.

    orig_csv: path to CSV
    new_data: pandas.DataFrame
    """
    new_record = filter_by_country(new_data)
    if Path(orig_csv).is_file():
        origin = pd.read_csv(orig_csv, index_col=0)
        origin.append(new_record, ignore_index=True)
        # Drop all duplicated records
        origin.drop_duplicates(keep=False, inplace=True, ignore_index=True)
    else:
        # Origin is empty, create a new one from new data.
        origin = new_record

    origin.to_csv(orig_csv, index=False)

    return origin


def create_index(data, out):
    """
    Return a web page with a table representing of provided data.

    out file is created if it doesn't exist.

    data: pandas.DataFrame
    out: path to file for index.html
    """
    css_classes = 'table table-sm table-striped table-hover table-borderless text-center'
    table = data.to_html(classes=css_classes, 
                         index=False, # do not display indexes
                         border=0, # remove table border
                         na_rep="-") # represent empty cels with '-'

    page = dominate.document(title="COVID-19")

    with page.head:
        tags.link(rel="stylesheet", href=BS_CSS_LINK)
        tags.script(rel="text/javascript", href=BS_JQ_LINK)
        tags.script(rel="text/javascript", href=BS_POP_LINK)
        tags.script(rel="text/javascript", href=BS_BS_LINK)

    with page:
        with tags.div():
            raw(table)

    index = Path(out)
    index.touch(exist_ok=True)
    with index.open("w") as fd:
        fd.write(page.render())