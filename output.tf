output "website_endpoint" {
  description = "domain name of the bucket"
  value       = aws_s3_bucket.website.website_endpoint
}

# output "r53_website_endpoint" {
#   description = "Website FQDN"
#   value       = aws_route53_record.main-a-record.fqdn
# }