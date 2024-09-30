resource "aws_cloudfront_distribution" "website_prod_distribution" {
    origin {
        domain_name = aws_s3_bucket.website_prod.bucket_regional_domain_name
        
        origin_id = aws_s3_bucket.website_prod.id

        custom_origin_config {
          http_port = 80
          https_port = 443 
          origin_protocol_policy = "http-only" 
          origin_ssl_protocols = ["TLSv1.2"]
        }
   }

   enabled = true 
   
   is_ipv6_enabled = false 
   
   default_root_object = "index.html"

   default_cache_behavior {
    allowed_methods = ["GET", "HEAD"]
    cached_methods = ["GET", "HEAD"]
    target_origin_id = aws_s3_bucket.website_prod.id

    forwarded_values {
        query_string = false

        cookies {
            forward = "none"
        }
    }

    viewer_protocol_policy = "redirect-to-https"
    
    min_ttl = 0
    
    default_ttl = 3600
    
    max_ttl = 86400
   } 

   restrictions {
    geo_restriction {
        restriction_type = "none" 
    }
   }
   
   viewer_certificate {
    cloudfront_default_certificate = true
   } 

   tags = {
    Name = "my-website-prod-1000"
   }
} 


resource "null_resource" "invalidate_cache" {
    
    triggers = {
        distribution_id = aws_cloudfront_distribution.website_prod_distribution.id
    } 
    
    provisioner "local-exec" {
        command = "./invalidate_cache.sh ${aws_cloudfront_distribution.website_prod_distribution.id}"
    }

    depends_on = [aws_cloudfront_distribution.website_prod_distribution]

}