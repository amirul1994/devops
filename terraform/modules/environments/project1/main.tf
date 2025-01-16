provider "local" {}

module "project1_dir" {
  source        = "../../modules/directory"
  directory_path = "${path.module}/project1_dir"
}

module "project1_file" {
  source        = "../../modules/file"
  directory_path = module.project1_dir.directory_path
  file_path     = "${module.project1_dir.directory_path}/file.txt"
  file_content  = "This is Project 1."
}

output "project1_file_path" {
  value = module.project1_file.file_path
}