#!/usr/bin/env bash

sudo yum update -y
sudo amazon-linux-extras install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo yum -y install python-pip

sudo pip install mlflow
sudo pip install boto3
sudo pip install -U pandas
sudo pip install -U python-dateutil==2.6.1
sudo amazon-linux-extras install -y nginx1
sudo service nginx start

echo >> "location /mlflow {
 proxy_pass http://localhost:5000/;
 }" >> /etc/nginx/nginx.conf

sudo service nginx reload

mlflow server --default-artifact-root <add S3 bucket here> --host 0.0.0.0 &

mlflow server --default-artifact-root s3://mymlflowbucket/ --host 0.0.0.0 &
