# README

### Summary

VulnWah-py is a tool that is used to aggregate vulnerability reports from Wazuh.
After aggregating the reports from each agent, a unified JSON object is uploaded to
AWS S3.  This makes it easier for third part risk management tools to interface with vulnerability finding from Wazuh.

#### The Problem
Disparate Vulnerability reports.

#### The Solution
Centralizing reporting from the desperate sources.

#### Future Interactions
Ultimating, the goal is to create a normalization framework that can ingest reports from different sources and write
them to a dynamoDB table that can be interfaced with using Jupyter Notebooks.

#### Setting up the tool

1. Configure Environmental Variables
To ensure that variables persist through reboots and across all users, configure and custom shell script in
/etc/profile.d/[custom.sh]. Add in the following variables (add in bucket name value):

```shell
export S3_BUCKET_NAME='s3_bucket_name'
```

2. Install the AWS CLI


```shell
pip3 install awscli
```

3. Configure AWS CLI

```shell
aws configure
```

Ensure that the user that will be configured has the correct permissions to access the S3 bucket.






