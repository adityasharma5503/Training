resource "local_file" "my_file" {
    filename = "first.txt"
    content = "this is my first file automated"
    file_permission = 766
}