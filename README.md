# Terraform automation for COVID19 scraper
### learning project

![Terraform](https://github.com/mkutlak/aws-covid-data/workflows/Terraform/badge.svg)

### Description
Create necessary resources to deploy serverless COVID19 scraper.

Creates S3 bucket, CDN, DNS records, IAM policies, Lambda functions.

### Usage
Initiate Terraform:
```bash
make init
```

To plan the deployment:
```bash
$ make
$ make plan
```

To deploy the serverless app:
```bash
$ make
$ make apply
```

To destroy the app:
```bash
$ make destroy
```
