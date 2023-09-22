import subprocess


def execute_build_push(name: str) -> None:
    subprocess.run(
        f"docker build -f {name}.Dockerfile -t annleefores/codepod-{name}:1.0.0 .".split(
            " "
        )
    )
    subprocess.run(f"docker push annleefores/codepod-{name}:1.0.0".split(" "))


def execute_kube(docker: str, k8s: str):
    if k8s == "apply":
        # Build codepod-prod image
        subprocess.run(
            "docker build -f ./server/codepod/Dockerfile -t annleefores/codepod-prod:1.0.0 ./server/codepod/".split(
                " "
            )
        )
        # Build backend image
        subprocess.run(
            "docker build -f ./server/backend/Dockerfile -t annleefores/backend:1.0.0 ./server/backend/".split(
                " "
            )
        )
    subprocess.run(f"kubectl {k8s} -f ./k8s/backend".split(" "))
    subprocess.run(
        f"docker compose -f compose.yml -f k8s.compose.yml {docker}".split(" ")
    )


def execute(docker: str) -> None:
    subprocess.run(f"docker compose {docker}".split(" "))
