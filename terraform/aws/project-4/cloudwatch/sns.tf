resource "aws_sns_topic" "cloudwatch_alerts" {
    name = "cloudwatch-alerts"
} 

resource "aws_sns_topic_policy" "cloudwatch_alerts_policy" {
    arn = aws_sns_topic.cloudwatch_alerts.arn
    policy = data.aws_iam_policy_document.cloudwatch_alerts_policy.json
} 

data "aws_iam_policy_document" "cloudwatch_alerts_policy" {
    statement {
        effect = "Allow"
        actions = ["SNS:Publish"]
        resources = [aws_sns_topic.cloudwatch_alerts.arn]

        principals {
            type = "Service"
            identifiers = ["cloudwatch.amazonaws.com"]
        }
    }
} 

resource "aws_sns_topic_subscription" "email_alert_subscription" {
    topic_arn = aws_sns_topic.cloudwatch_alerts.arn
    protocol = "email"
    endpoint = "mail@example.com"
} 

output "sns_topic_arn" {
    value = aws_sns_topic.cloudwatch_alerts.arn
}