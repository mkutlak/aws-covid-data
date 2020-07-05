variable "aws_region" {
  description = "Main AWS region."
  default     = "eu-central-1"
}

variable "aws_credentials_file" {
  description = "Path to stored credentials for AWS."
}

variable "aws_credentials_profile" {
  description = "Profile selected in credentials file."
  default     = "mkutlak"
  type        = string
}

variable "domain_name" {
  default = "themkutlak.eu"
  type    = string
}

variable "website_bucket_name" {
  default = "covid19.themkutlak.eu"
  type    = string
}

variable "hosted_zone_domain_name" {
  default = "themkutlak.eu."
  type    = string
}
