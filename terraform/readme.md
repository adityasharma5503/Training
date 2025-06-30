## taint, untaint

- Terraform taint and untaint are used to destroy and recreate selected resources.

- Use case: we can use -  
> terraform taint resource_name.identifier

eg. terraform taint aws_instance.myinstance

This will mark the resource to taint in the tfstate file.

**Note** : changes will be applied only on next terraform apply 

- Drawback: If someone else apply changes to infrastructure without knowing that we have tainted some resources, then it causes problems

## replace

> terraform apply -replace="aws_instance.web"

- This command is used to replace/recreate the resource when applying the configuration itself.

## destroy and apply with target ?

Following commands lets us to apply and destory with targetting specific resource

> terraform apply -target="aws_instance.web"

> terraform destroy -target="aws_instance.web"

**Question:** Can we not just destroy and apply the resource?
**Answer:** This method does not keeps the dependencies to the resources in check. So best way is to use replace


## Provisioners in terraform

allow you to run scripts or commands on a resource after it is created — typically used to configure virtual machines (like installing software on an EC2 instance) after provisioning.

- 3 Types :
1. File Provisioner
2. Local-exec Provisioner
3. Remote-exec Provisioner