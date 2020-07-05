# Terraform automation for COVID19 scraper

### Description
Create necessary resources to deploy serverless COVID19 scraper.

Creates S3 bucket, CDN, DNS records, IAM policies, Lambda functions.

### Usage
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
