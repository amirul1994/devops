resource "aws_s3_access_point" "thinking_place_access_point" {
  bucket = aws_s3_bucket.thinking_place.id
  name   = "thinking-place-access-point"
}