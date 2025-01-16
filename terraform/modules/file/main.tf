resource "local_file" "file" {
  filename = var.file_path
  content  = var.file_content
}