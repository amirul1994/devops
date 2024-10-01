resource "aws_s3_object" "index_html_dev" {
    bucket = aws_s3_bucket.website_dev.id 
    key = "index.html"
    source = "index.html"
    content_type = "text/html"
} 

resource "aws_s3_object" "error_html_dev" {
    bucket = aws_s3_bucket.website_dev.id
    key = "error.html"
    source = "error.html"
    content_type = "text/html"
} 

resource "aws_s3_object" "index_html_staging" {
    bucket = aws_s3_bucket.website_prod.id
    key = "index.html" 
    source = "index.html"
    content_type = "text/html"
} 

resource "aws_s3_object" "error_html_staging" {
    bucket = aws_s3_bucket.website_staging.id 
    key = "error.html" 
    source = "error.html"
    content_type = "text/html"
} 

resource "aws_s3_object" "index_html_prod" {
    bucket = aws_s3_bucket.website_prod.id 
    key = "index.html"
    source = "index.html" 
    content_type = "text/html"
} 

resource "aws_s3_object" "error_html_prod" {
    bucket = aws_s3_bucket.website_prod.id 
    key = "error.html"
    source = "error.html"
    content_type = "text/html"
}