import pulumi
import pulumi_aws as aws 

class AwsInfrastructure:
    def __init__(self):
        self.create_vpc()
        self.create_public_subnet()
        self.create_internet_gateway()
        self.create_route_table()
        self.create_security_group()
        self.create_instances()
    
    def create_vpc(self):
        self.vpc = aws.ec2.Vpc("my-vpc",
            cidr_block = "10.0.0.0/16",
            tags={"Name":"my-vpc"}
            )
        pulumi.export("vpcId", self.vpc.id)
    
    def create_public_subnet(self):
        self.public_subnet = aws.ec2.Subnet("public-subnet",
            vpc_id = self.vpc.id,
            cidr_block = "10.0.1.0/24",
            availability_zone = "us-east-1a",
            map_public_ip_on_launch = True,
            tags = {"Name": "public-subnet"}
            )
        pulumi.export("publicSubnetId", self.public_subnet.id)
    
    def create_internet_gateway(self):
        self.igw = aws.ec2.InternetGateway("internet-gateway",
            vpc_id = self.vpc.id
            tags = {"Name": "igw"}
            )
        pulumi.export("igwId", self.igw.id)
    
    def create_route_table(self):
        self.public_route_table = aws.ec2.RouteTable("public-route-table",
            vpc_id = self.vpc.id,
            tags = {"Name": "rt-public"}
            )
        pulumi.export("publicRouteTableId", self.public_route_table.id)
    
        self.route = aws.ec2.Route("igw-route",
           route_table_id = self.public_route_table.id,
           destination_cidr_block = "0.0.0.0/0",
           gateway_id = self.igw.id
        )

        self.route_table_association = aws.ec2.RouteTableAssociation("public-route-table-association",
            subnet_id = self.public_subnet.id,
            route_table_id = self.public_route_table.id
        )

    def create_security_group(self):
        self.public_security_group = aws.ec2.SecurityGroup("public-secgrp",
            vpc_id = self.vpc.id,
            description = "Enable HTTP and SSH access for public instance",
            ingress = [{"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}],
            egress = [{"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}]
            )
    
    def create_instances(self):
        ami_id = "ami-060e277c0d4cce553"
        key_name = "MyKeyPair"

        self.nginx_instance = aws.ec2.Instance("nginx-instance",
            instance_type = "t2.micro",
            vpc_security_group_ids = [self.public_security_group.id],
            ami = ami_id,
            subnet_id = self.public_subnet.id,
            key_name = key_name,
            associate_public_ip_address = True,
            tags = {"Name": "nginx-lb"}
        )
        pulumi.export("publicInstanceId", self.nginx_instance.id)
        pulumi.export("publicInstanceIp", self.nginx_instance.public_ip)

        self.master_instance = aws.ec2.Instance("master-instance",
            instance_type="t3.small",
            vpc_security_group_ids = [self.public_security_group.id],
            ami = ami_id,
            subnet_id = self.public_subnet.id,
            key_name = key_name,
            associate_public_ip_address= True,
            tags = {"Name": "master"}
        )
        pulumi.export("masterInstanceId", self.master_instance.id)
        pulumi.export("masterInstanceIp", self.master_instance.public_ip)

        self.worker1_instance = aws.ec2.Instance("worker1-instance",
            instance_type = "t3.small",
            vpc_security_group_ids = [self.public_security_group.id]
            ami = ami_id,
            subnet_id = self.public_subnet.id,
            key_name = key_name,
            associate_public_ip_address= True,
            tags = {"Name":"worker1"}
        )
        pulumi.export("worker1InstanceId", self.worker1_instance.id)
        pulumi.export("worker1InstanceIp", self.worker1_instance.public_ip)

        self.worker2_instance = aws.ec2.Instance("worker2-instance",
            instance_type = "t3.small",
            vpc_security_group_ids = [self.public_security_group.id],
            ami = ami_id,
            subnet_id = self.public_subnet.id,
            key_name = key_name,
            associate_public_ip_address = True,
            tags = {"Name":"worker2"}
        )
        pulumi.export("worker2InstanceId", self.worker2_instance.id)
        pulumi.export("worker2InstanceIp", self.worker2_instance.public_ip)

aws_infra = AwsInfrastructure()
