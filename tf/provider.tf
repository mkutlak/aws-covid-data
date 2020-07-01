# Default provider
provider "aws" {
  region                  = var.aws_region
  shared_credentials_file = var.aws_credentials_file
  profile                 = var.aws_credentials_profile
}

# Provider for us-east-1 region for ACM (Certificate Management)
# us-east-1 is required for certification
provider "aws" {
  alias                   = "us_east"
  region                  = "us-east-1"
  shared_credentials_file = var.aws_credentials_file
  profile                 = var.aws_credentials_profile
}