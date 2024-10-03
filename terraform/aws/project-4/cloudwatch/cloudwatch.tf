variable "s3_buckets" {
    description = "map of s3 bucket arns for dev, staging and prod"
    type = map(string)
}

variable "cloudfront_distribution_id" {
    description = "CloudFront Distribution ID"
    type = string
}

resource "aws_cloudwatch_metric_alarm" "s3_bucket_size_bytes_alarm" {
    for_each = var.s3_buckets
    alarm_name = "${each.key}_BucketSizeBytes_Alarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = "BucketSizeBytes"
    namespace = "AWS/S3"
    statistic = "Average"
    period = 86400 
    threshold = 5000000000 
    dimensions = {
        BucketName = each.value
        StorageType = "StandardStorage"
    } 

    alarm_description = "Alarm when the bucket size exceeds 5GB"
} 

resource "aws_cloudwatch_metric_alarm" "s3_number_of_objects_alarm" {
    for_each = var.s3_buckets
    alarm_name = "${each.key}_NumberOfObjects_Alarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = "NumberOfObjects"
    namespace = "AWS/S3"
    statistic = "Average"
    period = 86400 
    threshold = 1000
    dimensions = {
        BucketName = each.value
        StorageType = "AllStorageTypes"
    }

    alarm_description = "Alarm when the number of objects exceeds 1000"
} 

resource "aws_cloudwatch_metric_alarm" "s3_all_requests_alarm" {
    for_each = var.s3_buckets 
    alarm_name = "${each.key}_AllRequests_Alarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "AllRequests"
    namespace = "AWS/S3"
    statistic = "Sum"
    period = 120 
    threshold = 300 
    dimensions = {
        BucketName = each.value
    }

    alarm_description = "Alarm when the total requests exceed 300 in 2 minutes" 
} 

resource "aws_cloudwatch_metric_alarm" "s3_4xx_errors_alarm" {
    for_each = var.s3_buckets 
    alarm_name = "${each.key}_4xxErrors_Alarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "4xxErrors"
    namespace = "AWS/S3"
    statistic = "Sum"
    period = 300
    threshold = 50
    dimensions = {
        BucketName = each.value
    } 

    alarm_description = "Alarm when 4xx errors exceed 50 in 5 minutes"
} 

resource "aws_cloudwatch_metric_alarm" "s3_5xx_erros_alarm" {
    for_each = var.s3_buckets 
    alarm_name = "${each.key}_5xxErrors_Alarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = "5xxErrors"
    namespace = "AWS/S3"
    statistic = "Sum"
    period = 300
    threshold = 10
    dimensions = {
        BucketName = each.value
    }

    alarm_description = "Alarm when 5xx errors exceed 10 in 5 minutes"
} 

resource "aws_cloudwatch_metric_alarm" "s3_first_byte_latency_alarm" {
    for_each = var.s3_buckets
    alarm_name = "${each.key}_FirstByteLatency_Alarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = "FirstByteLatency"
    namespace = "AWS/S3"
    statistic = "Average"
    period = 300 
    threshold = 1 
    dimensions = {
        BucketName = each.value
    }

    alarm_description = "Alarm when the first byte latency exceeds 1 second"
} 

resource "aws_cloudwatch_metric_alarm" "s3_total_request_latency_alarm" {
    for_each = var.s3_buckets
    alarm_name = "${each.key}_TotalRequestLatency_Alarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = "TotalRequestLatency"
    namespace = "AWS/S3"
    statistic = "Average"
    period = 60 
    threshold = 2 
    dimensions = {
        BucketName = each.value
    } 

    alarm_description = "Alarm when the total requets latency exceeds 2 seconds"
} 

resource "aws_cloudwatch_metric_alarm" "s3_request_alarm" {
    for_each = var.s3_buckets 
    alarm_name = "${each.key}_GetRequests_Alarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = "GetRequests"
    namespace = "AWS/S3"
    statistic = "Sum"
    period = 300
    threshold = 1000
    dimensions = {
        BucketName = each.key
    } 

    alarm_description = "Alarm when GET requests exceeds 1000 in 5 minutes"
} 

resource "aws_cloudwatch_metric_alarm" "s3_put_request_alarm" {
    for_each = var.s3_buckets
    alarm_name = "${each.key}_PutRequests_Alarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = "PutRequests"
    namespace = "AWS/S3"
    statistic = "Sum"
    period = 300
    threshold = 1000 
    dimensions = {
        BucketName = each.key
    } 

    alarm_description = "Alarm when PUT requests exceed 1000 in 5 minutes"
} 

resource "aws_cloudwatch_metric_alarm" "s3_delete_request_alarm" {
    for_each = var.s3_buckets
    alarm_name = "${each.key}_DeleteRequests_Alarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = "DeleteRequests"
    namespace = "AWS/S3"
    statistic = "Sum"
    period = 300
    threshold = 100 
    dimensions = {
        BucketName = each.key
    }

    alarm_description = "Alarm when DELETE requests exceed 100 in 5 minutes"
}

resource "aws_cloudwatch_metric_alarm" "cloudfront_cache_hit_rate_alarm" {
    alarm_name = "CloudFrontCacheHitRateAlarm"
    comparison_operator = "LessThanThreshold"
    evaluation_periods = 1
    metric_name = "CacheHitRate"
    namespace = "AWS/CloudFront"
    period = 300 
    statistic = "Average"
    threshold = 80 
    dimensions = {
        DistributionId = var.cloudfront_distribution_id
        Region = "Global"
    }

    alarm_description = "Alarm when CloudFront cache hit rate falls below 80%"
}

resource "aws_cloudwatch_metric_alarm" "cloudfront_origin_latency_alarm" {
    alarm_name = "CloudFrontOriginalLatencyAlarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = 1
    metric_name = "OriginLatency"
    namespace = "AWS/CloudFront"
    period = 300
    statistic = "Average"
    threshold = 500 
    dimensions = {
        DistributionId = var.cloudfront_distribution_id
        Region = "Global"
    }

    alarm_description = "Alarm when CloudFront origin latency exceeds 500ms"
}