#!/usr/bin/python3
import os
import boto3
from io import StringIO
import covid_scraper as cs

BUCKET_NAME='covid.themkutlak.eu'
OUTPUT_DIR='data'

def lambda_handler(event, context):
    """
    AWS Lambda function to pull COVID-19 data and save them to S3
    bucket.
    """
    csv_buffer = StringIO()
    s3 = boto3.resource('s3')

    print("Pulling COVID-19 data.")
    datafile, covid_data = cs.pull_todays_covid_data()
    if not covid_data.empty:
        covid_data.to_csv(csv_buffer)
    else:
        return { 'message': 'Failed to get today\'s COVID-19 data.' }

    print(f"Saving '{datafile}' to S3 bucket '{BUCKET_NAME}'.")
    filepath = os.path.join(OUTPUT_DIR, datafile)
    s3.Object(BUCKET_NAME, filepath).put(Body=csv_buffer.getvalue())

    print("All done.")
    return { 'message': 'Success!' }