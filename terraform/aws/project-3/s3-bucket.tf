resource "aws_s3_bucket" "thinking_place" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_public_access_block" "thinking_place_public_access_block" {
  bucket = aws_s3_bucket.thinking_place.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "thinking_place_policy" {
  bucket = aws_s3_bucket.thinking_place.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = "*",
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = [
          "${aws_s3_bucket.thinking_place.arn}/*"
        ]
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.thinking_place_public_access_block]
}