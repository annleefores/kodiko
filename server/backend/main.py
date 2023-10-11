import json
from typing import Dict
from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
from kubernetes.client.rest import ApiException
import logging
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os


load_dotenv()

from lib.utils import base64_encoder_decoder, generate_random_string, uuid_gen
from lib.congito_jwt_token import CognitoJwtToken
from codepod_kube.codepod_kube import (
    create_ingress,
    create_pod,
    create_svc,
    delete_ingress,
    delete_pod,
    delete_svc,
)


class Item(BaseModel):
    name: str


app = FastAPI()


# TODO: Refactor k8s function call

unauth_routes = ["/docs", "/redoc", "/openapi.json"]


@app.middleware("http")
async def verify_token(request: Request, call_next):
    token = request.headers.get("authorization")

    print(token)

    # unauth routes
    if os.getenv("ENV") == "DEV":
        if request.url.path in unauth_routes:
            # return response from path
            response = await call_next(request)
            return response

    # auth routes
    if token is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content="Add a valid bearer token"
        )

    auth = CognitoJwtToken(token=token)

    try:
        claims = auth.verify()
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=str(e))

    # return response from path
    response = await call_next(request)

    return response


@app.post("/api/dummy", status_code=status.HTTP_200_OK)
def dummy(item: Item):
    pod_data = {"pod_name": item.name, "pod_id": str(uuid_gen(item.name))}

    return {
        "success": "codepod created successfully",
        "pod_data": base64_encoder_decoder(data=json.dumps(pod_data), to_encode=True),
    }


@app.post("/api/create", status_code=status.HTTP_200_OK)
def create_codepod(item: Item) -> Dict[str, str]:
    # To check if user has a codepod running
    prev_name = item.name

    name = f"codepod-{generate_random_string(8)}"

    exceptions = {
        "create_pod": False,
        "create_svc": False,
        "create_ingress": False,
        "pod_already_exists": 0,
    }

    # create pod
    try:
        created_pod_resp = create_pod(name=name, prev_name=prev_name)
        if not created_pod_resp:
            exceptions["pod_already_exists"] += 1
    except ApiException as e:
        logging.exception("Exception when calling CoreV1Api->create_namespaced_pod:")
        exceptions["create_pod"] = True

    # create svc
    try:
        created_svc_resp = create_svc(name=name, prev_name=prev_name)
        if not created_svc_resp:
            exceptions["pod_already_exists"] += 1
    except ApiException as e:
        logging.exception(
            "Exception when calling CoreV1Api->create_namespaced_service:"
        )
        exceptions["create_svc"] = True

    # create ingress
    try:
        created_ingress_resp = create_ingress(name=name, prev_name=prev_name)
        if not created_ingress_resp:
            exceptions["pod_already_exists"] += 1
    except ApiException as e:
        logging.exception(
            "Exception when calling NetworkingV1Api->create_namespaced_ingress:",
        )
        exceptions["create_ingress"] = True

    # Todo: Add some error fixing logic
    # print which function had errors
    for func, stat in exceptions.items():
        if stat:
            print(f"{func} encountered an issue")

    # if user has a codepod already running, send back previous details
    if exceptions["pod_already_exists"] == 3:
        name = prev_name

    return {
        "success": "codepod created successfully",
        "pod_name": name,
        "pod_id": str(uuid_gen(name)),
    }


@app.post("/api/delete", status_code=status.HTTP_200_OK)
def delete_codepod(item: Item) -> Dict[str, str]:
    name = item.name

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
