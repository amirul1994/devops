Project Title: "Multi-Environment Static Website Hosting with S3 and CloudFront"

Project Goal:

Create a multi-environment (e.g., development, staging, production) static website hosting solution using AWS S3, with content delivered through CloudFront for faster global access, all managed with Terraform.

Project Components:

S3 Buckets for Static Website Hosting:

Create separate S3 buckets for different environments (e.g., my-website-dev, my-website-staging, and my-website-prod).

Enable static website hosting for each bucket.
Set up appropriate bucket policies to make the website publicly accessible (or private if needed).

Versioning and Lifecycle Policies:

Enable versioning for all S3 buckets to ensure old versions of files can be retained.
Set up a lifecycle policy to automatically move older versions of files to a different storage class (e.g., Glacier) or delete them after a certain period.

CloudFront Distribution:

Create CloudFront distributions for each environment to serve the website content from S3, ensuring low-latency access globally.

Configure custom domain names (if needed) using Route 53.

Set up SSL certificates with ACM for secure HTTPS traffic.

IAM Policies and Roles:

Create IAM roles and policies to manage access to the S3 buckets.
Ensure that only specific users or services can upload files to the buckets, while making the content publicly accessible via CloudFront.

Logging and Monitoring:

Enable access logging for both the S3 buckets and the CloudFront distributions, storing logs in a separate S3 bucket.

Set up CloudWatch metrics for monitoring traffic and access patterns.

project-4/

├── main.tf

├── variables.tf

├── outputs.tf

├── terraform.tfvars

├── modules/
│   
    ├── s3/
|   |   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf

│   ├── cloudfront/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf

│   ├── iam/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf

├── environments/

│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars

│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars

│   ├── prod/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars