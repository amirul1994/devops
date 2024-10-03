resource "aws_s3_bucket_replication_configuration" "thinking_place_replication" {
  bucket = aws_s3_bucket.thinking_place.id

  role = aws_iam_role.replication.arn

  rule {
    id     = "replication-rule"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.replication_bucket.arn
      storage_class = "STANDARD"
    }
  }

    depends_on = [
      aws_s3_bucket_versioning.thinking_place_versioning,
      aws_s3_bucket_versioning.replication_bucket_versioning
    ]
}

resource "aws_iam_role" "replication" {
  name = "s3-replication-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "s3.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_s3_bucket" "replication_bucket" {
  bucket = "thinking-place-replication"
}