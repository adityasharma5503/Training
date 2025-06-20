
To create helm chart named apache helm -
```
helm create apache-helm
```
Then we will edit the values.yml file 


now to package configuration
```
helm package apache-helm
```


now we can create resources using the package. lets say we want to apply for dev env so we can give name dev-apache and install using-
```
helm install dev-apache apache-helm
```


to delete 
```
helm uninstall dev-apache
```