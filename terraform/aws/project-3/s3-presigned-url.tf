resource "aws_s3_object" "thinking_place_object" {
  bucket = aws_s3_bucket.thinking_place.id
  key    = "example"
  source = "example.txt"
}

resource "aws_s3_object" "thinking_place_presigned_url" {
  bucket = aws_s3_bucket.thinking_place.id
  key    = "presigned-url-object"
  source = "presigned-url-object.txt"
}

resource "null_resource" "generate_presigned_url" {
  provisioner "local-exec" {
    command = "aws s3 presign s3://${aws_s3_bucket.thinking_place.id}/${aws_s3_object.thinking_place_presigned_url.key}"
  }

  triggers = {
    object_key = aws_s3_object.thinking_place_presigned_url.key
  }
}

output "presigned_url" {
  value = "aws s3 presign s3://${aws_s3_bucket.thinking_place.id}/${aws_s3_object.thinking_place_presigned_url.key}"
}