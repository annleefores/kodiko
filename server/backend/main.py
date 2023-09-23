from typing import Dict
from fastapi import FastAPI, status
from dotenv import load_dotenv
import uvicorn
from kubernetes.client.rest import ApiException
import logging

load_dotenv()

from codepod_kube.codepod_kube import (
    create_ingress,
    create_pod,
    create_svc,
    delete_ingress,
    delete_pod,
    delete_svc,
)


app = FastAPI()


@app.get("/create", status_code=status.HTTP_201_CREATED)
def create_codepod() -> Dict[str, str]:
    # add randomness to pod name
    name = "codepod"

    exceptions = {
        "create_pod": False,
        "create_svc": False,
        "create_ingress": False,
    }

    # create pod
    try:
        created_pod_resp = create_pod(name=name)
    except ApiException as e:
        logging.exception("Exception when calling CoreV1Api->create_namespaced_pod:")
        exceptions["create_pod"] = True

    # create svc
    try:
        created_svc_resp = create_svc(name=name)
    except ApiException as e:
        logging.exception(
            "Exception when calling CoreV1Api->create_namespaced_service:"
        )
        exceptions["create_svc"] = True

    # create ingress
    try:
        created_ingress_resp = create_ingress(name=name)
    except ApiException as e:
        logging.exception(
            "Exception when calling NetworkingV1Api->create_namespaced_ingress:",
        )
        exceptions["create_ingress"] = True

    for func, stat in exceptions.items():
        if stat:
            print(f"{func} caused an error")

    return {"success": "codepod created successfully", "pod_name": name}


@app.get("/delete", status_code=status.HTTP_201_CREATED)
def delete_codepod() -> Dict[str, str]:
    # get name from client
    name = "codepod"

    exceptions = {
        "delete_pod": False,
        "delete_svc": False,
        "delete_ingress": False,
    }

    # delete pod
    try:
        deleted_pod_resp = delete_pod(name=name)
    except ApiException as e:
        logging.exception("Exception when calling CoreV1Api->delete_namespaced_pod")
        exceptions["delete_pod"] = True

    # delete svc
    try:
        deleted_svc_resp = delete_svc(name=name)
    except ApiException as e:
        logging.exception("Exception when calling CoreV1Api->delete_namespaced_service")
        exceptions["delete_svc"] = True

    # delete ingress
    try:
        deleted_ingress_resp = delete_ingress(name=name)
    except ApiException as e:
        logging.exception("Exception when calling CoreV1Api->delete_namespaced_service")

        exceptions["delete_ingress"] = True

    for func, stat in exceptions.items():
        if stat:
            print(f"{func} caused an error")

    return {"success": "codepod deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
