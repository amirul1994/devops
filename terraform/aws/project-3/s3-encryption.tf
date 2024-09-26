resource "aws_s3_bucket_server_side_encryption_configuration" "thinking_place_encryption" {
  bucket = aws_s3_bucket.thinking_place.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}