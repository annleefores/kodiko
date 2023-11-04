# type: ignore

import boto3

client = boto3.client("iam")

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

username = "kodiko"


def createAK():
    resp = client.create_access_key(UserName=username)
    return resp.get("AccessKey")


def deleteAK():
    access_key_list = client.list_access_keys(
        UserName=username,
    )
    access_key = access_key_list.get("AccessKeyMetadata")[0]["AccessKeyId"]
    resp = client.delete_access_key(UserName=username, AccessKeyId=access_key)
