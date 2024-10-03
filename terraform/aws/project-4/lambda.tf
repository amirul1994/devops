resource "aws_iam_role" "lambda_exec_role" {
    name = "lambda_exec_role"

    assume_role_policy = jsonencode ({
        "Version" : "2012-10-17",
        "Statement" : [{
            "Action" : "sts:AssumeRole",
            "Principal" : {
                "Service" : "lambda.amazonaws.com"
            },
            "Effect" : "Allow",
            "Sid" : ""
        }]
    })
} 

resource "aws_iam_policy" "lambda_policy" {
    name = "lambda_policy"
    description = "Lambda policy for reading from S3 and writing to CloudWatch"
    policy = jsonencode({
        "Version" : "2012-10-17",
        "Statement": [
            {
                "Effect" : "Allow",
                "Action" : [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],

                "Resource" : "arn:aws:logs:*:*:*"
            },
            
            {
                "Effect" : "Allow",
                "Action" : [
                    "s3:GetObject"
                ],

                "Resource" : "arn:aws:s3:::website_log/*"
            }
        ]
    })
} 

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
    role = aws_iam_role.lambda_exec_role.name 
    policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_lambda_function" "process_s3_logs" 