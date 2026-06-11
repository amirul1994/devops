## Terraform Apply Output Summary

### 1. Random String Generation
- ✅ `random_string.suffix` - Created (ID: `8XsRikKn`)

### 2. VPC & Networking Resources
- ✅ `module.vpc.aws_vpc.this[0]` - Created (ID: `vpc-073cc9c0a723c0478`)
- ✅ `module.vpc.aws_default_route_table.default[0]` - Created (ID: `rtb-0b92858e1865796ec`)
- ✅ `module.vpc.aws_default_network_acl.this[0]` - Created (ID: `acl-0b62dff6bb2cd98cd`)
- ✅ `module.vpc.aws_default_security_group.this[0]` - Created (ID: `sg-0eb5dfc906d765473`)
- ✅ `module.vpc.aws_route_table.public[0]` - Created (ID: `rtb-00f718fa396d7070e`)
- ✅ `module.vpc.aws_route_table.private[0]` - Created (ID: `rtb-0de80687527c8c8da`)
- ✅ `module.vpc.aws_internet_gateway.this[0]` - Created (ID: `igw-06b58a0455cbd7a9e`)
- ✅ `module.vpc.aws_subnet.public[0]` - Created (ID: `subnet-06025cff7311f5f5c`)
- ✅ `module.vpc.aws_subnet.public[1]` - Created (ID: `subnet-0b1d6a450e43e6c1d`)
- ✅ `module.vpc.aws_subnet.private[0]` - Created (ID: `subnet-00ceeda20aed5630c`)
- ✅ `module.vpc.aws_subnet.private[1]` - Created (ID: `subnet-05cafd81a512ddddf`)
- ✅ `module.vpc.aws_eip.nat[0]` - Created (ID: `eipalloc-0c0a2f473e12405af`)
- ✅ `module.vpc.aws_nat_gateway.this[0]` - Created (ID: `nat-08b15f82162439514`) *(2m 9s)*
- ✅ `module.vpc.aws_route.public_internet_gateway[0]` - Created
- ✅ `module.vpc.aws_route.private_nat_gateway[0]` - Created
- ✅ `module.vpc.aws_route_table_association.public[0]` - Created
- ✅ `module.vpc.aws_route_table_association.public[1]` - Created
- ✅ `module.vpc.aws_route_table_association.private[0]` - Created
- ✅ `module.vpc.aws_route_table_association.private[1]` - Created

### 3. Security Groups
- ✅ `aws_security_group.all_worker_mgmt` - Created (ID: `sg-0a3ee56ce9edce5e8`)
- ✅ `aws_security_group_rule.all_worker_mgmt_ingress` - Created
- ✅ `aws_security_group_rule.all_worker_mgmt_egress` - Created
- ✅ `module.eks.aws_security_group.cluster[0]` - Created (ID: `sg-03809321fe49213bf`)
- ✅ `module.eks.aws_security_group.node[0]` - Created (ID: `sg-043ab97ce5b191874`)
- ✅ Multiple security group rules for cluster and node groups - Created

### 4. EKS Cluster & IAM Resources
- ✅ `module.eks.aws_iam_role.this[0]` - Created (ID: `amirul-eks-8XsRikKn-cluster-20260611145250346000000001`)
- ✅ `module.eks.aws_iam_role_policy_attachment.this["AmazonEKSClusterPolicy"]` - Created
- ✅ `module.eks.module.kms.aws_kms_key.this[0]` - Created (ID: `419125b9-5d58-496b-8896-9a02d91a6248`) *(26s)*
- ✅ `module.eks.module.kms.aws_kms_alias.this["cluster"]` - Created (ID: `alias/eks/amirul-eks-8XsRikKn`)
- ✅ `module.eks.aws_iam_policy.cluster_encryption[0]` - Created
- ✅ `module.eks.aws_iam_role_policy_attachment.cluster_encryption[0]` - Created
- ✅ `module.eks.aws_cloudwatch_log_group.this[0]` - Created (ID: `/aws/eks/amirul-eks-8XsRikKn/cluster`)
- ✅ `module.eks.aws_eks_cluster.this[0]` - Created (ID: `amirul-eks-8XsRikKn`) *(9m 50s)*
- ✅ `module.eks.aws_ec2_tag.cluster_primary_security_group["cluster"]` - Created
- ✅ `module.eks.data.tls_certificate.this[0]` - Read
- ✅ `module.eks.aws_iam_openid_connect_provider.oidc_provider[0]` - Created
- ✅ `module.eks.time_sleep.this[0]` - Created *(30s wait)*

### 5. EKS Managed Node Group
- ✅ `module.eks.module.eks_managed_node_group["node_group"].aws_iam_role.this[0]` - Created
- ✅ `module.eks.module.eks_managed_node_group["node_group"].aws_iam_role_policy_attachment.this["AmazonEKSWorkerNodePolicy"]` - Created
- ✅ `module.eks.module.eks_managed_node_group["node_group"].aws_iam_role_policy_attachment.this["AmazonEC2ContainerRegistryReadOnly"]` - Created
- ✅ `module.eks.module.eks_managed_node_group["node_group"].aws_iam_role_policy_attachment.this["AmazonEKS_CNI_Policy"]` - Created
- ✅ `module.eks.module.eks_managed_node_group["node_group"].aws_launch_template.this[0]` - Created (ID: `lt-02ee8d163aa197a0b`)
- ✅ `module.eks.module.eks_managed_node_group["node_group"].aws_eks_node_group.this[0]` - Created (ID: `amirul-eks-8XsRikKn:node-group-20260611164149171400000001`) *(~18m)*

### 6. EKS Add-ons
- ✅ `module.eks.aws_eks_addon.this["coredns"]` - Created *(16s)*
- ✅ `module.eks.aws_eks_addon.this["kube-proxy"]` - Created *(26s)*

---

**Total Deployment Time:** Approximately **20-25 minutes**

**Key Resources Created:**
- **Cluster Name:** `amirul-eks-8XsRikKn`
- **VPC ID:** `vpc-073cc9c0a723c0478`
- **Account ID:** `454631876617`
- **Region:** `us-east-1` (inferred from OIDC provider URL)
- **Node Group:** `node-group-20260611164149171400000001`

All resources were created successfully with no errors! 🎉