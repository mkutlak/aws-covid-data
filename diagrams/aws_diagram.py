#!/bin/python3
"""
Diagram of AWS Infra for COVID19 Scraper App.
"""
from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.general import TradicionalServer
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.aws.storage import S3


with Diagram ("COVID19 Scraper Web App", show=False):
    with Cluster("Processing"):
        lbd = Lambda("Scraper")

    with Cluster("Web"):
        s3 = S3("C19.eu")

    source = TradicionalServer("DATA")
    cron = Cloudwatch("CW(cron)")
    iam = IAM("IAM")

    # Pipeline from data source to output through S3.
    source >> lbd >> s3

    # Lambda function updating WebApp after S3 change.
    s3 >> lbd

    # IAM for basic Lambda execution.
    iam >> lbd

    # Daily execution of Lambda function
    cron >> lbd
