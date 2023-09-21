# /usr/bin/python3

import typer
import os
import subprocess


app = typer.Typer(
    add_completion=False, no_args_is_help=True, pretty_exceptions_enable=False
)

path = os.path.abspath(os.path.join(__file__, "../../../"))
os.chdir(path)


def execute(docker: str, k8s: str):
    subprocess.run(
        f"docker compose -f compose.yml -f k8s.compose.yml {docker}".split(" ")
    )
    os.chdir("k8s/codepod")
    subprocess.run(f"kubectl {k8s} -f ./".split(" "))


@app.command()
def up() -> None:
    """
    Start docker compose and K8s applications
    """
    execute("up -d", "apply")


@app.command()
def down() -> None:
    """
    Stop docker compose and K8s applications
    """
    execute("down", "delete")


@app.command("push-cp")
def build_push_codepod() -> None:
    """
    Build and Push codepod build and deploy base images
    """
    os.chdir("scripts/docker/codepod")
    # build and push codepod-build image
    subprocess.run(
        "docker build -f build.Dockerfile -t annleefores/codepod-build:1.0.0 .".split(
            " "
        )
    )
    subprocess.run("docker push annleefores/codepod-build:1.0.0".split(" "))

    # build and push codepod-deploy image
    subprocess.run(
        "docker build -f deploy.Dockerfile -t annleefores/codepod-deploy:1.0.0 .".split(
            " "
        )
    )
    subprocess.run("docker push annleefores/codepod-deploy:1.0.0".split(" "))


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Manage dx related commands for Kodiko application development
    """
    if ctx.invoked_subcommand is None:
        print("Initializing database")


if __name__ == "__main__":
    app()
