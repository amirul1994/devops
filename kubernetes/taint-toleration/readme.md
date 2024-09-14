Taints and tolerations are used in Kubernetes to control which Pods can be scheduled on specific nodes. Taints are applied to nodes to repel Pods that do not have the corresponding toleration, while tolerations are added to Pods to allow them to be scheduled on nodes with matching taints. This mechanism helps in dedicating nodes to specific workloads or preventing certain Pods from being scheduledon certain nodes.

There are three effects in Kubernetes taints:

NoSchedule: Pods that do not tolerate the taint will not be scheduled on the node.

PreferNoSchedule: The system will try to avoid placing a Pod that does not tolerate the taint on the node, but it is not strictly required.

NoExecute: Existing Pods that do not tolerate the taint will be evicted from thenode, and new Pods that do not tolerate the taint will not be scheduled on the node.

Taint the nodes

kubectl taint nodes node1 app=blue:NoSchedule
kubectl taint nodes node1 app2=green:NoSchedule
