# Terraform automation for COVID19 scraper
### learning project

![Terraform](https://github.com/mkutlak/aws-covid-data/workflows/Terraform/badge.svg)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/mkutlak/aws-covid-data.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mkutlak/aws-covid-data/alerts/)

### Description
Create necessary resources to deploy "Serverless" COVID19 scraper.

<p align="center">
<img src="https://github.com/mkutlak/aws-covid-data/blob/master/diagrams/covid19_scraper_web_app.png" height="480">
</p>

Creates the following resources:
#### S3 Bucket
The bucket is used to store scraped Covid-19 data from [CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19/) in a `data` dir and `index.html` that shows data for Czechia in a simple table.

The file structure:
``` bash
- data/
  - czechia_table.csv
  - MM-DD-YYYY.csv
- index.html
```

You can change the name of the bucket in `variable.tf` under `website_bucket_name` variable.

```
variable "website_bucket_name" {
  description = "Bucket space for website."
  default     = "covid19.themkutlak.eu"
  type        = string
}
```

#### IAM policy
The IAM policy defines permissions for Lambda function.

The Lambda function requires permission to `read`, `write` and `list` objects in S3.

#### Lambda layer
Because the `covid_scaper` is using `pandas` and `dominate` packages we have to create a Lambda layer and provide these packages there as well as the `covid_scraper` itself. 

```bash
$ cat src/requirements.txt
pandas==1.0.5
dominate==2.5.1
```
#### Lambda function
The Lamba function scrapes Covid-19 data in CSV format from [CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19/). The data is then saved to created S3 bucket. After that the Lambda function updates the index page table with the new data using data from Czechia only.

#### CloudWatch event
The event is used to trigger the Lambda function at regular intervals with a cron scheduler.

The cron is configurable with `cron_schedule` variable in `variable.tf`.
```
variable "cron_schedule" {
  description = "Cron scheduler for lambda function."
  default     = "cron(30 3 * * ? *)"
  type        = string
}
```

### Usage
Initiate Terraform:
```bash
$ make init
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
