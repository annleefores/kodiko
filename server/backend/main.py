from typing import Dict
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
from kubernetes.client.rest import ApiException
import logging


load_dotenv()

from utils.utils import generate_random_string, uuid_gen
from codepod_kube.codepod_kube import (
    create_ingress,
    create_pod,
    create_svc,
    delete_ingress,
    delete_pod,
    delete_svc,
)


app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Refactor k8s function call


@app.get("/api/create", status_code=status.HTTP_200_OK)
def create_codepod() -> Dict[str, str]:
    name = f"codepod-{generate_random_string(8)}"

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

    # Todo: Add some error fixing logic
    # print which function had errors
    for func, stat in exceptions.items():
        if stat:
            print(f"{func} caused an error")

    return {
        "success": "codepod created successfully",
        "pod_name": name,
        "pod_id": str(uuid_gen(name)),
    }


@app.get("/api/delete", status_code=status.HTTP_200_OK)
def delete_codepod(name: str) -> Dict[str, str]:
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

    # Todo: Add some error fixing logic
    # print which function had errors
    for func, stat in exceptions.items():
        if stat:
            print(f"{func} caused an error")

    return {"success": "codepod deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
