#!/bin/python3
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

Filters data by COUNTRY and DATE.
"""
import os
import click
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime as dt
from datetime import timedelta
from urllib.parse import urljoin
from urllib.error import HTTPError


COLUMN_FILTER='Country_Region'
DATE_FORMAT='%m-%d-%Y'
DATE_TODAY=dt.today().strftime(DATE_FORMAT)
DATE_YESTERDAY=(dt.today()-timedelta(days=1)).strftime(DATE_FORMAT)
GH_COVID_RAW=r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'


def validate_date_fmt(ctx, param, value):
    """
    Validate format of the date provided by user.
    """
    try:
        provided_date = dt.strptime(value, DATE_FORMAT)
        if value > DATE_TODAY:
            raise click.BadParameter('Provided date is in the future.')
        return provided_date.strftime(DATE_FORMAT)
    except ValueError:
        raise click.BadParameter('Incorrect date format. Correct format is MM-DD-YYYY.')

@click.command()
@click.option('-S', '--since', callback=validate_date_fmt, default=DATE_TODAY, help='Date since to get data, in format MM-DD-YYYY.')
@click.option('-C', '--country', default='Czechia', type=str, help='Country name used to filter the data.')
@click.option('-o', '--output', type=click.Path(), help='Output directory to place CSVs.')
def execute_main(since, country, output):
    """
    Pulls data (CSV) from the referenced GH repo, filters
    by country specified 'country' parameter and saves it
    to CSV file.

    Ref link: https://github.com/CSSEGISandData/COVID-19
    """
    if not output:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output)

    output_dir.mkdir(exist_ok=True)

    date_range = pd.date_range(start=since, end=DATE_TODAY)
    date_csv_files = [f"{date.strftime(DATE_FORMAT)}.csv" for date in date_range]

    # get raw csvs from github
    # filter out other contries and save locally
    for fname in date_csv_files:
        fout = output_dir / fname
        csv_url = urljoin(GH_COVID_RAW, fname)
        try:
            covid_data = pd.read_csv(csv_url)
            country_data = covid_data[covid_data[COLUMN_FILTER]==country]
            country_data.to_csv(fout)
        except HTTPError as ex:
            if ex.code == 404:
                print(f"COVID-19 data are not available for {fout.stem}.")
            else:
                logging.error(f"{ex}: Failed to get data for {fout.stem}.")

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    execute_main()
