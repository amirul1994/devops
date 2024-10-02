![s3_terraform](https://github.com/user-attachments/assets/ed43871b-3987-4377-bd13-4b84a367e74d)


Project Title: "Multi-Environment Static Website Hosting with S3 and CloudFront"

Project Goal:

Create a multi-environment (e.g., development, staging, production) static website hosting solution using AWS S3, with content delivered through CloudFront for faster global access, all managed with Terraform.

Project Components:

Here is the requested format:

---

**1) Create S3 Buckets for Static Website Hosting**

   **a) Create S3 Buckets:**
   
   i) Create separate S3 buckets for each environment (e.g., `my-website-dev`, `my-website-staging`, `my-website-prod`).

   **b) Enable Static Website Hosting for Each Bucket:**

   i) Enable static website hosting in the bucket properties.  
   
   ii) Set the index and error documents (e.g., `index.html`, `error.html`).

   **c) Configure Bucket Policies:**

   i) Set up appropriate bucket policies to make the website publicly accessible if required.  
   
   ii) For private access, restrict the bucket policy as necessary.

---

**2) Versioning and Lifecycle Policies**

   **a) Enable Versioning for All S3 Buckets:**

   i) Enable versioning on each S3 bucket to retain old versions of files.

   **b) Set Up Lifecycle Policies:**

   i) Configure a lifecycle rule to move older versions of files to a different storage class (e.g., Glacier).  
   
   ii) Optionally, configure a rule to delete old file versions after a certain period.

---

**3) CloudFront Distribution**

   **a) Create CloudFront Distributions:**

   i) Create a CloudFront distribution for each environment to serve website content from S3.

   **b) Configure Custom Domain Names:**

   i) Set up custom domains using Route 53 (if needed).

   **c) Set Up SSL Certificates:**

   i) Use AWS Certificate Manager (ACM) to configure SSL certificates for HTTPS traffic.

---

**4) IAM Policies and Roles**

   **a) Create IAM Roles and Policies:**

   i) Define IAM roles and policies to manage access to S3 buckets.  
   
   ii) Restrict file upload permissions to specific users or services while ensuring content is publicly accessible via CloudFront.

---

**5) Logging and Monitoring**

   **a) Enable Access Logging:**

   i) Set up access logging for both S3 buckets and CloudFront distributions.  
   
   ii) Store the logs in a separate S3 bucket.

   **b) Set Up CloudWatch Metrics:**

   i) Monitor traffic and access patterns using CloudWatch metrics.


ACM Certificates and CloudFront
Global Certificates: ACM certificates issued in the us-east-1 region (N. Virginia) are considered global certificates. These certificates can be used with AWS services that require global certificates, such as Amazon CloudFront.

Regional Certificates: ACM certificates issued in other regions are regional certificates and can only be used with services in that specific region. For example, a certificate issued in us-west-2 can be used with services like Elastic Load Balancing (ELB) or API Gateway in the us-west-2 region.

Why us-east-1 for ACM Certificates?
CloudFront Requirement: If you are using Amazon CloudFront for content delivery, you must use an ACM certificate issued in the us-east-1 region. CloudFront requires global certificates, and only certificates issued in us-east-1 meet this requirement.


The origin_access_identity must be a valid OAI ID that you have created in your AWS account.
