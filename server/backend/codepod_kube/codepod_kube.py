from typing import Dict
from kubernetes import client, config, utils
import os

if os.getenv("BACKEND_ENV") == "kube":
    config.load_kube_config()
else:
    config.load_incluster_config()

k8s_client = client.ApiClient()


def create() -> Dict[str, str]:
    codepod_yaml_file = "manifest/codepod.yml"
    utils.create_from_yaml(k8s_client, codepod_yaml_file, verbose=True)
    codepod_ingress_yaml_file = "manifest/codepod-ingress.yml"
    utils.create_from_yaml(k8s_client, codepod_ingress_yaml_file, verbose=True)
