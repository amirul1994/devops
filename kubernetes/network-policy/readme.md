A network policy is a set of rules that define how pods communicate with each other and with other network endpoints. It can be thought of it like a firewall for Kubernetes pods. Network policy for a pod, defines what traffic is allowed to come into (ingress) or go out from (egress) the pod.

kubectl create namespace ns-1
kubectl create namespace ns-2

kubectl run demo-app-0 --image=nginx
kubectl run demo-app-1 --image=nginx --namespace=ns-1
kubectl run demo-app-2 --image=nginx --namespace=ns-2

