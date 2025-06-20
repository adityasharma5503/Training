### create dashboard deployment

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

It will create a ns kubernetes-dashboard and create all required services and deployment



### then run the dashboard-admin-user.yaml file that we created:

```
kind: ServiceAccount
apiVersion: v1
metadata:
  name:  admin-user
  namespace: kubernetes-dashboard
---

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: admin-user-binding
subjects:
  - kind: ServiceAccount
    name: admin-user
    namespace: kubernetes-dashboard
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
  ```


  ### then run the command -

  ```
  kubectl proxy --address=0.0.0.0
  ```

  then access the dashboard-
```
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```