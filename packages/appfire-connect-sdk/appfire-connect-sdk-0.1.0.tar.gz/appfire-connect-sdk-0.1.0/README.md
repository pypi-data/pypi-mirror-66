
# Appfire connect app SDK  
  
## What does it do?  
Creates a Atlassian Connect app template and provides a toolkit for deploying to AWS environment  
  
## Command Line Arguments  
```  
--verbose, -v : "verbose"  
--region, -r : "AWS region", default="us-east-1"  
--profile, -p : "AWS profile as the default environment", default="default"  
--env, -e : "personal, dev, test, stage or prod", default="personal"  
--stack, -s : "CDK stack to deploy", default="app", "core" or "app"  
--app-suffix, -as : "green" or nothing (not passing the argument)
```  
###### Note: see personal.env.yml or env.yml for personal or DTS/Prod environments respectively.  
  
## Run via Python  
```  
create-appfire-app -v  
```  
  
## Bootstrap app  
#### bootstraps CDK toolkit and initialises required services for appfire connect app to run  
```  
ac bootstrap   
``` 
## List stacks  
```  
ac list (or ac ls)  
```  
  
## Deploy app  
```  
ac deploy <stack-name>   
```
## Diff stack  
```
ac diff   
```
## Destroy stack  
```
ac destroy <stack-name> 
```