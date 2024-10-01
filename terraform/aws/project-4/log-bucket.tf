resource "aws_s3_bucket" "website_log" {
    bucket = "my-website-log-1000"

    tags = {
        Name = "my-website-log"
        Environment = "log"
    } 
} 

resource "aws_s3_bucket_versioning" "log_bucket_versioning" {
    bucket = aws_s3_bucket.website_log.bucket 

    versioning_configuration {
        status = "Enabled"
    }
} 

resource "aws_s3_bucket_acl" "website_log_acl" {
    bucket = aws_s3_bucket.website_log.id
    acl = "log-delivery-write"
}

resource "aws_s3_bucket_policy" "website_log_policy" {
    bucket = aws_s3_bucket.website_log.id 

    policy = jsonencode ({
        Version = "2012-10-17",

        Statement = [
            {
                Effect = "Allow",
                
                Principal = {
                    Service = "cloudfront.amazonaws.com"
                }, 

                Action = "s3:PutObject",

                Resource = "${aws_s3_bucket.website_log.arn}/*"

                Condition = {
                    StringEquals = {
                        "aws:SourceArn" = "arn:aws:cloudfront::${data.aws_caller_identity.current.account_id}:distribution/${aws_cloudfront_distribution.website_prod_distribution.id}"
                    }
                }
            }, 
            
            {
                Effect = "Allow",
                Principal = {
                    Service = "cloudfront.amazonaws.com"
                }, 
            
                Action = "s3:GetBucketAcl",
                Resource = aws_s3_bucket.website_log.arn
            }, 

            {
                Effect = "Allow",
                Principal = {
                    AWS = "*"
                }, 

                Action = "s3:PutObject",
                Resource = "${aws_s3_bucket.website_log.arn}/*",
                Condition = {
                    ArnLike = {
                        "aws:SourceArn" = [
                            "arn:aws:s3:::website_dev",
                            "arn:aws:s3:::website_staging",
                            "arn:aws:s3:::website_prod"
                        ]
                    }
                }
            }
        ]
    })
}

resource "aws_s3_bucket_public_access_block" "website_log_public_access" {
    bucket = aws_s3_bucket.website_log.id 

    block_public_policy = true 
    block_public_acls = true 
    ignore_public_acls = true 
    restrict_public_buckets = true
} 

resource "aws_s3_bucket_ownership_controls" "website_log_ownership" {
    bucket = aws_s3_bucket.website_log.id 

    rule {
        object_ownership = "BucketOwnerPreferred"
    }
}