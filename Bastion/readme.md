# Ec2 Bastion Instance  
This CloudFormation template deploys an EC2-based Bastion Instance into an isolated Virtual Private Cloud {VPC).  The Bastion Instance comes pre-loaded with the command line utilities and other software needed to perform deployment deployment and validation tasks across the exercises and project tasks in this course.  

## Step 1 - Download Template
Prior to deploying the Bastion Instance, you must download the CloudFormation template from the link below:

[https://raw.githubusercontent.com/udacity/CD14673-Deploy-and-Manage-Azure-Compute-Resources-Public/refs/heads/main/Bastion/template.yaml](https://raw.githubusercontent.com/udacity/CD14673-Deploy-and-Manage-Azure-Compute-Resources-Public/refs/heads/main/Bastion/template.yaml)

## Step 2 - Deployment  
To deploy the CloudFormation template, visit the CloudFormation console within your AWS Account.  Begin deployment by using the **Create Stack** wizard.  Use any name desired for the name of the CloudFormation stack.  When prompted, indicate that you will upload a template file and provide the file downloaded from Step 1 above.


**Enable IAM Resource Creation**  
At Step 3 of the Create Stack wizard titled "Configure stack options", you will be prompted to indicate Capabilities.  Check the box to indicating ***"I acknowledge that AWS CloudFormation might create IAM resources."***

![../Img/iam_capab.png](../Img/iam_capab.png)

## Step 3 - Connect to the Bastion

Once complete, the CloudFormation stack will provide an output named **BastionSSMConsoleLine**.  The value of this output contains a link to being an AWS Systems Manager (SSM) connection to the bastion instance.  This connection will allow you to execute local commands on the instance from within the browser.  This can also be achieved by locating the bastion instance in the Ec2 Console, using the Connect wizard, and selecting the SSM option.