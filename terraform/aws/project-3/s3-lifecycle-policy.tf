resource "aws_s3_bucket_lifecycle_configuration" "thinking_place_lifecycle" {
  bucket = aws_s3_bucket.thinking_place.id

  rule {
    id     = "expire-noncurrent-objects"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}