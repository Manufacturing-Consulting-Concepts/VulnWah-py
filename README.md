# README

### Setting up the tool

1. Configure Environmental Variables
   To ensure that variables persist through reboots and across all users, configure and custom shell script in
   /etc/profile.d/[custom.sh].
   Add in the following variables (add in bucket name value):

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






