output "alb_vpc1_dns" {
    value = module.alb_vpc1.alb_dns_name
} 

output "alb_vpc2_dns" {
    value = module.alb_vpc2.alb_dns_name
}