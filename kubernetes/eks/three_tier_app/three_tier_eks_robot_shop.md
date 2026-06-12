
# Three-Tier Architecture on AWS EKS with Robot Shop Microservices

## Overview
- **Presenter**: Abishek (DevOps/Cloud Engineer)
- **Topic**: Three-Tier Architecture Model & Deployment on AWS EKS (Kubernetes)
- **Demo Project**: Robot Shop (IBM Instana demo e-commerce application)
- **Platform**: AWS EKS (Elastic Kubernetes Service) with EC2 instances (not Fargate)

---

## 1. Three-Tier Architecture Explained

### What is Three-Tier Architecture?
A popular architectural pattern used by real-world applications (Instagram, Facebook, Amazon, Flipkart, Myntra, etc.).

### The Three Layers:

| Layer | Also Called | Purpose | In Robot Shop |
|-------|-------------|---------|---------------|
| **Frontend** | Presentation Layer | User Interface (UI) | AngularJS web app served by Nginx |
| **Backend** | Logic Layer | Business logic, API mediation | Multiple microservices (Cart, Catalog, Payment, Shipping, Ratings, User, Dispatch) |
| **Database** | Data Layer | Data persistence | MongoDB, MySQL, Redis, RabbitMQ |

### How They Work Together:
1. **User** interacts with the **Frontend** (presentation layer)
2. **Frontend** sends requests to **Backend** (logic layer)
3. **Backend** queries **Database** (data layer) for product details, user info, etc.
4. **Backend** returns processed data to **Frontend** for display

---

## 2. Demo Project: Robot Shop

### About Robot Shop
- **Original Author**: IBM (created to demo Instana APM tool)
- **Type**: Sample e-commerce microservices application
- **Purpose**: Sells robots and AI products
- **Repository**: https://github.com/instana/robot-shop
- **Presenter Fork**: Modified for easy EKS deployment (added EKS steps, Helm charts)

### Why Robot Shop for Learning?
1. **Multiple Microservices**: Each service is independently deployable
2. **Polyglot Architecture**: Different programming languages per service
3. **Multiple Databases**: Uses different database technologies
4. **Real-world Features**: Registration, login, catalog, cart, checkout, shipping, payments
5. **Message Queue**: Uses RabbitMQ for order processing
6. **In-memory Store**: Uses Redis for cart persistence

### Application Features (User Workflows):
- **User Registration/Login**: New users register, existing users login
- **Product Catalog**: Browse AI products and robots by category
- **Product Details**: View images, ratings, pricing, discounts
- **Add to Cart**: Like Amazon/Flipkart experience
- **Checkout**: Shipping address input with distance/cost calculation
- **Payment**: Placeholder for payment gateway integration (PayPal default)
- **Order Confirmation**: Order ID generated, order sent to messaging queue

---

## 3. Microservices Architecture

### Monolithic vs Microservices

| Aspect | Monolithic | Microservices |
|--------|-----------|---------------|
| **Codebase** | Single binary/application | Multiple independent services |
| **Deployment** | Deploy everything together | Deploy services independently |
| **Impact of Changes** | One change affects entire app | One change affects only that service |
| **Testing** | Full regression testing needed | Test only the changed service |
| **Team Structure** | One large team | Multiple small teams per service |
| **Example** | All 10,000 lines in one folder | Catalog, Payment, Shipping as separate services |

### Why Microservices?
- **Independent Deployment**: Each service can be deployed separately
- **Technology Diversity**: Different languages/frameworks per service
- **Scalability**: Scale individual services based on demand
- **Fault Isolation**: Failure in one service doesn't crash others
- **Team Autonomy**: Different teams own different services
- **Real-world Example**: Amazon has 500-1000+ microservices

### Robot Shop Microservices (12 Components):

