from typing import Any
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import os
from typing import List, Dict


if os.getenv("BACKEND_ENV") == "kube":
    config.load_kube_config()
else:
    config.load_incluster_config()


def create_pod(name: str, prev_name: str):
    v1 = client.CoreV1Api()

    if read_resources(v1, name, "pod") or (
        read_resources(v1, prev_name, "pod") if prev_name else False
    ):
        print(f"{name} pod already exists")
        return False

    print(f"Creating {name} pod...")

    pod_spec = client.V1PodSpec(
        containers=[
            client.V1Container(
                name="codepod",
                image="annleefores/codepod-prod:1.0.0",
                ports=[client.V1ContainerPort(container_port=5000)],
                image_pull_policy="IfNotPresent",
                resources=client.V1ResourceRequirements(
                    limits={"memory": "500Mi", "cpu": "1000m"}
                ),
                env_from=[
                    client.V1EnvFromSource(
                        secret_ref=client.V1SecretEnvSource(name=name)
                    )
                ],
            )
        ]
    )
    pod_metadata = client.V1ObjectMeta(name=name, labels={"app": name})
    pod_body = client.V1Pod(
        api_version="v1", kind="Pod", metadata=pod_metadata, spec=pod_spec
    )

    resp = v1.create_namespaced_pod(namespace="default", body=pod_body)

    return True


def delete_pod(name: str):
    v1 = client.CoreV1Api()

    if read_resources(v1, name, "pod") is False:
        print(f"{name} pod does not exist or already deleted....")
        return 1

    print(f"Deleting {name} pod....")

    resp = v1.delete_namespaced_pod(namespace="default", name=name)

    return resp


def create_svc(name: str, prev_name: str):
    v1 = client.CoreV1Api()

    if read_resources(v1, name, "service") or (
        read_resources(v1, prev_name, "service") if prev_name else False
    ):
        print(f"{name} service already exists")
        return False

    print(f"Creating {name} svc....")

    svc_metadata = client.V1ObjectMeta(name=name, labels={"app": name})

    svc_spec = client.V1ServiceSpec(
        selector={"app": name},
        type="ClusterIP",
        ports=[client.V1ServicePort(port=5000, target_port=5000)],
    )

    svc_body = client.V1Service(
        api_version="v1", kind="Service", metadata=svc_metadata, spec=svc_spec
    )

    resp = v1.create_namespaced_service(namespace="default", body=svc_body)

    return True


def delete_svc(name: str):
    v1 = client.CoreV1Api()

    if read_resources(v1, name, "service") is False:
        print(f"{name} service does not exist or already deleted....")
        return 1

    print(f"Deleting {name} svc....")

    resp = v1.delete_namespaced_service(namespace="default", name=name)

    return resp


# Ext Secret

group = "external-secrets.io"
version = "v1beta1"
plural = "externalsecrets"


def get_external_secret(v1: Any, name: str, namespace: str = "default") -> bool:
    resp = False

    try:
        resp = v1.get_namespaced_custom_object(
            group=group, version=version, namespace=namespace, plural=plural, name=name
        )
    except ApiException as e:
        if e.status != 404:
            print(f"Unknown error: {e}")
            exit(1)
    # return None or some response
    return resp


