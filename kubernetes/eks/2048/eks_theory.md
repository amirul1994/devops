# Demo Scope: Deploying a "2048 Game" Application on EKS

**Objective:** Deploy a "2048 Game" application on Amazon EKS with the following architecture:
*   **VPC:** Configured with Public and Private Subnets.
*   **Application:** Deployed in the **Private Subnet**.
*   **Access:** Public access via Load Balancer using an **Ingress Controller**.

---

## 2. What is EKS?

*   **Definition:** A **managed Kubernetes service** provided by AWS.
*   **Key Distinction:**
    *   **Managed Control Plane:** AWS manages the Master Nodes (API Server, etcd, Scheduler, Controller Manager). AWS handles high availability, patching, certificate renewal, and uptime (SLA backed).
    *   **Unmanaged Data Plane (Worker Nodes):** The user is responsible for managing worker nodes, though AWS provides tools to simplify this.

---

## 3. Why Use EKS? (The Problem with Self-Managed K8s)

*   **Self-Managed Complexity:** Setting up K8s manually (using `kubeadm` or even automation tools like `kops`) requires:
    *   Provisioning EC2 instances for Masters and Workers.
    *   Installing components: CNI plugins, Container Runtime, DNS, kube-proxy.
    *   Joining nodes to the control plane.
*   **Maintenance Burden:** Even with automation tools, you are responsible for:
    *   Debugging crashed etcd or API servers.
    *   Renewing expired certificates.
    *   Handling scheduler issues.
    *   Managing scaling and monitoring for hundreds/thousands of clusters.
*   **EKS Advantage:** Offloads the heavy lifting of control plane maintenance to AWS, allowing engineers to focus on applications rather than infrastructure debugging.

---

## 4. Worker Node Options in EKS

When attaching worker nodes to the EKS control plane, you have two main choices:

| Feature | **EC2 Instances (Self-Managed Workers)** | **AWS Fargate (Serverless)** |
| :--- | :--- | :--- |
| **Management** | You manage the EC2 instances. | Fully serverless; no servers to manage. |
| **Scaling** | You must configure Auto Scaling Groups (ASG) and thresholds. | Automatic scaling handled by AWS. |
| **Availability** | You ensure HA via ASG across AZs. | Highly available by default. |
| **Use Case** | When you need specific OS-level control or persistent storage configurations. | When you want zero infrastructure management for containers. |

---

## 5. Exposing Applications: Services vs. Ingress

### A. Kubernetes Service Types

1.  **ClusterIP (Default):** Accessible only within the cluster (internal communication between pods/nodes).
2.  **NodePort:** Exposes the service on a static port on each Node’s IP.
    *   *Limitation:* Only accessible if you have direct network access to the Node IPs (usually inside the VPC/Private Subnet). Not ideal for public internet access.
3.  **LoadBalancer:** Provisions an external AWS Load Balancer (ELB/ALB/NLB) with a public IP.
    *   *Limitation:* **Costly.** Creating one Load Balancer per service is expensive and inefficient for microservices architectures.

### B. The Best Practice: Ingress

*   **Concept:** Ingress is not a Service type but a resource that manages external access to services, typically HTTP/HTTPS.
*   **How it works:**
    1.  **Ingress Resource:** A YAML file defining rules (e.g., `example.com/app` routes to `Service-A`).
    2.  **Ingress Controller:** The actual software/load balancer that implements the rules defined in the Ingress Resource.
*   **Workflow:**
    1.  User creates an **Ingress Resource**.
    2.  **Ingress Controller** (watching the cluster) detects the new resource.
    3.  Controller provisions/configures a **Load Balancer** (e.g., AWS ALB).
    4.  Traffic flows: `User -> Public LB (Public Subnet) -> Ingress Controller -> Service (ClusterIP/NodePort) -> Pod (Private Subnet)`.

---

## 6. Ingress Controllers

*   The Ingress Resource is just a configuration; it needs a controller to act on it.
*   **Common Controllers:**
    *   **AWS ALB Ingress Controller:** Specifically creates/configures AWS Application Load Balancers.
    *   **Nginx Ingress Controller:** Uses Nginx as the reverse proxy.
    *   **F5, Traefik, etc.:** Other vendors offer their own controllers.
*   **Ingress Class:** Allows you to specify which controller should handle a specific Ingress resource if multiple controllers exist in the cluster.

---

## 7. Summary of Architecture for the Demo

1.  **VPC:** Created with Public and Private subnets.
2.  **EKS Cluster:** Control plane managed by AWS.
3.  **Worker Nodes:** Deployed in Private Subnets.
4.  **Application:** Deployed as Pods.
5.  **Service:** Internal ClusterIP or NodePort.
6.  **Ingress Resource:** Defines routing rules (host/path).
7.  **Ingress Controller (ALB):** Watches Ingress resources and provisions a public-facing Application Load Balancer in the Public Subnet to route traffic to the private pods.