| Service | Language/Framework | Purpose | Database Used |
|---------|-------------------|---------|---------------|
| **Web** | AngularJS + Nginx | Frontend UI | - |
| **Cart** | Python (Flask) | Shopping cart logic | Redis |
| **Catalogue** | NodeJS (Express) | Product catalog | MongoDB |
| **User** | NodeJS (Express) | User registration/login | MongoDB |
| **Ratings** | PHP (Apache) | Product ratings/reviews | MySQL |
| **Shipping** | Java (Spring Boot) | Shipping cost calculation | MySQL (Maxmind data) |
| **Payment** | Python (Flask) | Payment processing | - |
| **Dispatch** | Golang | Order dispatch/message handling | RabbitMQ |
| **MongoDB** | - | NoSQL database for users/catalog | - |
| **MySQL** | - | Relational database for ratings/shipping | - |
| **Redis** | - | In-memory data store for carts | - |
| **RabbitMQ** | - | Message queue for order pipeline | - |

### Why Different Languages?
- **Educational Purpose**: Shows how to write Dockerfiles for different languages
- **Real-world Scenario**: Companies may use different languages based on team expertise or service requirements
- **Demonstrates Polyglot Microservices**: Not all services need same language

---

## 4. Database Architecture (Data Layer)

### Database Choices & Rationale:

| Database | Type | Used By | Purpose |
|----------|------|---------|---------|
| **MongoDB** | NoSQL (Document) | User, Catalogue | Store user details, product catalog (flexible schema) |
| **MySQL** | Relational | Ratings, Shipping | Structured data for ratings, shipping/Maxmind data |
| **Redis** | In-Memory Data Store | Cart | Session/cart persistence (fast access) |
| **RabbitMQ** | Message Broker | Dispatch | Order queue processing |

### Why Redis (In-Memory Data Store) vs In-Memory Cache?
- **In-Memory Cache**: Data lost if application crashes/restarts
- **Redis (In-Memory Data Store)**: Persists data even if app goes down
- **Use Case**: Cart items persist across user sessions and app restarts
- **Kubernetes Deployment**: Deployed as **StatefulSet** (not Deployment) to maintain state

### Why Two Different Databases?
- **Educational**: Learn to deploy both MongoDB and MySQL on Kubernetes
- **Real-world**: Different data models suit different databases
- **Could be same**: In production, might use one database type, but demo shows diversity

---

## 5. Docker & Containerization

### Dockerfile Examples per Service:

#### Java (Shipping Service):
```dockerfile
# Multi-stage build
FROM maven:3.6-jdk-8 AS build
WORKDIR /app
COPY . .
RUN mvn package

FROM openjdk:8-jre
COPY --from=build /app/target/shipping.jar /app.jar
CMD ["java", "-jar", "/app.jar"]
```

#### PHP (Ratings Service):
```dockerfile
FROM php:7.4-apache
COPY . /var/www/html/
RUN composer install
```

#### Python (Cart/Payment):
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

#### Golang (Dispatch):
```dockerfile
FROM golang:1.16 AS build
WORKDIR /app
COPY . .
RUN go build -o dispatch

FROM alpine
COPY --from=build /app/dispatch /dispatch
CMD ["/dispatch"]
```

### Docker Repository:
- **Images**: All pre-built and available on Docker Hub
- **Repository**: `robotshop` (or custom repo)
- **Tag**: `latest` (or specific version)

---

## 6. Kubernetes & Helm Deployment

### Helm Chart Structure:
```
robot-shop/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Configurable values (image repo, version, etc.)
└── templates/          # Kubernetes manifests
    ├── cart-deployment.yaml
    ├── cart-service.yaml
    ├── catalogue-deployment.yaml
    ├── catalogue-service.yaml
    ├── dispatch-deployment.yaml
    ├── dispatch-service.yaml
    ├── mongodb-deployment.yaml
    ├── mongodb-service.yaml
    ├── mysql-deployment.yaml
    ├── mysql-service.yaml
    ├── payment-deployment.yaml
    ├── payment-service.yaml
    ├── rabbitmq-deployment.yaml
    ├── rabbitmq-service.yaml
    ├── ratings-deployment.yaml
    ├── ratings-service.yaml
    ├── redis-statefulset.yaml    # StatefulSet for persistence
    ├── redis-service.yaml
    ├── shipping-deployment.yaml
    ├── shipping-service.yaml
    ├── user-deployment.yaml
    ├── user-service.yaml
    ├── web-deployment.yaml
    └── web-service.yaml
```

