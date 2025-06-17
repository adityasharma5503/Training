1. generate private key file-
openssl genrsa -out adam.key 2048

2. Generate certificate signing request file-
openssl req -new -key adam.key -out adam.csr -subj "/CN=adam"

3. 
