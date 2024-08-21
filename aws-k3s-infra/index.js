const pulumi = require("@pulumi/pulumi");
const aws = require("@pulumi/aws");

// Create a VPC
const vpc = new aws.ec2.Vpc("my-vpc", {
    cidrBlock: "10.0.0.0/16",
    tags: {
        Name: "my-vpc"
    }
});
exports.vpcId = vpc.id;

// Create a public subnet
const publicSubnet = new aws.ec2.Subnet("public-subnet", {
    vpcId: vpc.id,
    cidrBlock: "10.0.1.0/24",
    availabilityZone: "us-east-1a",
    mapPublicIpOnLaunch: true,
    tags: {
        Name: "public-subnet"
    }
});
exports.publicSubnetId = publicSubnet.id;

// Create an Internet Gateway
const igw = new aws.ec2.InternetGateway("internet-gateway", {
    vpcId: vpc.id,
    tags: {
        Name: "internet-gateway"
    }
});
exports.igwId = igw.id;

// Create a route table
const publicRouteTable = new aws.ec2.RouteTable("public-route-table", {
    vpcId: vpc.id,
    tags: {
        Name: "rt-public"
    }
});

// Create a route in the route table for the Internet Gateway
const route = new aws.ec2.Route("igw-route", {
    routeTableId: publicRouteTable.id,
    destinationCidrBlock: "0.0.0.0/0",
    gatewayId: igw.id
});

// Associate the route table with the public subnet
const routeTableAssociation = new aws.ec2.RouteTableAssociation("public-route-table-association", {
    subnetId: publicSubnet.id,
    routeTableId: publicRouteTable.id
});
exports.publicRouteTableId = publicRouteTable.id;

// Create a security group for the public instance
const publicSecurityGroup = new aws.ec2.SecurityGroup("public-secgrp", {
    vpcId: vpc.id,
    description: "Enable HTTP and SSH access for public instance",
    ingress: [
        { protocol: "tcp", fromPort: 80, toPort: 80, cidrBlocks: ["0.0.0.0/0"] },
        { protocol: "tcp", fromPort: 22, toPort: 22, cidrBlocks: ["0.0.0.0/0"] },
        { protocol: "tcp", fromPort: 6443, toPort: 6443, cidrBlocks: ["10.0.0.0/16"]},
        { protocol: "tcp", fromPort: 30001, toPort: 30001, cidrBlocks: ["0.0.0.0/0"]},
        { protocol: "udp", fromPort: 8472, toPort: 8472, cidrBlocks: ["10.0.0.0/16"]},
        { protocol: "tcp", fromPort: 2379, toPort: 2380, cidrBlocks: ["10.0.0.0/16"]}
    ],
    egress: [
        { protocol: "-1", fromPort: 0, toPort: 0, cidrBlocks: ["0.0.0.0/0"] }
    ]
});

// Use the specified Ubuntu 24.04 LTS AMI
const amiId = "ami-04a81a99f5ec58529";

// Create nginx instance
const nginxInstance = new aws.ec2.Instance("nginx-instance", {
    instanceType: "t2.micro",
    vpcSecurityGroupIds: [publicSecurityGroup.id],
    ami: amiId,
    subnetId: publicSubnet.id,
    keyName: "MyKeyPair",
    associatePublicIpAddress: true,
    tags: {
        Name: "nginx-lb"
    }
});
exports.nginxInstanceId = nginxInstance.id;
exports.nginxInstanceIp = nginxInstance.publicIp;

// Create master instance
const masterInstance = new aws.ec2.Instance("master-instance", {
    instanceType: "t3.small",
    vpcSecurityGroupIds: [publicSecurityGroup.id],
    ami: amiId,
    subnetId: publicSubnet.id,
    keyName: "MyKeyPair",
    associatePublicIpAddress: true,
    tags: {
        Name: "master"
    }
});
exports.masterInstanceId = masterInstance.id;
exports.masterInstanceIp = masterInstance.publicIp;

// Create worker1 instance
const worker1Instance = new aws.ec2.Instance("worker1-instance", {
    instanceType: "t3.small",
    vpcSecurityGroupIds: [publicSecurityGroup.id],
    ami: amiId,
    subnetId: publicSubnet.id,
    keyName: "MyKeyPair",
    associatePublicIpAddress: true,
    tags: {
        Name: "worker1"
    }
});
exports.worker1InstanceId = worker1Instance.id;
exports.worker1InstanceIp = worker1Instance.publicIp;

// Create worker2 instance
const worker2Instance = new aws.ec2.Instance("worker2-instance", {
    instanceType: "t3.small",
    vpcSecurityGroupIds: [publicSecurityGroup.id],
    ami: amiId,
    subnetId: publicSubnet.id,
    keyName: "MyKeyPair",
    associatePublicIpAddress: true,
    tags: {
        Name: "worker2"
    }
});
exports.worker2InstanceId = worker2Instance.id;
exports.worker2InstanceIp = worker2Instance.publicIp;
