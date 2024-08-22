import pulumi
import pulumi_aws as aws
import pulumi_aws.ec2 as ec2
from pulumi_aws.ec2 import SecurityGroupRuleArgs

# configuration 
config = pulumi.Config()
instance_type = 't3.small'
ami = "ami-0e86e20dae9224db8"

#create a vpc
vpc = ec2.Vpc(
    'my-vpc',
    cidr_block='10.0.0.0/16',
    enable_dns_hostnames=True,
    enable_dns_support=True
)


# Create subnets
public_subnet = ec2.Subnet('public-subnet',
    vpc_id=vpc.id,
    cidr_block='10.0.1.0/24',
    map_public_ip_on_launch=True,
    availability_zone='us-east-1a'
)

private_subnet = ec2.Subnet('private-subnet',
    vpc_id=vpc.id,
    cidr_block='10.0.2.0/24',
    map_public_ip_on_launch=False,
    availability_zone='us-east-1a'
)

# Internet Gateway
igw = ec2.InternetGateway('internet-gateway', vpc_id=vpc.id)

# Route Table for Public Subnet
public_route_table = ec2.RouteTable('public-route-table', 
    vpc_id=vpc.id,
    routes=[{
        'cidr_block': '0.0.0.0/0',
        'gateway_id': igw.id,
    }]
)

# Associate the public route table with the public subnet

public_route_table_association = ec2.RouteTableAssociation(
    'public-route-table-association',
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id
)


# Elastic IP for NAT Gateway
eip = ec2.Eip('nat-eip', vpc=True)

# NAT Gateway
nat_gateway = ec2.NatGateway(
    'nat-gateway',
    subnet_id=public_subnet.id,
    allocation_id=eip.id
)


# Route Table for Private Subnet
private_route_table = ec2.RouteTable(
    'private-route-table', 
    vpc_id=vpc.id,
    routes=[{
        'cidr_block': '0.0.0.0/0',
        'nat_gateway_id': nat_gateway.id,
    }]
)

# Associate the private route table with the private subnet
private_route_table_association = ec2.RouteTableAssociation(
    'private-route-table-association',
    subnet_id=private_subnet.id,
    route_table_id=private_route_table.id
)

