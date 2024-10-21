# data "aws_db_instance" "db_instance" {
#     db_instance_identifier = aws_db_instance.mysql_rds.id
# }

# resource "null_resource" "ssh_bastion" {
#     depends_on = [aws_instance.bastion]

#     connection {
#         type = "ssh"
#         user = "ubuntu"
#         host = aws_instance.bastion.public_ip
#         private_key = file("${path.module}/bastion-key.pem")
#     }

#     provisioner "remote-exec" {
#         inline = [
#             "sudo apt update -y",
#             "sudo apt install mysql-client -y",
#             # "export RDS_PASSWD='${var.rds_passwd}'"
#         ]
#     }
# } 