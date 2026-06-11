# Note: Deploying an Application on AWS EKS with Fargate and ALB Ingress

## Overview
This session covers deploying a Kubernetes application (2048 Game) on Amazon EKS using **Fargate** for serverless compute and an **Application Load Balancer (ALB)** for external access. The focus is on setting up the necessary infrastructure, configuring IAM permissions, and troubleshooting common issues.

---

## 1. Prerequisites & Tools
Before starting, ensure the following tools are installed on your local machine:
*   **kubectl**: To interact with the Kubernetes cluster.
*   **eksctl**: To create and manage EKS clusters.
*   **AWS CLI**: To interact with AWS services, configured with `aws configure` using Access Key ID and Secret Access Key.

> **Resource:** All commands and files are available in the GitHub repository: `AWS-DevOps-Zero-to-Hero/day-22`.

---

## 2. Creating the EKS Cluster
Instead of using the AWS Console manually, use `eksctl` to automate the creation of the cluster, VPC, subnets, and security groups.

**Why this step is done:** We need a managed Kubernetes control plane to run our application. Using `eksctl` with the `--fargate` flag simplifies the setup by automatically configuring the cluster to use serverless compute, removing the need to manage EC2 worker nodes manually.

**Command:**
```bash
eksctl create cluster \
--name demo-cluster \
--region us-east-1 \
--fargate
```
*   **Why Fargate?** It removes the need to manage EC2 worker nodes. However, it requires **Fargate Profiles** to define which namespaces can run pods.
*   **Time:** Creation takes approximately 15–20 minutes.

---

## 3. Configuring kubectl
Update your local kubeconfig to connect to the new cluster.

**Why this step is done:** After creating the cluster, your local `kubectl` tool needs to know how to authenticate and communicate with the new EKS API server. This command updates your local configuration file (`~/.kube/config`) with the cluster endpoint and authentication details.

**Command:**
```bash
aws eks update-kubeconfig --name demo-cluster --region us-east-1
```

---

## 4. Setting Up Fargate Profile
By default, Fargate only allows pods in `default` and `kube-system` namespaces. To deploy our app in a custom namespace (`game-2048`), we must create a specific Fargate profile.

**Why this step is done:** AWS Fargate is a serverless engine that requires explicit permission to run pods in specific namespaces. Unlike EC2 nodes where any namespace can schedule pods, Fargate uses "Profiles" as a allow-list. Without this profile, pods deployed to the `game-2048` namespace would remain in a `Pending` state indefinitely.

**Command:**
```bash
eksctl create fargateprofile \
--cluster demo-cluster \
--region us-east-1 \
--name alb-sample-app \
--namespace game-2048
```

---

## 5. Deploying the Application (2048 Game)
Apply the Kubernetes manifests (Namespace, Deployment, Service, and Ingress) provided in the GitHub repo.

**Why this step is done:** This creates the actual application resources inside the cluster. We deploy the Namespace first, then the Deployment (which creates the Pods), the Service (which exposes the Pods internally), and the Ingress (which defines the rules for external access). Note that the Ingress resource will exist but won't work yet because the controller that reads it isn't installed.

**Command:**
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/examples/2048/2048_full.yaml
```
*   **Note:** At this stage, the Ingress resource will be created, but it will **not** have an address because the **ALB Ingress Controller** is not yet installed.

---

## 6. Setting Up IAM OIDC Provider
The ALB Controller needs permission to interact with AWS APIs (to create/load balance). This requires an IAM OIDC provider associated with the EKS cluster.

**Why this step is done:** To allow Kubernetes Service Accounts to assume AWS IAM Roles (a feature called IRSA - IAM Roles for Service Accounts), AWS needs to trust the Kubernetes cluster. This command creates an OpenID Connect (OIDC) provider in IAM that corresponds to your EKS cluster's issuer URL, establishing this trust relationship.

**Command:**
```bash
eksctl utils associate-iam-oidc-provider \
--region us-east-1 \
--cluster demo-cluster \
--approve
```

---

## 7. Installing the AWS Load Balancer Controller
This involves creating an IAM Policy, an IAM Role, and a Kubernetes Service Account, then installing the controller via Helm.

### Step A: Create IAM Policy
Download the **complete official policy** from the AWS GitHub repository. This policy contains all necessary permissions including `CreateLoadBalancer`, `DescribeLoadBalancerAttributes`, and `CreateSecurityGroup`.

**Why this step is done:** The ALB Controller runs as a pod inside Kubernetes but needs to make API calls to AWS (EC2, ELB, etc.) to create real cloud resources. AWS requires strict permissions for these actions. Using the official policy ensures no permissions are missing, preventing `AccessDenied` errors that commonly occur with custom-written policies.

**Command:**
```bash
curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.0/docs/install/iam_policy.json
```

**Create Policy Command:**
```bash
aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam-policy.json
```

> **⚠️ Important:** Do NOT use a custom-written policy. Always use the official policy from the AWS GitHub repository. Missing permissions like `elasticloadbalancing:CreateLoadBalancer`, `elasticloadbalancing:DescribeLoadBalancerAttributes`, or `ec2:CreateSecurityGroup` will cause the controller to fail with `AccessDenied` errors.

### Step B: Create IAM Role and Service Account
Use `eksctl` to create a Kubernetes service account annotated with the IAM role.

**Why this step is done:** This links the Kubernetes world with the AWS world. It creates a Service Account in Kubernetes and an IAM Role in AWS. The `eksctl` command automatically configures the Trust Relationship so that only pods using this specific Service Account can assume this IAM Role. This is more secure than attaching permissions to the worker nodes themselves.

**Command:**
```bash
eksctl create iamserviceaccount \
--cluster=demo-cluster \
--namespace=kube-system \
--name=aws-load-balancer-controller \
--role-name AmazonEKSLoadBalancerControllerRole \
--attach-policy-arn=arn:aws:iam::<ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
--approve
```
*(Replace `<ACCOUNT_ID>` with your actual AWS Account ID)*

> **Note:** If the service account already exists, delete it first with `kubectl delete serviceaccount -n kube-system aws-load-balancer-controller` or use `--override-existing-serviceaccounts`.

### Step C: Install Controller via Helm
Add the EKS chart repo and install the controller.

**Why this step is done:** Helm is used to deploy the ALB Controller application itself into the `kube-system` namespace. The controller is a set of pods that watch for `Ingress` resources. When it sees one, it uses the permissions from the Service Account (created in Step B) to provision an actual AWS Application Load Balancer and configure it according to the Ingress rules.

**Commands:**
```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=demo-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=us-east-1 \
  --set vpcId=<VPC_ID>
