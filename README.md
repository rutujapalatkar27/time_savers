# time_savers

## Introduction 
AWS Resources Script Project 
This project contains custom designed script for listing EC2 and EKS clusters and more. 

## prerequisites
1. install aws cli tool
$ curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
$ sudo installer -pkg AWSCLIV2.pkg -target /

2. open aws credentials file and update your programmatic access credentials
$ vi ~/.aws/credentials

3. Install AWS SDK for python (Boto3)
$ pip install boto3

4. Install python 
$ sudo apt update
$ sudo apt install python3

## run the script

1. lists all the users
$ python3 starter.py -l 

2. lists all ec2 instances
$ python3 starter.py -ec2

3. lists all eks clusters
$ python3 starter.py -eks

4. lists all ec2 and eks for particular user
$ python3 starter.py -o <user_name>
