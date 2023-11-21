from typing import List
import boto3

# Create an IAM user (kodiko) with ssm:GetParameter* permission
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "VisualEditor0",
#             "Effect": "Allow",
#             "Action": "ssm:GetParameter*",
#             "Resource": "arn:aws:ssm:<region>:<accountID>:parameter/kodiko/*"
#         }
#     ]
# }


class SSM:
    def __init__(self) -> None:
        self.param = boto3.client("ssm", region_name="ap-south-1")  # type: ignore

    def get_val(self, name: str):
        response = self.param.get_parameter(Name=name)
        val: str | None = response["Parameter"].get("Value")
        return val

    # Make sure accesskey and secret is saved as stringlist, without any space between them. the separator must be a single comma
    def getAK(self) -> List[str]:
        val = self.get_val(name="/kodiko/backend/ACCESS_CREDS")
        if val:
            return val.split(",")
        return ["NONE", "NONE"]


def get_eks_vpc() -> str:
    eks_client = boto3.client("eks", region_name="ap-south-1")  # type: ignore
    response = eks_client.describe_cluster(name="kodiko")
    resourcesVpcConfig = response["cluster"].get("resourcesVpcConfig")
    if resourcesVpcConfig:
        vpc_id = resourcesVpcConfig.get("vpcId", "NONE")
        return vpc_id
    return "NONE"
