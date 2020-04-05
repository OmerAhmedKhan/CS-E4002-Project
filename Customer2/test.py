import boto3

x = boto3.client('ecr')
print(x.describe_repositories()['repositories'])