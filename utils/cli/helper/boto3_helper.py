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

iam = boto3.client("iam")  # type: ignore

username = "kodiko"


def createAK() -> List[str]:
    resp = iam.create_access_key(UserName=username)
    access_key_data = resp.get("AccessKey")

    if access_key_data:
        return [
            access_key_data["AccessKeyId"],
            access_key_data["SecretAccessKey"],
        ]
    return ["NONE", "NONE"]


# make sure access key is present before parsing it
def deleteAK() -> None:
    access_key_list = iam.list_access_keys(UserName=username, MaxItems=1)

    if access_key_list["AccessKeyMetadata"]:
        access_key = access_key_list["AccessKeyMetadata"][0].get("AccessKeyId", "NONE")
        iam.delete_access_key(UserName=username, AccessKeyId=access_key)


def get_eks_vpc() -> str:
    eks_client = boto3.client("eks", region_name="ap-south-1")  # type: ignore
    response = eks_client.describe_cluster(name="kodiko")
    resourcesVpcConfig = response["cluster"].get("resourcesVpcConfig")
    if resourcesVpcConfig:
        vpc_id = resourcesVpcConfig.get("vpcId", "NONE")
        return vpc_id
    return "NONE"
