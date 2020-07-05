# Terraform automation for COVID19 scraper
### learning project

![Terraform](https://github.com/mkutlak/aws-covid-data/workflows/Terraform/badge.svg)

### Description
Create necessary resources to deploy serverless COVID19 scraper.

Creates S3 bucket, CDN, DNS records, IAM policies, Lambda functions.

<p align="center">
<img src="https://github.com/mkutlak/aws-covid-data/blob/master/diagrams/covid19_scraper_web_app.png" height="480">
</p>

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
