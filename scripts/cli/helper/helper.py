import subprocess
import os


def execute_build_push(name: str) -> None:
    subprocess.run(
        f"docker build -f {name}.Dockerfile -t annleefores/codepod-{name}:1.0.0 .".split(
            " "
        )
    )
    subprocess.run(f"docker push annleefores/codepod-{name}:1.0.0".split(" "))


def execute_kube(docker: str, k8s: str):
    subprocess.run(
        f"docker compose -f compose.yml -f k8s.compose.yml {docker}".split(" ")
    )
    os.chdir("k8s/codepod")
    subprocess.run(f"kubectl {k8s} -f ./".split(" "))


def execute(docker: str) -> None:
    subprocess.run(f"docker compose {docker}".split(" "))
