resource "aws_s3_bucket" "website_dev" {
    bucket = "my-website-dev-1000"

    tags = {
        Name = "my-website-dev"
        Environment = "dev"
    }
}  

resource "aws_s3_bucket_lifecycle_configuration" "website_dev_lifecycle" {
    bucket = aws_s3_bucket.website_dev.bucket
    
    rule {
        id = "dev-lifecycle-rule"

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

resource "aws_s3_bucket_versioning" "website_dev_versioning" {
    bucket = aws_s3_bucket.website_dev.bucket 

    versioning_configuration {
        status = "Enabled"
    }
}

resource "aws_s3_bucket_website_configuration" "website_hosting_dev" {
    bucket = aws_s3_bucket.website_dev.bucket 

    index_document {
        suffix = "index.html"
    } 

    error_document {
        key = "error.html"
    }
} 

output "bucket_website_url_dev" {
    value = aws_s3_bucket_website_configuration.website_hosting_dev.website_endpoint
}