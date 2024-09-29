resource "aws_s3_bucket" "website_prod" {
    bucket = "my-website-prod-1000"

    tags = {
        Name = "my-website-prod"
        Environment = "prod"
    }
} 

resource "aws_s3_bucket_lifecycle_configuration" "website_prod_lifecycle" {
    bucket = aws_s3_bucket.website_prod.bucket 

    rule {
        id = "prod-lifecycle-rule"

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

resource "aws_s3_bucket_versioning" "prod_bucket_versioning" {
    bucket = aws_s3_bucket.website_prod.bucket 

    versioning_configuration {
        status = "Enabled"
    }
}

resource "aws_s3_bucket_website_configuration" "website_hosting_prod" {
    bucket = aws_s3_bucket.website_prod.bucket

    index_document {
        suffix = "index.html"
    } 

    error_document {
        key = "error.html"
    }

} 

resource "aws_s3_bucket_public_access_block" "website_prod_public_access" {
    bucket = aws_s3_bucket.website_prod.id 

    block_public_policy = false
}

resource "aws_s3_bucket_policy" "website_prod_policy" {
    bucket = aws_s3_bucket.website_prod.id 

    policy = jsonencode ({
        Version = "2012-10-17",
        Statement = [
            {
                Sid = "PublicReadGetObject",
                Effect = "Allow",
                Principal = "*",
                Action = "s3:GetObject",
                Resource = "${aws_s3_bucket.website_prod.arn}/*"
            }
        ]
    })
}

output "bucket_website_url_prod" {
    value = aws_s3_bucket_website_configuration.website_hosting_prod.website_endpoint
} 