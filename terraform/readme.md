Project Title: "Multi-Environment Static Website Hosting with S3 and CloudFront"

Project Goal:

Create a multi-environment (e.g., development, staging, production) static website hosting solution using AWS S3, with content delivered through CloudFront for faster global access, all managed with Terraform.

Project Components:

Here is the requested format:

1) Create S3 Buckets for Static Website Hosting

a) Create S3 Buckets:

i) Create separate S3 buckets for each environment (e.g., my-website-dev, my-website-staging, my-website-prod).

b) Enable Static Website Hosting for Each Bucket:

i) Enable static website hosting in the bucket properties.

ii) Set the index and error documents (e.g., index.html, error.html).

c) Configure Bucket Policies:

i) Set up appropriate bucket policies to make the website publicly accessible if required.

ii) For private access, restrict the bucket policy as necessary.

2) Versioning and Lifecycle Policies

a) Enable Versioning for All S3 Buckets:

i) Enable versioning on each S3 bucket to retain old versions of files.

b) Set Up Lifecycle Policies:

i) Configure a lifecycle rule to move older versions of files to a different storage class (e.g., Glacier).

ii) Optionally, configure a rule to delete old file versions after a certain period.

3) CloudFront Distribution

a) Create CloudFront Distributions:

i) Create a CloudFront distribution for each environment to serve website content from S3.

b) Configure Custom Domain Names:

i) Set up custom domains using Route 53 (if needed).

c) Set Up SSL Certificates:

i) Use AWS Certificate Manager (ACM) to configure SSL certificates for HTTPS traffic.

4) IAM Policies and Roles

a) Create IAM Roles and Policies:

i) Define IAM roles and policies to manage access to S3 buckets.

ii) Restrict file upload permissions to specific users or services while ensuring content is publicly accessible via CloudFront.

5) Logging and Monitoring

a) Enable Access Logging:

i) Set up access logging for both S3 buckets and CloudFront distributions.

ii) Store the logs in a separate S3 bucket.

b) Set Up CloudWatch Metrics:

i) Monitor traffic and access patterns using CloudWatch metrics.


terraform init - This command initializes a working directory containing Terraform configuration files. It downloads the necessary provider plugins and sets up the backend configuration. This step is essential before running other Terraform commands.

terraform plan - This command generates and shows an execution plan. It details what actions Terraform will take to reach the desired state specified in the configuration files. This is a dry run and does not make any changes to the infrastructure.

terraform apply - This command applies the changes required to reach the desired state of the configuration. It executes the actions outlined in the execution plan, which can include creating, updating, or deleting infrastructure resources.

terraform destroy - destroy the infra

.terraform folder - created when any plugin is initialized. If this folder get deleted, again use 'terraform init' command.

terraform.tfstate - keep the track of the state of the infrastructure. If any change has been made, compare it with this file and then apply the changes. After applying the changes, modify the file according to the changes. If this file is deleted, it will break terraform leading to a mismatch state.

terraform state list - The terraform state list command lists all the resources that Terraform is managing in the current state.

terraform state show - The terraform state show command is used to display detailed information about a specific resource in the Terraform state.

terraform state show <resource_address>
terraform state show aws_internet_gateway.gw

terraform destroy -target <resource_address>
terraform destroy -target aws_instance.web-server-instance 

terraform apply -target <resource_adress>
terraform apply -target aws_instance.web-server-instace