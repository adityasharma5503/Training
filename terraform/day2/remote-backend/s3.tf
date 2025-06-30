resource "aws_s3_bucket" "tfstate-bucket" {
  bucket = "tfstate_bucket"

  tags = {
    Name        = "tfstate-bucket"
  }
}

# resource "aws_s3_bucket_object" "object" {
#   bucket = "tfstate_bucket"
#   key    = "tfstate"
#   source = "/tfstate"

#   etag = filemd5("path/to/file")
# }