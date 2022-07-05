#!/usr/bin/python3
import boto3
import botocore
from prettytable import PrettyTable
import argparse

parser = argparse.ArgumentParser(description='lists ec2 instances and eks clusters for particular owner')
# Add required arguments to the parser
parser.add_argument('-o','--owner',
                    type=str,
                    default=None,
                    help='Enter owner name'
                    )   
# Add optional arguments to the parser
parser.add_argument('-l', '--list',
                    action='store_true',
                    help='enlist all the owners'
                    )  
parser.add_argument('-ec2','--instances',
                    action='store_true',
                    help='Enlists all ec2 instances'
                    )
parser.add_argument('-eks','--clusters',
                    action='store_true',
                    help='Enlists all eks clusters'
                    )

args=parser.parse_args()

#Listing all EC2 instances
x=PrettyTable()
x.field_names=["Name", "Region", "Id", "Status", "Owner"]
regions = ["us-east-2", "us-west-2"]
for x1 in regions:
    try:
        Region=x1
        client=boto3.client('ec2', region_name=x1)
        ecs=client.describe_instances()
        for x2 in ecs['Reservations']:
            for x3 in x2['Instances']:
                name=x3['InstanceId']
                for x4 in x3['Tags']:
                    if x4['Key']=='Name':
                        name=x4['Value']
                        owner=name.split('-')[0]
                x.add_row([name, x1, x3['InstanceId'], x3['State']['Name'],owner])
    except:
        pass

#Listing all EKS clusters
y=PrettyTable()
y.field_names=["Name","Cluster Name", "Status", "Owner"]
client2=boto3.client('eks')
resp=client2.list_clusters()
for x5 in resp['clusters']:
    eks=client2.describe_cluster(name=x5)
    clusterName=eks['cluster']['tags']['Name']
    name=eks['cluster']['name']
    owner=name.split('-')[0]
    status=eks['cluster']['status']
    y.add_row([clusterName, name, status, owner])

#for ec2 instances
q=PrettyTable(print_empty=False)
q.title = "EC2 Instances"
q.field_names = ["Name", "Region", "Id", "Status", "Owner"]
res1=[]
for row in x:
    row.border = False
    row.header = False
    z = row.get_string(fields=["Owner"]).strip()
    if z not in res1:
        res1.append(z)
    if z==args.owner:
        s=row.get_string()
        data=s.split() #split string into a list
        q.add_row([data[0],data[1],data[2],data[3],data[4]])
        #print(data)

#for eks cluster
w=PrettyTable(print_empty=False)
w.title = "EKS Clusters"
w.field_names = ["name","Cluster Name", "Status", "Owner"]
res2=[]
for row in y:
    row.border = False
    row.header = False
    z =  row.get_string(fields=["Owner"]).strip()
    if z not in res2:
        res2.append(z)
    if z==args.owner:
        r=row.get_string()
        data=r.split()
        w.add_row([data[0],data[1],data[2],data[3]])

if args.list:
    res=list(set(res1+res2))
    print("  ".join(res))

if args.instances:
    print(x)

if args.clusters:
    print(y)

try:
    if q.rows[0][4]==args.owner:
        print(q)
except:
    if args.owner!=None and args.owner not in res1:
        print('No EC2 instances for the user {}'. format(args.owner))

try:
    if w.rows[0][3]==args.owner:
        print(w)
except:
    if args.owner!=None and args.owner not in res2:
        print('No EKS clusters for the user {}'. format(args.owner))
















