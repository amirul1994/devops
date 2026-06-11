data "aws_caller_identity" "current" {}

module "eks" {
    source = "terraform-aws-modules/eks/aws"
    version = "~> 21.0"
    name = local.cluster_name
    kubernetes_version = var.kubernetes_version

    enable_irsa = true

    tags = {
        cluster = "demo"
    }

    vpc_id = module.vpc.vpc_id

    subnet_ids = module.vpc.private_subnets

    addons = {
        coredns = {
            most_recent = true
        }
        kube-proxy = {
            most_recent = true
        }
        vpc-cni = {
            most_recent = true
            before_compute = true
            resolve_conflicts_on_create = "OVERWRITE"
            resolve_conflicts_on_update = "OVERWRITE"
        }
    }

    access_entries = {
        admin = {
            principal_arn = data.aws_caller_identity.current.arn
            policy_associations = {
                admin = {
                    policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
                    access_scope = {
                        type = "cluster"
                }
            }
        }
     }
   }

    eks_managed_node_groups = {
        node_group = {
            name = "node-group"
            min_size = 2
            max_size = 6
            desired_size = 2

            instance_types = ["t3.medium"]
            ami_type = "AL2023_x86_64_STANDARD"
            ami_release_version = null
            vpc_security_group_ids = [aws_security_group.all_worker_mgmt.id]
        }
    }
}