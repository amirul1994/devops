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