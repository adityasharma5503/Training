# Stacks

**Create a stack**
```
pulumi stack init staging
```
This creates an empty stack and sets it as the active stack. 

The stack name is specified in one of the following formats:
1. stackName
2. orgName/stackName
3. orgName/projectName/stackName : Identifies the stack stackName in the organization orgName and the project projectName. projectName must match the project specified by the nearest Pulumi.yaml project file.

While stacks with applied configuration settings will often be accompanied by Pulumi.<stack-name>.yaml files, these files are not created by pulumi stack init. They are created and managed with pulumi config

**Listing stacks**

```
pulumi stack ls
```

**Select a stack**

```
pulumi stack select stackName
```

**Update a stack**
```
pulumi up
```

**View stack resources**
```
pulumi stack
```
with no arguments


## **Stack tags**

view tags
```
pulumi stack tag ls
```

set custom tags
```
pulumi stack tag set <name> <value>
```

remove tag
```
pulumi stack tag rm <name>.
```

## Stack outputs

python-
```python
pulumi.export("url", resource.url)
```

cli-
```bash
pulumi stack output exportName 
```
or
```bash
pulumi stack output --json
```
to get all exports in json

to get secrets which are not shown otherwise
```bash
pulumi stack output --show-secrets
```











