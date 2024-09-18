Communication between two VPCs in AWS can happen in several ways. In this article, I will demonstrate two methods to ensure communication between two different VPCs.

a. Transit Gateway

b. VPC Peering

Transit Gateway
AWS Transit Gateway is a service used to connect multiple AWS VPCs or an AWS VPC and an on-premises network. It provides a single gateway for this connectivity. It allows you to create a global network by connecting VPCs and edge networks across multiple AWS regions.
The Transit Gateway follows the 'Hub and Spoke' model. The Transit Gateway plays the role of the 'Hub' and the VPCs act as the 'Spokes'.

![image](https://github.com/Amirul1994/devops/assets/119165587/a76f745f-1724-400a-8dba-d4396d63f86b)

Since the Transit Gateway manages how traffic is routed among all the connected networks, this allows for centralized control and a single network management system.
I have created two VPCs, one has two subnets – one public subnet and one private subnet. The private subnet gets the internet connectivity through the NAT gateway.  I have configured the bastion ec2 instance and put it in the public subnet and the nginx ec2 instance in the private subnet. In the other VPC, I have created another ec2 instance.

Configure Transit Gateway
VPC Dashboard > Transit gateways > Transit gateways

![image](https://github.com/Amirul1994/devops/assets/119165587/1f48f2ea-d440-4597-93da-fc6d7935c1cf)

Click on ‘Create transit gateway’.

![image](https://github.com/Amirul1994/devops/assets/119165587/9ff56966-68bc-4c53-907b-f1ffc978f48e)

Other than giving the name, I kept everything default. At the bottom, I have clicked ‘Create transit gateway’. It takes time to be available.

![image](https://github.com/Amirul1994/devops/assets/119165587/d953c203-2d9e-4e21-b88c-888ff9fbd7ec)

The next step is to attach the Transit gateway to the respective VPCs and their particular subnet.

VPC Dashboard > Transit gateways > Transit gateway attachments

![image](https://github.com/Amirul1994/devops/assets/119165587/d7de3da3-5b34-43a8-a326-7e653672290d)

Click on ‘Create transit gateway attachment’.

The configuration is as follows.

![image](https://github.com/Amirul1994/devops/assets/119165587/446b677b-0f6c-4cb0-a7c3-307a97791fb8)

![image](https://github.com/Amirul1994/devops/assets/119165587/62a64266-5b7d-4c22-9dbf-c40c0c20d19a)

![image](https://github.com/Amirul1994/devops/assets/119165587/def0a7ab-2887-4120-9609-c68c6bd3f9ba)

![image](https://github.com/Amirul1994/devops/assets/119165587/a3c03eef-8f92-400c-8047-3cdf5a7d3a86)

Similarly, create a Transit Gateway Attachment for vpc-2.

![image](https://github.com/Amirul1994/devops/assets/119165587/e3ba8a6f-585f-4510-9813-9aae8e8274ab)

![image](https://github.com/Amirul1994/devops/assets/119165587/b1337726-a9e2-498d-8809-aa30ab8bdd1b)

And then, at the bottom click on ‘Create transit gateway attachment’.

Transit Gateway has its own route tables and other settings.

![image](https://github.com/Amirul1994/devops/assets/119165587/05b6cf04-73e8-4adc-8bb1-7ec951450a4c)

![image](https://github.com/Amirul1994/devops/assets/119165587/f23edef4-eb35-4aa1-b663-4fea5d518170)

Configure route tables for the respective subnets.
First, configure vpc-1 private subnet’s route table.

![image](https://github.com/Amirul1994/devops/assets/119165587/36e7a097-7033-4577-9a8f-5e8ea455dc28)

![image](https://github.com/Amirul1994/devops/assets/119165587/87f383c5-88e9-4a09-8a72-b825a028bc46)

‘Destination’ is the vpc-2 private subnet and ‘Target’ is ‘Transit Gateway’.

![iClick on ‘save changes’.

The next one is the vpc-2 private subnet.

![image](https://github.com/Amirul1994/devops/assets/119165587/245ba40e-1ae8-4ff4-9f17-c1bd56e982e5)

![image](https://github.com/Amirul1994/devops/assets/119165587/1eb76e9d-c542-4685-bead-2561d03d0994)

Click on ‘save changes’.

Now ping the vpc-2 private subnet’s instance.

![image](https://github.com/Amirul1994/devops/assets/119165587/d15a278f-c1d0-47c7-8791-a246f2b91688)

Ping succeeds, hence this is the proof of communication via Transit Gateway.

VPC Peering
VPC peering is a technique that enables communication between two VPCs. VPCs can be in the same AWS region or in different regions (inter-region VPC peering) if supported by AWS. This also allows communication between VPCs in different AWS accounts. VPC peering can simplify the management of multiple environments and facilitate the integration of applications and services across regions.

![image](https://github.com/Amirul1994/devops/assets/119165587/05d4d199-53b2-4553-9129-742cd7d9efd6)

Configure VPC Peering 

VPC Dashboard > Virtual Private Cloud > Peering connections

![image](https://github.com/Amirul1994/devops/assets/119165587/62aabc75-2986-41d6-a902-862f7375562d)

![image](https://github.com/Amirul1994/devops/assets/119165587/6f3c134a-dbfd-4727-b084-cdd3226363f4)

![image](https://github.com/Amirul1994/devops/assets/119165587/c19a0b11-74c8-496d-8e66-ec74779665cf)

![image](https://github.com/Amirul1994/devops/assets/119165587/087d86b9-3cf8-44d6-a48c-2627a908e79a)

![image](https://github.com/Amirul1994/devops/assets/119165587/c541d1e2-f326-42ec-af60-8e0ab4470673)

If the request is made from another account, the accepter has to accept the request to form VPC Peering.

![image](https://github.com/Amirul1994/devops/assets/119165587/0ef9f2c4-704e-4fbe-9ad0-35af690bc152)

Configure route tables for the respective subnets.

First, configure vpc-1 private subnet’s route table.

![image](https://github.com/Amirul1994/devops/assets/119165587/76741e5b-2775-444b-8fbe-8e07c0f839f3)

![image](https://github.com/Amirul1994/devops/assets/119165587/08426213-6692-450f-a715-ff14fcacd8b9)

![image](https://github.com/Amirul1994/devops/assets/119165587/284c4dde-4c82-47c5-b348-ebb7b17ad77f)

For vpc-2 private subnet 

![image](https://github.com/Amirul1994/devops/assets/119165587/fb314ff9-5e09-49ec-b861-acd784e6e7e1)

Select the ‘pcx-…….(vpc-1-vpc-2) and click on ‘Save changes’.

Now, ping from vpc-1-nginx to vpc-2-app

![image](https://github.com/Amirul1994/devops/assets/119165587/dd46a9d0-2e5e-485f-8683-89b48fc8daf9)

Ping succeeds, hence this the proof of communication via Peering connection.

Advantage of AWS Transit Gateway over VPC Peering

With a Transit Gateway, once a VPC is attached, it can communicate with all other connected VPCs. This simplifies network management and scalability, as only a single attachment is needed for each VPC to enable communication with multiple VPCs.

In contrast, VPC peering requires establishing individual peering connections between each pair of VPCs. As the number of VPCs increases, the number of required peering connections grows exponentially, leading to increased complexity and management overhead.
