variable "files" {
  type = map(string)
  default = {
   "pets.txt" = "this is the pets file"
   "dogs.txt" = "this is the dogs file"
   "cats.txt" = "this is the cats file"
   }
} 

resource "local_file" "example" {
   for_each = var.files
   filename = "/root/${each.key}"
   content = each.value
}