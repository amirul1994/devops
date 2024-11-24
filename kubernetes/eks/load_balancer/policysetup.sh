#!/bin/bash

# Define the policy document
POLICY_DOCUMENT='{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "elasticloadbalancing:*",
                "ec2:DescribeAvailabilityZones",
                "ec2:CreateSecurityGroup",
                "ec2:CreateTags",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:DescribeInternetGateways",
                "shield:GetSubscriptionState",
                "ec2:DescribeAccountAttributes",
                "iam:CreateServiceLinkedRole",
                "wafv2:GetWebACLForResource",
                "ec2:DeleteSecurityGroup",
                "waf-regional:GetWebACLForResource",
                "ec2:RevokeSecurityGroupIngress",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeTargetGroups",
                "elasticloadbalancing:DescribeListeners",
                "elasticloadbalancing:DescribeRules",
                "elasticloadbalancing:CreateLoadBalancer",
                "elasticloadbalancing:CreateTargetGroup",
                "elasticloadbalancing:CreateListener",
                "elasticloadbalancing:CreateRule",
                "elasticloadbalancing:DeleteLoadBalancer",
                "elasticloadbalancing:DeleteTargetGroup",
                "elasticloadbalancing:DeleteListener",
                "elasticloadbalancing:DeleteRule",
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:DeregisterTargets",
                "elasticloadbalancing:SetIpAddressType",
                "elasticloadbalancing:SetSecurityGroups",
                "elasticloadbalancing:SetSubnets",
                "elasticloadbalancing:ModifyLoadBalancerAttributes",
                "elasticloadbalancing:ModifyTargetGroup",
                "elasticloadbalancing:ModifyTargetGroupAttributes"
            ],
            "Resource": "*"
        }
    ]
}'

# Create the policy
POLICY_ARN=$(aws iam create-policy --policy-name CombinedAdditionalPolicy --policy-document "$POLICY_DOCUMENT" --query 'Policy.Arn' --output text)

# Get the instance role name from CloudFormation stack
ROLE_NAME=$(aws cloudformation describe-stacks --stack-name eks-cluster-stack --query 'Stacks[0].Outputs[?OutputKey==`NodeInstanceRole`].OutputValue' --output text | cut -d'/' -f2)

# Attach the policy to the instance role
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn $POLICY_ARNroot@aws-client:~#