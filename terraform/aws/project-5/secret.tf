# resource "aws_secretsmanager_secret" "rds_secret" {
#     name = "rds_password_secret"
# } 

# resource "random_password" "rds_password" {
#     length = 20
#     special = true
# }

# resource "aws_secretsmanager_secret_version" "rds_secret_version" {
#     secret_id = aws_secretsmanager_secret.rds_secret.id
#     secret_string = jsonencode({
#         username = "admin"
#         password = random_password.rds_password.result 
#     })
# } 