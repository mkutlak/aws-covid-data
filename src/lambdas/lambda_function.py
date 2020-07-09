#!/usr/bin/python3
import os
import boto3
import covid_scraper as cs
from botocore.exceptions import ClientError
from mimetypes import guess_type

INDEX='index.html'
CZECH_DATA='czechia_table.csv'
S3_DIR='data'
TMP='/tmp/'

# Client for operation with S3
# Requires IAM policy for S3 with following permissions:
# GetObject, PutObject and HeadObject
s3 = boto3.client('s3')


def get_paths(filename):
    """
    Returns temporary path for Lambda processing and S3 path.

    /tmp/filname
    data/filename
    """
    lamPath = os.path.join(TMP, filename)
    s3Path = os.path.join(S3_DIR, filename)

    return lamPath, s3Path


def is_S3File(bucket, key):
    """
    Check if 'key' object exists in S3 Bucket.

    bucket: Name of the S3 bucket
    key: Object path in S3
    """
    is_file = False
    try:
        s3.head_object(Bucket=bucket, Key=key)
        is_file = True

    except ClientError as err:
        if err.response['Error']['Code'] == '404':
            print(f"Error Message: {err.response['Error']['Message']}")
        else:
            raise

    return is_file



def lambda_handler(event, context):
    """
    AWS Lambda function to pull COVID-19 data and save them to S3
    bucket.
    """
    cvd_bucket = event["S3Bucket"] if "S3Bucket" in event else None
    if not cvd_bucket:
        print('Missing S3 bucket!')
        return { 'message': 'Error: S3 bucket was not found in event data!' }

    print("Pulling COVID-19 data.")
    fileName, covidData = cs.get_covid_data()
    tmpPath, newPath = get_paths(fileName)

    if not covidData.empty:
        covidData.to_csv(tmpPath)
    else:
        return { 'message': 'Failed to get today\'s COVID-19 data.' }

    print(f"Saving '{fileName}' to S3 bucket '{cvd_bucket}/{S3_DIR}'.")
    s3.upload_file(tmpPath, cvd_bucket, newPath)

    print(f"Updating table data.")
    tmpCzech, czechTable = get_paths(CZECH_DATA)
    if is_S3File(cvd_bucket, czechTable):
        s3.download_file(cvd_bucket, czechTable, tmpCzech)
    newData = cs.update_csv(tmpCzech, covidData)

    print(f"Saving {CZECH_DATA} to S3 bucket '{cvd_bucket}'.")
    s3.upload_file(tmpCzech, cvd_bucket, czechTable)

    print(f"Saving updated index.html to S3 bucket {cvd_bucket}.")
    tmpIndex, _ = get_paths(INDEX)
    cs.create_index(newData, tmpIndex)
    content_type = guess_type(tmpIndex)[0]
    s3.upload_file(tmpIndex, cvd_bucket, INDEX,
                   ExtraArgs={'ContentType': content_type, 'ACL': "public-read"})

    print("All done.")
    return { 'message': 'Success!' }
