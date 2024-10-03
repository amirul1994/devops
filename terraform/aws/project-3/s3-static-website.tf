resource "aws_s3_bucket_website_configuration" "thinking_place_website" {
  bucket = aws_s3_bucket.thinking_place.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}