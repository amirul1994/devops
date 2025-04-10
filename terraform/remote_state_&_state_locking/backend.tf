terraform {
    backend "s3" {
        bucket = "amirul-terraform-state-bucket"
        region = "ap-southeast-1"
        dynamodb_table = "terraform-state-lock"
        key = "dev/ec2.tfstate"
        encrypt = true
    }
}