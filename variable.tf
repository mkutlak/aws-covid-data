variable "aws_region" {
  description = "Main AWS region."
  default     = "eu-central-1"
}

# Credentials
variable "aws_credentials_file" {
  description = "Path to stored credentials for AWS."
}

variable "aws_credentials_profile" {
  description = "Profile name to select in credentials file."
  type        = string
}

# S3, Route53, CloudFront
variable "domain_name" {
  default = "themkutlak.eu"
  type    = string
}

variable "website_bucket_name" {
  description = "Bucket space for website."
  default     = "covid19.themkutlak.eu"
  type        = string
}

variable "hosted_zone_domain_name" {
  description = "Route53 hosted zone."
  default     = "themkutlak.eu."
  type        = string
}

# Lambda
variable "cron_schedule" {
  description = "Cron scheduler for lambda function."
  default     = "cron(30 3 * * ? *)"
  type        = string
}
