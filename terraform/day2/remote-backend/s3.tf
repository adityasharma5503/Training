resource "aws_s3_bucket" "tfstate-bucket" {
  bucket = "tfstate_bucket"

  tags = {
    Name        = "tfstate-bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_object" "object" {
  bucket = "tfstate_bucket"
  key    = "new_object_key"
  source = "path/to/file"

  etag = filemd5("path/to/file")
}