resource "aws_iam_user" "kk_labs_user_751906" {
  name = "kk_labs_user_751906"
}

resource "aws_iam_user_policy" "kk_labs_user_policy" {
  user = aws_iam_user.kk_labs_user_751906.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutBucketPolicy",
          "s3:GetBucketPolicy",
          "s3:PutBucketReplication",
          "s3:GetBucketReplication",
          "iam:PassRole"
        ],
        Resource = [
          "arn:aws:s3:::thinking-place",
          "arn:aws:iam::211125603807:role/s3-replication-role"
        ]
      }
    ]
  })
}