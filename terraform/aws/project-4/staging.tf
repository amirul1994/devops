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


resource "aws_s3_bucket_policy" "website_staging_policy" {
    bucket = aws_s3_bucket.website_staging.id 

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
                    "${aws_s3_bucket.website_staging.arn}/*",
                    "${aws_s3_bucket.website_staging.arn}"
                    ]
            }
        ]
    })
} 

resource "aws_s3_bucket_logging" "website_staging_logging" {
    bucket = aws_s3_bucket.website_staging.id 

    target_bucket = aws_s3_bucket.website_log.bucket 
    target_prefix = "staging-log/"
}

resource "aws_s3_object" "sample2_object" {
    bucket = aws_s3_bucket.website_staging.bucket
    key = "sample/sample.txt"
    source = "sample2.txt"
}

output "bucket_website_url_staging" {
    value = aws_s3_bucket_website_configuration.website_hosting_staging.website_endpoint
}