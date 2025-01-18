provider "local" {

}

variable "file_contents" {
    type = map(string)
    default = {
        "file1" = "This is content for file1."
        "file2" = "This is content for file2."
        "file3" = "This is content for file3."
    }
} 

resource "local_file" "example1" {
    content = lookup(var.file_contents, "file1", "Default content")
    filename = "${path.module}/example1.txt"
} 

resource "local_file" "example2" {
    content = lookup(var.file_contents, "file2", "Default content")
    filename = "${path.module}/example2.txt"
} 

resource "local_file" "example3" {
    content = lookup(var.file_contents, "file3", "Default content")
    filename = "${path.module}/example3.txt"
}

resource "local_file" "example" {
    content = join(", ", keys(var.file_contents))
    filename = "file_keys.txt"
} 

resource "local_file" "lowercase_example" {
    content = lower("HELLO TERRAFORM")
    filename = "lowecase.txt"
}

output "result" {
    value = coalesce(var.file_contents)
}