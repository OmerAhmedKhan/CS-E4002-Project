# Deployment Process

  - Initiate AWS EC2 Instance
  - Install mlflow
  - Install pip pakages dependencies
  - Configure AWS credential
  - Upload codebase to support on-demand Deployment
  
  
  The built-in script attached will auomate this process which will spin everything up and running.
  You just need to configure your AWS credential manually which can also be automated but for this projec I let it be manual.
  To build everything inside EC2 instance, copy **build.sh** to instance through following command
  
  ```
  scp your_username@remotehost.edu:build.sh /some/local/directory 
  ```
  and then run this command on EC2 instance
  ```
 sh  /some/local/directory/build.sh
  ```
