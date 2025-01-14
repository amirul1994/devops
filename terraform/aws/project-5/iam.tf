resource "aws_iam_role" "rds_iam_role" {
    name = "rds_iam_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "rds.amazonaws.com"
                }
            }
        ]
    })
} 

resource "aws_iam_policy_attachment" "rds_iam_policy_attachment" {
    name = "rds_iam_policy_attachment"
    roles = [aws_iam_role.rds_iam_role.name]
    policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
} 


resource "aws_iam_policy" "rds_custom_policy" {
    name = "rds_custom_policy"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Action = [
                    "rds:DeleteDBSubnetGroup",
                    "rds:CreateDBSubnetGroup",
                    "rds:DescribeDBSubnetGroups",
                    "rds:GrantDBPrivileges"
                ],
                Resource = "*"
            }
        ]
    })
} 

resource "aws_iam_policy_attachment" "rds_custom_policy_attachment" {
    name = "rds_custom_policy_attachment"
    roles = [aws_iam_role.rds_iam_role.name]
    policy_arn = aws_iam_policy.rds_custom_policy.arn
} 


# data "aws_caller_identity" "current" {}


# resource "aws_secretsmanager_secret" "rds_secret" {
#   name        = "rds_password_secret"
#   description = "RDS password secret for the application"
# }


# resource "aws_iam_policy" "secrets_manager_access" {
#   name = "secrets_manager_access"

#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Action = [
#           "secretsmanager:DescribeSecret",
#           "secretsmanager:GetSecretValue",
#           "secretsmanager:ListSecrets",
#           "secretsmanager:PutSecretValue"
#         ],
#         Resource = aws_secretsmanager_secret.rds_secret.arn  # Change Resource to specific secret ARN
#       }
#     ]
#   })
# } 


# resource "aws_iam_policy_attachment" "secrets_manager_policy_attachment" {
#   name       = "secrets_manager_policy_attachment"
#   policy_arn = aws_iam_policy.secrets_manager_access.arn
#   users      = [data.aws_caller_identity.current.user_id]
# }


# resource "aws_secretsmanager_secret_policy" "secret_policy" {
#   secret_arn = aws_secretsmanager_secret.rds_secret.arn

#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Principal = {
#           AWS = data.aws_caller_identity.current.arn
#         },
#         Action = [
#           "secretsmanager:DescribeSecret",
#           "secretsmanager:GetSecretValue"
#         ],
#         Resource = aws_secretsmanager_secret.rds_secret.arn
#       }
#     ]
#   })
# }
