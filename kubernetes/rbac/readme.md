In Kubernetes, RBAC is used to manage permissions and control access to the Kubernetes API.  

Roles and ClusterRoles:

A Role is a set of permissions within a specific namespace.
A ClusterRole is a set of permissions that are cluster-wide.

RoleBindings and ClusterRoleBindings:

A RoleBinding grants the permissions defined in a Role to a user or a group within a specific namespace.
A ClusterRoleBinding grants the permissions defined in a ClusterRole to a user or a group cluster-wide.

Users and Groups: Kubernetes doesn't manage users and groups itself. Instead, itrelies on external systems to manage them. Users and groups are represented in Kubernetes as strings.

Verbs: Verbs are actions that can be performed on resources. Some common verbs include "get", "list", "watch", "create", "update", "patch", "delete", and "exec".

