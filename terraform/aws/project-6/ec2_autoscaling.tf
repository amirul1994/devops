resource "aws_launch_template" "my_launch_template" {
        name = "my-launch-template"

        image_id = "ami-0cad6ee50670e3d0e"
        instance_type = var.instance_type

        user_data = base64encode(<<-EOF
                    #!/bin/bash
                    sudo apt install -y nginx
                    sudo systemctl start nginx
                    sudo systemctl enable nginx
                    echo "hello from $(hostname -f)" > /var/www/html/index.html
                    EOF 
        )
        
        network_interfaces {
            associate_public_ip_address = false
            security_groups = [aws_security_group.ec2_sg.id]
        }
        
}

resource "aws_autoscaling_group" "my_asg" {
    desired_capacity = var.desired_capacity
    max_size = var.max_size
    min_size = var.min_size
    vpc_zone_identifier = aws_subnet.private[*].id
    launch_template {
        id = aws_launch_template.my_launch_template.id
    } 

    target_group_arns = [aws_lb_target_group.tg.arn]

    tag {
        key = "Name"
        value = "autoscaling-ec2"
        propagate_at_launch = true
    }
}