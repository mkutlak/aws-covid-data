output "website_endpoint" {
  description = "Domain name of the bucket"
  value       = aws_s3_bucket.website.website_endpoint
}