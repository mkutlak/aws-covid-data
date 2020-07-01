#AWS S3 (Storage)
# Create bucket to store COVID19 data and static webapp
resource "aws_s3_bucket" "website" {
  bucket = var.website_bucket_name
  acl    = "public-read"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${var.website_bucket_name}/*"
    }
  ]
}
EOF

  website {
    index_document = "index.html"
  }
}

#AWS ACM
# Get a SSL certificate 
data "aws_acm_certificate" "main" {
  provider = aws.us_east
  domain   = var.domain_name
  statuses = ["ISSUED"]
  types    = ["AMAZON_ISSUED"]

}


#AWS CloudFront (CDN)
# Define origin for S3
locals {
  s3_origin_id = "s3-covid-website"
}

# Create CF distribution
resource "aws_cloudfront_distribution" "main_dist" {
  origin {
    domain_name = aws_s3_bucket.website.bucket_domain_name
    origin_id   = local.s3_origin_id
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  aliases = [var.website_bucket_name]

  viewer_certificate {
    acm_certificate_arn = data.aws_acm_certificate.main.arn
    ssl_support_method  = "sni-only"
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = local.s3_origin_id
    viewer_protocol_policy = "allow-all"
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  depends_on = [aws_s3_bucket.website]
}

#AWS Route53 (DNS records)
# Get info about hosted zone 
data "aws_route53_zone" "main" {
  name = var.hosted_zone_domain_name
}

# Create Route53 "A" record for covid19 web
resource "aws_route53_record" "main-a-record" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "covid19.${data.aws_route53_zone.main.name}"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.main_dist.domain_name
    zone_id                = aws_cloudfront_distribution.main_dist.hosted_zone_id
    evaluate_target_health = false
  }

  depends_on = [aws_cloudfront_distribution.main_dist]
}

# Create Route53 "AAAA" record for covid19 web
resource "aws_route53_record" "main-aaaa-record" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "covid19.${data.aws_route53_zone.main.name}"
  type    = "AAAA"

  alias {
    name                   = aws_cloudfront_distribution.main_dist.domain_name
    zone_id                = aws_cloudfront_distribution.main_dist.hosted_zone_id
    evaluate_target_health = false
  }
  depends_on = [aws_cloudfront_distribution.main_dist]
}

#AWS IAM
# TODO: FIX ME, policy role attaching
# Create IAM role for Lambda function to enable working with S3
resource "aws_iam_role" "covid_lambda_s3_role" {
  name               = "covid-lambda-s3-role"
  description        = "Enable Lambda function to work with S3."
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:*"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::*"
        }
    ]
}
EOF
}

#AWS Lambda (Serverless)
# Create Lambda layer for COVID19 app.
resource "aws_lambda_layer_version" "covid_layer" {
  layer_name          = "covid-scraper-with-pandas-layer"
  filename            = "../src/python.zip"
  compatible_runtimes = ["python3.8"]
}

# Create Lambda function that scrapes COVID19 data to S3.
resource "aws_lambda_function" "covid_lambda_function" {
  function_name = "covid19-lambda-scraper"
  filename      = "../src/lambda.zip"
  handler       = "lambda_handler"
  role          = aws_iam_role.covid_lambda_s3_role.arn
  runtime       = "python3.8"

  depends_on = [aws_iam_role.covid_lambda_s3_role]
}

#AWS CloudWatch (Log/Monitor/Schedule)
#TODO: Add cron, trigger on putobject
