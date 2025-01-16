variable "filenames" {
 type = list(string)
 default = ["pets.txt", "dogs.txt", "cats.txt"]
} 
resource "local_file" "example" {
 count = length(var.filenames)
 filename = "/root/${var.filenames[count.index]}"
 content = "This is file number ${count.index + 1}"
}