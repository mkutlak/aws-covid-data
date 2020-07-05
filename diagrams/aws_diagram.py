#!/bin/python3
"""
Diagram of AWS Infra for COVID19 Scraper App.
"""
from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.general import TradicionalServer
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import CloudFront, Route53
from diagrams.aws.security import ACM, IAM
from diagrams.aws.storage import S3


with Diagram ("COVID19 Scraper Web App", show=False):
    with Cluster("Processing"):
        lbd = Lambda("Scraper")

    with Cluster("Web"):
        dns = Route53("DNS")
        cfront = CloudFront("CDN")
        cert = ACM("CERT")

    source = TradicionalServer("DATA")
    s3 = S3("C19.eu")
    cron = Cloudwatch("CW(cron)")
    iam = IAM("IAM")

    # Pipeline from data source to output available through DNS record.
    source >> lbd >> s3 >> cfront >> dns

    # Lambda function updating WebApp after S3 change.
    lbd << s3

    # IAM for basic Lambda execution.
    iam >> lbd

    # Daily execution of Lambda function
    cron >> lbd

    # Certificate for CDN.
    cert >> cfront
