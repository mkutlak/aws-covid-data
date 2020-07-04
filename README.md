# Terraform automation for COVID19 scraper

### Description
Create necessary resources to deploy serverless COVID19 scraper.

Creates S3 bucket, CDN, DNS records, IAM policies, Lambda functions.

### Usage
To plan the deployment:
```bash
$ cd ../src ; make
$ cd -
$ terraform plan
```

To deploy the serverless app:
```bash
$ cd ../src ; make
$ cd -
$ terraform apply 
```

To destroy the app:
```bash
$ terrafrom destroy
$ cd ../src ; make clean
$ cd - 
```