### Helm Chart Benefits:
1. **Templating**: Reuse same deployment pattern for all services
2. **Values Management**: Change image repo/version in one place (`values.yaml`)
3. **Easy Deployment**: Single command deploys all 12 components
4. **Rollback**: Easy to rollback to previous versions

### Key Kubernetes Concepts Used:
- **Deployment**: For stateless services (cart, catalog, payment, etc.)
- **StatefulSet**: For Redis (requires persistent storage)
- **Service**: For internal communication between microservices
- **PersistentVolumeClaim**: For Redis data persistence
- **StorageClass**: `gp2` (AWS EBS default) or `standard`

---

## 7. AWS EKS Deployment Steps

### Prerequisites:
1. **eksctl**: CLI tool for EKS cluster management
2. **kubectl**: Kubernetes CLI
3. **AWS CLI**: AWS command line interface
4. **Helm**: Kubernetes package manager

### Step 1: Create EKS Cluster
```bash
eksctl create cluster --name robot-shop --region us-west-1
```
- **Note**: Cluster creation takes ~15-20 minutes
- **Instance Type**: EC2 instances (NOT Fargate - explained below)

### Why EC2 Instances Instead of Fargate?
1. **Redis Requirements**: Needs `NET_ADMIN` privileges (not supported by Fargate)
2. **EBS Persistent Volumes**: Fargate doesn't support EBS for StatefulSets
3. **Educational**: Previous demo used Fargate, this shows EC2 approach

### Step 2: OIDC IAM Configuration
**Purpose**: Allow Kubernetes service accounts to assume AWS IAM roles

```bash
# Export cluster name
export CLUSTER_NAME=robot-shop

# Get OIDC ID
eksctl utils associate-iam-oidc-provider --cluster $CLUSTER_NAME --approve

# Verify OIDC provider
aws iam list-open-id-connect-providers
```

**Why OIDC?**
- EKS pods need to access AWS services (EBS for Redis storage)
- Kubernetes Service Accounts ↔ AWS IAM Roles integration
- Enables fine-grained AWS resource access from pods

### Step 3: ALB (Application Load Balancer) Controller Setup
**Purpose**: Expose web application to external world via Ingress

```bash
# 1. Download IAM policy for ALB controller
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.0/docs/install/iam_policy.json

# 2. Create IAM policy
aws iam create-policy     --policy-name AWSLoadBalancerControllerIAMPolicy     --policy-document file://iam_policy.json

# 3. Create IAM role and service account
eksctl create iamserviceaccount     --cluster=$CLUSTER_NAME     --namespace=kube-system     --name=aws-load-balancer-controller     --attach-policy-arn=arn:aws:iam::<ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy     --approve

# 4. Add Helm repo and install ALB controller
helm repo add eks https://aws.github.io/eks-charts
helm repo update
helm install aws-load-balancer-controller eks/aws-load-balancer-controller     -n kube-system     --set clusterName=$CLUSTER_NAME     --set serviceAccount.create=false     --set serviceAccount.name=aws-load-balancer-controller     --set region=us-west-1     --set vpcId=<VPC_ID>
```

**Important Notes:**
- ALB controller **must** be in `kube-system` namespace (watches all namespaces)
- Replace `<ACCOUNT_ID>` and `<VPC_ID>` with your values
- If CloudFormation fails, delete the stack and recreate
- Verify pods are running: `kubectl get pods -n kube-system`

### Step 4: EBS CSI Driver Setup
**Purpose**: Enable automatic EBS volume creation for StatefulSets

```bash
# 1. Create IAM service account for EBS CSI
eksctl create iamserviceaccount     --name ebs-csi-controller-sa     --namespace kube-system     --cluster $CLUSTER_NAME     --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy     --approve

# 2. Add EBS CSI driver as EKS add-on
aws eks create-addon     --cluster-name $CLUSTER_NAME     --addon-name aws-ebs-csi-driver     --service-account-role-arn arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>
```

