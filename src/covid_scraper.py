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
from datetime import datetime as dt
from datetime import timedelta
from urllib.parse import urljoin
from urllib.error import HTTPError

COLUMN_FILTER='Country_Region'
DATE_FORMAT='%m-%d-%Y'
DATE_TODAY=dt.today().strftime(DATE_FORMAT)
DATE_YESTERDAY=(dt.today()-timedelta(days=1)).strftime(DATE_FORMAT)
DEFAULT_COUNTRY='Czechia'
GH_COVID_RAW=r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'


def pull_todays_covid_data():
    """
    Pulls COVID data (in CSV) from today from the referenced GH repo,
    filters by country (by default 'Czechia') and returns pandas.DataFrame.

    Ref link: https://github.com/CSSEGISandData/COVID-19
    """
    todays_data = pd.DataFrame()
    todays_filename = f"{DATE_YESTERDAY}.csv"
    csv_url = urljoin(GH_COVID_RAW, todays_filename)

    try:
        todays_data = pd.read_csv(csv_url)
        todays_data = todays_data[todays_data[COLUMN_FILTER] == DEFAULT_COUNTRY]
    except HTTPError as ex:
        if ex.code == 404:
            print(f"COVID data for {DATE_YESTERDAY} are not available.")
        else:
            raise ex

    # Save to CSV file
    # todays_data.to_csv(todays_filename)

    return todays_filename, todays_data
