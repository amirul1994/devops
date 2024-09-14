A Persistent Volume (PV) in Kubernetes is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using StorageClasses. PVs are resources in the cluster that provide storage to users and have a lifecycle independent of any individual pod that uses the PV. For instance, database data often needs to be retained beyond the application's lifecycle. This is the role of a persistent volume.

key concepts about PersistentVolume
PersistentVolumeClaim (PVC)

A PVC is a request for storage by a user.
Users can request specific sizes and access modes (e.g., can be mounted once read-write or many times read-only).
PVCs are bound to PVs in a one to one relationship, and Kubernetes ensures that the requested storage is available and appropriately matched.
Access Modes: Each PersistentVolume can express how it can be accessed using the attribute spec.accessModes.

ReadWriteOnce (RWO): The volume can be mounted as read-write by a single node.
ReadOnlyMany (ROX): The volume can be mounted as read-only by many nodes.
ReadWriteMany (RWX): The volume can be mounted as read-write by many nodes.
Reclaim Policy: The reclaim policy specifies what should happen to a PersistentVolume object when the PersistentVolumeClaim is deleted

Retain: Manual reclamation of the resource.
Recycle: Basic scrub (rm -rf /thevolume/*).

Delete: Associated storage asset, such as AWS EBS, GCE PD, or Azure Disk, is deleted.

In nginx-pod.yaml file
The dnsPolicy field in a Kubernetes Pod specification determines how DNS resolution is handled for the Pod. It controls whether the Pod uses the cluster's DNS service, the host's DNS settings, or other DNS configurations. Here are the possible values for dnsPolicy and what they mean:

1. ClusterFirst
Default Behavior: This is the default DNS policy if none is specified.

Behavior: The Pod uses the DNS settings provided by the Kubernetes cluster. DNS queries that do not match the configured cluster domain suffix (e.g., .cluster.local) are forwarded to the upstream nameserver inherited from the node.

Use Case: Suitable for most Pods that need to resolve both cluster-internal and external DNS names.

2. ClusterFirstWithHostNet
Behavior: This policy is similar to ClusterFirst but is used for Pods running with hostNetwork: true. It ensures that DNS queries are resolved using the cluster's DNS service even when the Pod is using the host's network namespace.

Use Case: Useful for Pods that need to use the host's network but still require cluster DNS resolution.

3. Default
Behavior: The Pod inherits the DNS settings from the node where it is running. This means the Pod uses the same DNS configuration as the node.

Use Case: Suitable for Pods that need to use the same DNS settings as the host node.

4. None
Behavior: This policy allows you to specify a custom DNS configuration for the Pod using the dnsConfig field. It completely ignores the cluster's DNS settings.

Use Case: Useful for Pods that require a specific DNS configuration that differs from the cluster's default settings.
