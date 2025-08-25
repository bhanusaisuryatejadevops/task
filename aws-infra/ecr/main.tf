resource "aws_ecr_repository" "main" {
  name                 = "main-repo"
  image_tag_mutability = "MUTABLE"
  tags = {
    Name = "main-ecr"
  }
}

output "repository_url" {
  value = aws_ecr_repository.main.repository_url
}