**Why EBS CSI Driver?**
- **StorageClass + PVC**: When Redis StatefulSet requests storage
- **Automatic Provisioning**: EBS volume automatically created and attached
- **Without CSI Driver**: Manual EBS volume creation required
- **Interview Tip**: Common question for EKS + StatefulSet scenarios

### Step 5: Deploy Robot Shop Application

```bash
# Create namespace
kubectl create namespace robot-shop

# Deploy via Helm (from eks/helm directory)
helm install robot-shop . -n robot-shop

# Verify all pods are running
kubectl get pods -n robot-shop -w
```

**Wait Time**: Can take 5-15 minutes for all pods to be ready

### Step 6: Expose Application via Ingress

```bash
# Apply Ingress resource
kubectl apply -f ingress.yaml

# Check Ingress status
kubectl get ingress -n robot-shop
```

**Ingress YAML Example:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: robot-shop-ingress
  namespace: robot-shop
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 8080
```

**Access Methods:**
1. **LoadBalancer Service**: Direct AWS ELB (less common in production)
2. **Ingress + ALB Controller**: More common, flexible routing

**ALB Provisioning:**
- Check AWS EC2 Console → Load Balancers
- Status changes from `provisioning` → `active` (~2-5 minutes)
- DNS name becomes accessible once active

---

## 8. Architecture Diagram (High Level)

```
┌─────────────────────────────────────────────────────────────┐
│                        USER                                  │
│                   (Browser/Client)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              PRESENTATION LAYER (Frontend)                   │
│  ┌─────────────┐                                            │
│  │    Web      │  AngularJS + Nginx (Reverse Proxy)        │
│  │  (Port 8080)│                                            │
│  └──────┬──────┘                                            │
└─────────┼────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                LOGIC LAYER (Backend)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │  Cart    │ │ Catalogue│ │  User    │ │  Payment │       │
│  │ (Python) │ │ (NodeJS) │ │ (NodeJS) │ │ (Python) │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                    │
│  │ Ratings  │ │ Shipping │ │ Dispatch │                    │
│  │  (PHP)   │ │  (Java)  │ │ (Golang) │                    │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘                    │
└───────┼────────────┼────────────┼──────────────────────────┘
        │            │            │
        ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│                 DATA LAYER (Database)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ MongoDB  │ │  MySQL   │ │  Redis   │ │ RabbitMQ │       │
│  │ (User/   │ │ (Ratings/│ │  (Cart   │ │ (Order   │       │
│  │ Catalog) │ │ Shipping)│ │ Session) │ │  Queue)  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. CI/CD Pipeline Considerations

### Important Principles:
1. **One Pipeline Per Microservice**: Each service has its own CI/CD pipeline
2. **12 Pipelines Total**: For this project (12 components)
3. **Start Simple**: Begin with one service (e.g., Python-based Payment or Java-based Shipping)
4. **Helm per Service**: In production, each microservice has its own Helm chart

### Why Not One Pipeline for All?
- **Independent Deployment**: Services deploy independently
- **Different Languages**: Build steps differ (Maven for Java, pip for Python, etc.)
- **Different Teams**: Team ownership per service
- **Rollback Scope**: Rollback affects only one service

### Suggested Starting Points:
- **Payment** (Python/Flask) - Simple Dockerfile
- **Shipping** (Java/Spring Boot) - Maven build
- **Dispatch** (Golang) - Single binary

---

## 10. Cleanup & Cost Management

### Delete EKS Cluster:
```bash
eksctl delete cluster --name robot-shop --region us-west-1
```

**Note**: This deletes ALL resources (EC2 instances, load balancers, EBS volumes)

### Cost Considerations:
- EKS cluster running costs ~$0.10/hour ($72/month) + EC2 costs
- Remember to delete cluster after demo to avoid charges
- Fargate vs EC2: Different pricing models

---

## 11. Key Takeaways & Interview Tips

### Three-Tier Architecture:
- Presentation → Logic → Data layers
- Separation of concerns
- Scalability per layer

### Microservices Benefits:
- Independent deployment
- Technology diversity
- Fault isolation
- Team autonomy

### Kubernetes on AWS:
- EKS with EC2 vs Fargate trade-offs
- OIDC for IAM integration
- ALB for external exposure
- EBS CSI for persistent storage
- StatefulSet for stateful apps (Redis)

