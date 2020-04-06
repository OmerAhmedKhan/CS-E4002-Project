#!/usr/bin/env bash

sudo pip install mlflow
sudo pip install boto3
sudo pip install -U pandas
sudo pip install -U python-dateutil==2.6.1
sudo yum install nginx
sudo service nginx start

echo >> "location /mlflow {
 proxy_pass http://localhost:5000/;
 }" >> /etc/nginx/nginx.conf

sudo service nginx reload

mlflow server --default-artifact-root <add S3 bucket here> --host 0.0.0.0 &
