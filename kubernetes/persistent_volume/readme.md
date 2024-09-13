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