def create_external_secret(name: str, prev_name: str):
    v1 = client.CustomObjectsApi()

    if get_external_secret(
        v1=v1,
        name=name,
    ) or (get_external_secret(v1=v1, name=prev_name) if prev_name else False):
        print(f"{name} extSecret already exists")
        return False

    print(f"Creating {name} externalSecret....")

    # NOTE name should be something like codepod-secret

    # Add all AWS parameter store key vals here as dict
    data = {
        "COGNITO_CLIENT_ID": "/kodiko/backend/COGNITO_CLIENT_ID",
        "COGNITO_USER_POOL_ID": "/kodiko/backend/COGNITO_USER_POOL_ID",
    }

    # create data and data ref template for external secret

    # create key:key for template data
    data_template = {}

    # type declaration
    MyDictType = Dict[str, str | Dict[str, str]]
    MyListType = List[MyDictType]

    # create external secretRef template
    data_ref: MyListType = []

    for key, val in data.items():
        # the dict should be like this { "key" : "{{ .key }}" } for ext secret
        data_template[key] = f"{{{{ .{key}  }}}}"
        ref = {
            "secretKey": key,
            "remoteRef": {"key": val},
        }
        data_ref.append(ref)

    external_secret_body = {
        "apiVersion": "external-secrets.io/v1beta1",
        "kind": "ExternalSecret",
        "metadata": {"name": name},
        "spec": {
            "refreshInterval": "0",
            "secretStoreRef": {"name": "parameterstore", "kind": "SecretStore"},
            "target": {
                "name": name,
                "template": {
                    "engineVersion": "v2",
                    "data": data_template,
                },
            },
            "data": data_ref,
        },
    }

    resp = v1.create_namespaced_custom_object(
        group=group,
        version=version,
        namespace="default",
        plural=plural,
        body=external_secret_body,
    )

    return True


def delete_external_secret(name: str):
    v1 = client.CustomObjectsApi()

    if (
        get_external_secret(
            v1=v1,
            name=name,
        )
        is False
    ):
        print(f"{name} externalSecret does not exist or already deleted....")
        return 1

    print(f"Deleting {name} externalSecret....")

    resp = v1.delete_namespaced_custom_object(
        namespace="default",
        name=name,
        group=group,
        version=version,
        plural=plural,
        body=client.V1DeleteOptions(),
    )

    return resp


def create_ingress(name: str, prev_name: str):
    v1 = client.NetworkingV1Api()

    if read_resources(v1, name, "ingress") or (
        read_resources(v1, prev_name, "ingress") if prev_name else False
    ):
        print(f"{name} ingress already exists")
        return False

    print(f"Creating {name} ingress....")

    ingress_metadata = client.V1ObjectMeta(
        name=name,
        labels={"app": name},
        annotations={
            "nginx.ingress.kubernetes.io/proxy-read-timeout": "3600",
            "nginx.ingress.kubernetes.io/proxy-send-timeout": "3600",
        },
    )

    ingress_spec = client.V1IngressSpec(
        ingress_class_name="nginx",
        rules=[
            client.V1IngressRule(
                http=client.V1HTTPIngressRuleValue(
                    paths=[
                        client.V1HTTPIngressPath(
                            path_type="Prefix",
                            path="/ws/",
                            backend=client.V1IngressBackend(
                                service=client.V1IngressServiceBackend(
                                    name=name,
                                    port=client.V1ServiceBackendPort(
                                        number=5000,
                                    ),
                                )
                            ),
                        )
                    ]
                )
            )
        ],
    )

    ingress_body = client.V1Service(
        api_version="networking.k8s.io/v1",
        kind="Ingress",
        metadata=ingress_metadata,
        spec=ingress_spec,
    )

    resp = v1.create_namespaced_ingress(namespace="default", body=ingress_body)

    return True


def delete_ingress(name: str):
    v1 = client.NetworkingV1Api()

    if read_resources(v1, name, "ingress") is False:
        print(f"{name} ingress does not exist or already deleted....")
        return 1

    print(f"Deleting {name} ingress....")

    resp = v1.delete_namespaced_ingress(namespace="default", name=name)

    return resp


def read_resources(
    v1: Any,
    name: str,
    resource: str,
    namespace: str = "default",
) -> bool:
    resp = False

    try:
        method_name = f"read_namespaced_{resource}"
        get_method = getattr(v1, method_name)
        resp = get_method(name=name, namespace=namespace)
    except ApiException as e:
        if e.status != 404:
            print(f"Unknown error: {e}")
            exit(1)
    # return None or some response
    return resp
