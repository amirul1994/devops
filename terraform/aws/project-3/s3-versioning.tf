resource "aws_s3_bucket_versioning" "thinking_place_versioning" {
  bucket = aws_s3_bucket.thinking_place.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "replication_bucket_versioning" {
  bucket = aws_s3_bucket.replication_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}