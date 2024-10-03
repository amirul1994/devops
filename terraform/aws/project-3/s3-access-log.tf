resource "aws_s3_bucket" "access_log_bucket" {
  bucket = "thinking-place-access-logs"
}

resource "aws_s3_bucket_logging" "thinking_place_logging" {
  bucket = aws_s3_bucket.thinking_place.id

  target_bucket = aws_s3_bucket.access_log_bucket.id
  target_prefix = "log/"
}