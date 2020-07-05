#!/usr/bin/python3
import os
import boto3
import covid_scraper as cs
from pathlib import Path

BUCKET='covid19.themkutlak.eu'
INDEX='index.html'
CZECH_DATA='czechia_table.csv'
S3_DIR='/data/'
TMP='/tmp/'

def get_paths(filename):
    """
    Returns temporary path for Lambda processing and S3 path.

    /tmp/filname
    /data/filename
    """
    lamPath = os.path.join(TMP, filename)
    s3Path = os.path.join(S3_DIR, filename)

    return lamPath, s3Path


def lambda_handler(event, context):
    """
    AWS Lambda function to pull COVID-19 data and save them to S3
    bucket.
    """
    s3 = boto3.resource('s3')

    print("Pulling COVID-19 data.")
    fileName, covidData = cs.get_covid_data()
    tmpPath, newPath = get_paths(fileName)

    if not covidData.empty:
        covidData.to_csv(tmpPath)
    else:
        return { 'message': 'Failed to get today\'s COVID-19 data.' }

    print(f"Saving '{fileName}' to S3 bucket '{BUCKET}{S3_DIR}'.")
    s3.upload_file(tmpPath, BUCKET, newPath)

    print(f"Updating table data.")
    tmpCzech, czechTable = get_paths(CZECH_DATA)
    s3.download_file(BUCKET, czechTable, tmpCzech)
    newData = cs.update_csv(tmpCzech, covidData)

    print(f"Saving {CZECH_DATA} to S3 bucket '{BUCKET}'.")
    s3.upload_file(tmpCzech, BUCKET, czechTable)

    print(f"Saving updated index.html to S3 bucket {BUCKET}.")
    tmpIndex, _ = get_paths(INDEX)
    cs.create_index(newData, tmpIndex)
    s3.upload_file(tmpIndex, BUCKET, INDEX)

    print("All done.")
    return { 'message': 'Success!' }