### Common Interview Questions:
1. **Why StatefulSet for Redis?** → Needs persistent identity and storage
2. **Why EBS CSI driver?** → Automatic EBS provisioning for PVCs
3. **Why OIDC provider?** → Secure AWS resource access from pods
4. **Why ALB controller in kube-system?** → Watches all namespaces, single instance
5. **Microservices vs Monolith?** → Independent deploy, different languages, fault isolation

---

## 12. GitHub Repositories

### Original Repository:
- **URL**: https://github.com/instana/robot-shop
- **Author**: IBM / Instana Team
- **Purpose**: Sample microservices for APM/observability demos

### Presenter's Fork (EKS-Optimized):
- **URL**: *(Not explicitly provided in video, but mentioned as forked with EKS modifications)*
- **Changes Made**:
  - Added EKS deployment steps
  - Created/modified Helm charts for EKS
  - Added Ingress configuration for ALB
  - Simplified deployment process

### Related Resources:
- **AWS Zero to Hero Playlist**: Day 22 covers EKS setup prerequisites
- **Repository**: https://github.com/AbhishekVeeramalla/AWS-Zero-to-Hero (assumed based on reference)

---

## 13. Technology Stack Summary

| Category | Technologies Used |
|----------|-----------------|
| **Frontend** | AngularJS 1.x, Nginx |
| **Backend Languages** | NodeJS, Java (Spring Boot), Python (Flask), Golang, PHP |
| **Databases** | MongoDB, MySQL, Redis |
| **Message Queue** | RabbitMQ |
| **Containerization** | Docker, Docker Compose |
| **Orchestration** | Kubernetes, Helm |
| **Cloud Platform** | AWS EKS (EC2 instances) |
| **AWS Services** | EKS, EBS, ALB, IAM, OIDC |
| **Monitoring** | Instana (APM), Prometheus (metrics) |
| **Load Testing** | Locust (Python) |

---

## 14. Troubleshooting Tips

### Common Issues:
1. **Region Mismatch**: Ensure AWS CLI region matches EKS cluster region
   - Fix: `aws configure` → set region to `us-west-1` (or your cluster region)

2. **CloudFormation Failures**: ALB/CSI service account creation fails
   - Fix: Delete CloudFormation stack in AWS Console, then recreate

3. **Pods Not Ready**: Ratings/Shipping take longer to start
   - Fix: Wait 5-15 minutes, check `kubectl describe pod <pod-name>`

4. **ALB Provisioning Stuck**: Load balancer stays in "provisioning"
   - Fix: Check IAM policies, verify OIDC provider, ensure subnets tagged

5. **Ingress Not Getting Address**: No ALB DNS assigned
   - Fix: Verify ALB controller pods are running in `kube-system`

6. **Helm Chart Errors**: Wrong directory or missing files
   - Fix: Navigate to `eks/helm` folder before running `helm install`

### Verification Commands:
```bash
# Check all pods
kubectl get pods -n robot-shop

# Check services
kubectl get svc -n robot-shop

# Check ingress
kubectl get ingress -n robot-shop

# Check ALB controller
kubectl get pods -n kube-system | grep alb

# Check EBS CSI driver
kubectl get pods -n kube-system | grep ebs

# Check storage class
kubectl get storageclass

# Check persistent volumes
kubectl get pv
```

---

## 15. Additional Resources & References

- **Robot Shop GitHub**: https://github.com/instana/robot-shop
- **AWS EKS Documentation**: https://docs.aws.amazon.com/eks/
- **AWS Load Balancer Controller**: https://kubernetes-sigs.github.io/aws-load-balancer-controller/
- **EBS CSI Driver**: https://github.com/kubernetes-sigs/aws-ebs-csi-driver
- **Helm Documentation**: https://helm.sh/docs/
- **Instana APM**: https://www.instana.com/
- **AWS Zero to Hero Series**: Day 22 (EKS setup prerequisites)

---

*Generated from video transcript with additional research and corrections*
*Date: 2024*
*Presenter: Abishek*
