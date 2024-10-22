## Project Overview ##:

### Title: 

High Availability Web Application with Application Load Balancer (ALB) and Autoscaling on AWS using Terraform

### Objective:

Deploy a web application (e.g., Nginx or Apache) on EC2 instances behind an Application Load Balancer (ALB) with autoscaling for high availability and fault tolerance.

### Architecture:

1. VPC: A Virtual Private Cloud with multiple subnets across at    least two Availability Zones (AZs).
    
2. ALB: An Application Load Balancer to distribute traffic across multiple EC2 instances.
    
3. Autoscaling Group: Automatically scales EC2 instances based on load.
    
4. Security Groups: Allow traffic on ports 80 (HTTP) and 443 (HTTPS) for ALB, and appropriate ports for EC2 instances.