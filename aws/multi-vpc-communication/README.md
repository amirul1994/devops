Communication between two VPCs in AWS can happen in several ways. In this article, I will demonstrate two methods to ensure communication between two different VPCs.
a.      Transit Gateway
b.     VPC Peering
Transit Gateway
AWS Transit Gateway is a service used to connect multiple AWS VPCs or an AWS VPC and an on-premises network. It provides a single gateway for this connectivity. It allows you to create a global network by connecting VPCs and edge networks across multiple AWS regions.
The Transit Gateway follows the 'Hub and Spoke' model. The Transit Gateway plays the role of the 'Hub' and the VPCs act as the 'Spokes'.

Since the Transit Gateway manages how traffic is routed among all the connected networks, this allows for centralized control and a single network management system.
I have created two VPCs, one has two subnets – one public subnet and one private subnet. The private subnet gets the internet connectivity through the NAT gateway.  I have configured the bastion ec2 instance and put it in the public subnet and the nginx ec2 instance in the private subnet. In the other VPC, I have created another ec2 instance.
Configure Transit Gateway
VPC Dashboard > Transit gateways > Transit gateways


Click on ‘Create transit gateway’.

Other than giving the name, I kept everything default. At the bottom, I have clicked ‘Create transit gateway’. It takes time to be available.

The next step is to attach the Transit gateway to the respective VPCs and their particular subnet.
VPC Dashboard > Transit gateways > Transit gateway attachments

Click on ‘Create transit gateway attachment’.
The configuration is as follows.




 
Similarly, create a Transit Gateway Attachment for vpc-2.



And then, at the bottom click on ‘Create transit gateway attachment’.
Transit Gateway has its own route tables and other settings.


Configure route tables for the respective subnets.
First, configure vpc-1 private subnet’s route table.


‘Destination’ is the vpc-2 private subnet and ‘Target’ is ‘Transit Gateway’.

Click on ‘save changes’.
The next one is the vpc-2 private subnet.


Click on ‘save changes’.
Now ping the vpc-2 private subnet’s instance.

Ping succeeds, hence this is the proof of communication via Transit Gateway.
VPC Peering
VPC peering is a technique that enables communication between two VPCs. VPCs can be in the same AWS region or in different regions (inter-region VPC peering) if supported by AWS. This also allows communication between VPCs in different AWS accounts. VPC peering can simplify the management of multiple environments and facilitate the integration of applications and services across regions.

Configure VPC Peering
VPC Dashboard > Virtual Private Cloud > Peering connections





If the request is made from another account, the accepter has to accept the request to form VPC Peering.

Configure route tables for the respective subnets.
First, configure vpc-1 private subnet’s route table.



For vpc-2 private subnet

Select the ‘pcx-…….(vpc-1-vpc-2) and click on ‘Save changes’.
Now, ping from vpc-1-nginx to vpc-2-app.

Ping succeeds, hence this the proof of communication via Peering connection.
 
Advantage of AWS Transit Gateway over VPC Peering
With a Transit Gateway, once a VPC is attached, it can communicate with all other connected VPCs. This simplifies network management and scalability, as only a single attachment is needed for each VPC to enable communication with multiple VPCs.
In contrast, VPC peering requires establishing individual peering connections between each pair of VPCs. As the number of VPCs increases, the number of required peering connections grows exponentially, leading to increased complexity and management overhead.
