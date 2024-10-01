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


resource "aws_s3_bucket_policy" "website_dev_policy" {
    bucket = aws_s3_bucket.website_dev.id 

    policy = jsonencode ({
        Version = "2012-10-17", 
        
        Statement = [
            {
                Sid = "FullBucketAccess",
                Effect = "Allow",
                Principal = {
                    "AWS": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
                },
                Action = [
                          "s3:GetObject",
                          "s3:PutObject",
                          "s3:PutObjectAcl",
                          "s3:DeleteObject",
                        ],
                
                Resource = [
                    "${aws_s3_bucket.website_dev.arn}/*",
                    "${aws_s3_bucket.website_dev.arn}"
                ]
            }
        ]
    })
}

resource "aws_s3_bucket_logging" "website_dev_logging" {
    bucket = aws_s3_bucket.website_dev.id

    target_bucket = aws_s3_bucket.website_log.bucket 
    target_prefix = "dev-log/"
}

output "bucket_website_url_dev" {
    value = aws_s3_bucket_website_configuration.website_hosting_dev.website_endpoint
}