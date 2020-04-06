import argparse
import mlflow
import mlflow.sagemaker as sagemaker
import boto3
import os

region = 'eu-west-1'
port = 1234
#TODO Get it from user
#exp_name = 'direct-marketing-xgboost'
execution_role_arn = 'arn:aws:iam::438478214470:role/service-role/AmazonSageMaker-ExecutionRole-20200324T112499'


def execute_training(model_path, app_name, local=True):
    if local:
        sagemaker.run_local(model_path, port=1234)
        return

    os.system('mlflow sagemaker build-and-push-container -c oak')
    ecr_client = boto3.client('ecr')
    try:
        image_uri = ecr_client.describe_repositories(repositoryNames=[app_name])['repositories'][0]
    except ecr_client.exceptions.RepositoryNotFoundException:
        print('Image not found on Cloud')

    image_uri = '{}:1.7.2'.format(image_uri.get('repositoryUri'))
    print(image_uri)
    return model_path, image_uri

def deploy_endpoints(app_name, model_path, execution_role_arn, image_uri):
    mlflow.sagemaker.deploy(app_name, model_path, execution_role_arn, image_url=image_uri, region_name=region)
    return

if __name__ == '__main__':
    model_path, image_uri = execute_training('s3://mymlflowbucket/1/4fbf57f6de5e4f41bd2dbc3c7cdf25cf/artifacts/oak-marketing-xgboost-model/', 'oak', False)
    #deploy_endpoints('oak', model_path, execution_role_arn, image_uri)