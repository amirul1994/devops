terraform init - This command initializes a working directory containing Terraform configuration files. It downloads the necessary provider plugins and sets up the backend configuration. This step is essential before running other Terraform commands.

terraform plan - This command generates and shows an execution plan. It details what actions Terraform will take to reach the desired state specified in the configuration files. This is a dry run and does not make any changes to the infrastructure.

terraform apply - This command applies the changes required to reach the desired state of the configuration. It executes the actions outlined in the execution plan, which can include creating, updating, or deleting infrastructure resources.

terraform destroy - destroy the infra

.terraform folder - created when any plugin is initialized. If this folder get deleted, again use 'terraform init' command.

terraform.tfstate - keep the track of the state of the infrastructure. If any change has been made, compare it with this file and then apply the changes. After applying the changes, modify the file according to the changes. If this file is deleted, it will break terraform leading to a mismatch state.