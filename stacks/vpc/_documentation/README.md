# AWS VPC with Security Groups

## Description
This stack creates an AWS Virtual Private Cloud (VPC).

## Variables

### Required Variables

| Name | Description | Default |
|------|-------------|---------|
| vpc_name | VPC network name | &nbsp; |

### Optional Variables

| Name | Description | Default |
|------|-------------|---------|
| aws_default_region | Default AWS region | eu-west-1 |

## Dependencies

### Substacks
- [config0-publish:::tf_executor](http://config0.http.redirects.s3-website-us-east-1.amazonaws.com/assets/stacks/config0-publish/tf_executor/default)

### Execgroups
- [williaumwu:::config0-test2::vpc](http://config0.http.redirects.s3-website-us-east-1.amazonaws.com/assets/exec/groups/williaumwu/config0-test2/vpc/default)
