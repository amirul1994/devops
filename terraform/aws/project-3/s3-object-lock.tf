resource "aws_s3_bucket_object_lock_configuration" "thinking_place_object_lock" {
  bucket = aws_s3_bucket.thinking_place.id

  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = 5
    }
  }

  depends_on = [aws_s3_bucket_versioning.thinking_place_versioning]
}