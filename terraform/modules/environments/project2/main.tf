provider "local" {}

module "project2_dir" {
  source        = "../../modules/directory"
  directory_path = "${path.module}/project2_dir"
}

module "project2_file" {
  source        = "../../modules/file"
  directory_path = module.project2_dir.directory_path
  file_path     = "${module.project2_dir.directory_path}/file.txt"
  file_content  = "This is Project 2."
}

output "project2_file_path" {
  value = module.project2_file.file_path
}