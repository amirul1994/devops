resource "aws_s3_bucket" "website_staging" {
    bucket = "my-website-staging-1000"
    
    tags = {
        Name = "my-website-staging"
        Environment = "staging"
    }
} 

resource "aws_s3_bucket_lifecycle_configuration" "website_staging_lifecycle" {
    bucket = aws_s3_bucket.website_staging.bucket
    
    rule {
        id = "staging-lifecycle-rule"

        transition {
            days = 30 
            storage_class = "STANDARD_IA"
        } 

        expiration {
            days = 90
        } 

        status = "Enabled"
    }
} 

resource "aws_s3_bucket_versioning" "website_staging_versioning" {
    bucket = aws_s3_bucket.website_staging.bucket 

    versioning_configuration {
        status = "Enabled"
    }
}

resource "aws_s3_bucket_website_configuration" "website_hosting_staging" {
    bucket = aws_s3_bucket.website_staging.bucket

    index_document {
        suffix = "index.html"
    } 

    error_document {
        key = "error.html"
    }
} 

output "bucket_website_url_staging" {
    value = aws_s3_bucket_website_configuration.website_hosting_staging.website_endpoint
}