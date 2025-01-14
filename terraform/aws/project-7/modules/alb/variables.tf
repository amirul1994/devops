variable "vpc_id" {}

variable "subnets" {
    type = list(string)
} 

variable "target_id" {}

variable "alb_name" {}