provider "aws" {
    region = "us-east-1"
} 

data "aws_caller_identity" "current" {}

module "cloudwatch_s3_monitoring" {
    source = "./cloudwatch"

    s3_buckets = {
        dev = aws_s3_bucket.website_dev.arn 
        staging = aws_s3_bucket.website_staging.arn
        prod = aws_s3_bucket.website_prod.arn
    }
}