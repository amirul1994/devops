output "route53_zone_id" {
    value = aws_route53_zone.this.zone_id
}


output "route53_record_vpc1_id" {
    value = aws_route53_record.this_vpc1.id 
} 

output "route53_record_vpc2_id" {
    value = aws_route53_record.this_vpc2.id
}