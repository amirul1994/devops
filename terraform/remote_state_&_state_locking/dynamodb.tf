resource "aws_dynamodb_table" "state_lock_table" {
    name = "terraform-state-lock"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "LockID"
    attribute {
        name = "LockID"
        type = "S"
    }
}