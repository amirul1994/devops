resource "aws_route53_zone" "this" {
    name = var.domain_name
}

resource "aws_route53_record" "this_vpc1" {
    zone_id = aws_route53_zone.this.zone_id
    name = var.domain_name
    type = "A"
    #ttl = 300 

    weighted_routing_policy {
        weight = var.weight_vpc1
    } 

    set_identifier = "vpc1"
    #records = [var.alb_vpc1_dns] 

    alias {
        name = var.alb_vpc1_dns
        zone_id = var.alb_vpc1_zone_id
        evaluate_target_health = true 
    }
} 

resource "aws_route53_record" "this_vpc2" {
    zone_id = aws_route53_zone.this.zone_id
    name = var.domain_name
    type = "A"
    #ttl = 300 

    weighted_routing_policy {
        weight = var.weight_vpc2
    }

    set_identifier = "vpc2"

    alias {
        name = var.alb_vpc2_dns
        zone_id = var.alb_vpc2_zone_id
        evaluate_target_health = true
    }
    #records = [var.alb_vpc2_dns]
} 

# data "aws_route53_zone" "selected" {
#     name = var.domain_name
# }