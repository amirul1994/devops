  ![aws project](https://github.com/user-attachments/assets/f223b427-70fd-43a8-a6cc-e6f691bf70e3)
 

## KubeDeploy: Multi-Tier App with Terraform, Ansible & CI/CD in EKS Cluster

I will use the Application Load Balancer on the public subnet in multiple zones for high availability and fault tolerance. The private subnet will host the Webserver, RDS, and EKS Cluster. The Frontend will be deployed on ec2  instances with auto-scaling enabled, and RDS (MySQL) will be used as the database.

The backend will be hosted on the EKS cluster with different frameworks (NodeJS, Flask, Springboot, and .Net). The rest of the components that will be placed on the EKS cluster are Jenkins, ArgoCD, Prometheus, Grafana, and EFK. The demonstration of Continuous Integration (CI), and Continuous Delivery, Continuous Deployment (CD) will be executed using Jenkins & ArgoCD. In the EKS cluster, an Ingress controller will manage service discovery and enable proper routing between the  EKS cluster, and the outside world.

The task of observability will be done by implementing Prometheus, Grafana, and EFK (Elastic, Fluentd, Kibana) for log management. For image and report storage, S3 object storage will be used with proper lifecycle policy. As CDN, CloudFront will be used and for DNS management I will leverage Route53.

Terraform will handle infrastructure provisioning, meanwhile, Ansible will manage configuration in the AWS environment.
