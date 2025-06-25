#!/bin/bash

sudo apt-get update
sudo apt-get install nginx -y
sudo systemctl enable --now nginx
echo "<h1>nginx is installed</h1>" > /var/www/index.html