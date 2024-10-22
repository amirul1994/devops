resource "aws_lb" "alb" {
    name = "my-alb"
    internal = false
    load_balancer_type = "application"
    security_groups = [aws_security_group.alb_sg.id]
    subnets = aws_subnet.public[*].id
} 

resource "aws_lb_target_group" "tg" {
    name = "my-target-group"
    port = 80
    protocol = "HTTP"
    vpc_id = aws_vpc.my_vpc.id
    health_check {
        path = "/"
        interval = 30 
        timeout = 5
    }
} 

resource "aws_lb_listener" "http" {
    load_balancer_arn = aws_lb.alb.arn 
    port = 80
    protocol = "HTTP"

    default_action {
        type = "forward"
        target_group_arn = aws_lb_target_group.tg.arn
    }
}