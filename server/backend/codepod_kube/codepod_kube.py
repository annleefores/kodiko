from kubernetes import client, config, utils
import os


def main():
    if os.getenv("BACKEND_DEV_ENV"):
        config.load_kube_config()
    else:
        config.load_incluster_config()  # From a pod within the cluster

    k8s_client = client.ApiClient()
    codepod_yaml_file = "manifest/codepod.yml"
    utils.create_from_yaml(k8s_client, codepod_yaml_file, verbose=True)
    codepod_ingress_yaml_file = "manifest/codepod-ingress.yml"
    utils.create_from_yaml(k8s_client, codepod_ingress_yaml_file, verbose=True)
