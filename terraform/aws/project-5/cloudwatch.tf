resource "aws_cloudwatch_metric_alarm" "database_connections_alarm" {
    alarm_name = "HighDatabaseConnections"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = "1"
    metric_name = "DatabaseConnections"
    namespace = "AWS/RDS"
    period = "60"
    statistic = "Average"
    threshold = "150"
    dimensions = {
        DBInstanceIdentifier = aws_db_instance.mysql_rds.id
    }
    alarm_actions = [aws_sns_topic.alarm_notifications.arn]

}

resource "aws_cloudwatch_metric_alarm" "replication_status_alarm" {
    alarm_name = "ReplicationStatusAlarm"
    comparison_operator = "GreaterThanThreshold"
    evaluation_periods = "1"
    metric_name = "ReplicaLag"
    namespace = "AWS/RDS"
    period = "60"
    statistic = "Maximum"
    threshold = "180"
    dimensions = {
        DBInstanceIdentifier = aws_db_instance.mysql_rds.id
    }
    alarm_actions = [aws_sns_topic.alarm_notifications.arn]
}