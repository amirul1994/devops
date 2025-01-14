## Project Overview

## Title:

High Availability Web Application with Application Load Balancer (ALB) and Autoscaling on AWS using Terraform

## Objective:

Deploy a web application (e.g., Nginx or Apache) on EC2 instances behind an Application Load Balancer (ALB) with autoscaling for high availability and fault tolerance.

## Architecture:

## VPC:

A Virtual Private Cloud with multiple subnets across at least two Availability Zones (AZs).

Each VPC will have:

a. Two public subnets for the ALB.

b. One private subnet for the EC2 instances.

c. NAT Gateways in the public subnets to allow outbound internet access for the EC2 instances in the private subnets.

## ALB:

An Application Load Balancer to distribute traffic across multiple EC2 instances.The ALB will be placed in the public subnets and will forward traffic to the EC2 instances in the private subnets. The ALB will have a listener on port 80 (HTTP) and will forward traffic to the target group.

## EC2 Instances:

EC2 instances will be placed in the private subnets.Each VPC will have one EC2 instance in the private subnet. The EC2 instances will run a web server (e.g., Apache) and will serve a simple HTML page displaying server details.

## Security Groups:

Allow traffic on port 80 (HTTP) for the ALB. Allow traffic on ports 22 (SSH) and 80 (HTTP) for the EC2 instances.

## Route 53:

A weighted routing policy in Route 53 to distribute traffic between the two ALBs based on specified weights.

## Terraform Modules:

- VPC Module: To create VPCs, subnets, NAT Gateways, and Internet Gateways.

- EC2 Module: To create EC2 instances in the private subnets.

- ALB Module: To create Application Load Balancers and their associated Target Groups.

- Route 53 Module: To create a weighted routing policy in Route 53.