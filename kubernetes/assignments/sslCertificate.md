step 1:

```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=localhost/O=localhost"
```


step 2:
```
kubectl create secret tls example-tls \
  --key tls.key \
  --cert tls.crt
```


step 3:
edit the ingress file 

```
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - localhost
    secretName: example-tls
```



