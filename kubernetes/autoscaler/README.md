Understanding Scalability in Kubernetes
Scalability refers to a system's ability to handle increasing load. In Kubernetes, scaling workloads
involves dynamically adjusting the number of instances (replicas) of a workload based on demand or
predefined metrics.
Horizontal Pod Autoscaler (HPA)
The Horizontal Pod Autoscaler automatically scales the number of pods in a deployment, replica set, or
stateful set based on observed CPU utilization, memory utilization, or custom metrics. It continuously
adjusts the number of replicas to maintain a target utilization level specified in the HPA configuration.

![image](https://github.com/user-attachments/assets/fcd46ad6-3fdb-41e9-8c9d-bafa8300ab5a)

kubectl get hpa nginx

kubectl describe hpa nginx