```
*(Replace `<VPC_ID>` with the VPC ID from your EKS cluster overview - can be found with `aws eks describe-cluster --name demo-cluster --query "cluster.resourcesVpcConfig.vpcId"`)*

---

## 8. Verification & Troubleshooting

### Verify Controller Pods
Check if the controller pods are running in the `kube-system` namespace.

**Why this step is done:** We need to ensure the controller application has started successfully. If the pods are not ready, they cannot watch for Ingress resources or create Load Balancers.

**Command:**
```bash
kubectl get deployment -n kube-system aws-load-balancer-controller
```
*   **Expected:** 2/2 replicas ready (High availability is default).

### Check Controller Logs
If the Ingress doesn't get an address, check the controller logs for permission errors.

**Why this step is done:** Logs provide the specific reason why the controller might be failing. It will explicitly state if an API call was denied due to missing IAM permissions or if there were configuration issues.

**Command:**
```bash
kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller --tail=50
```

**Common Permission Errors and Fixes:**
| Error | Missing Permission | Solution |
|-------|-------------------|----------|
| `not authorized to perform: ec2:CreateSecurityGroup` | `ec2:CreateSecurityGroup` | Use official IAM policy |
| `not authorized to perform: elasticloadbalancing:CreateLoadBalancer` | `elasticloadbalancing:CreateLoadBalancer` | Use official IAM policy |
| `not authorized to perform: elasticloadbalancing:DescribeLoadBalancerAttributes` | `elasticloadbalancing:DescribeLoadBalancerAttributes` | Use official IAM policy |

**If you see any of these errors:** Delete the custom policy and recreate it using the official JSON from GitHub (Step 7A), then restart the controller:
```bash
kubectl delete pod -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
```

### Verify Ingress Address
Check the Ingress resource in the `game-2048` namespace.

**Why this step is done:** This confirms that the ALB Controller has successfully processed the Ingress resource and provisioned the AWS Load Balancer. The presence of an address means the DNS record is ready.

**Command:**
```bash
kubectl get ingress -n game-2048
```
*   **Expected:** The `ADDRESS` column should populate with the DNS name of the ALB within 1-2 minutes after controller installation.
*   **Note:** It may take a few minutes for the ALB to become active.

### Check Target Group Bindings
**Why this step is done:** TargetGroupBindings are custom resources created by the controller that link Kubernetes Services to AWS Target Groups. Verifying this ensures the traffic flow from the ALB to the Pods is correctly configured.

**Command:**
```bash
kubectl get targetgroupbindings -n game-2048
```
*   **Expected:** A target group binding should exist showing registered targets.

### Access the Application
1.  Get the ALB DNS name from the Ingress:
    ```bash
    kubectl get ingress ingress-2048 -n game-2048 -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
    ```
2.  Or find it in the **EC2 Dashboard** > **Load Balancers**.
3.  Paste the DNS name into your browser. You should see the 2048 game.

---

## Key Concepts Recap
1.  **Fargate Profiles:** Mandatory for running pods in non-default namespaces on Fargate.
2.  **IAM OIDC Provider:** Bridges Kubernetes Service Accounts with AWS IAM Roles (IRSA).
3.  **ALB Ingress Controller:** Watches for `Ingress` resources and provisions AWS ALBs automatically.
4.  **Official IAM Policy:** Always use the official policy from GitHub - custom policies are often incomplete and cause `AccessDenied` errors.
5.  **Separation of Concerns:** DevOps engineers set up the Controller and IAM roles; developers define Deployments, Services, and Ingress rules.