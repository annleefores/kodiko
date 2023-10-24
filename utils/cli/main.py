# /usr/bin/python3

from typing import Annotated
import typer
import os
from helper.helper import execute, execute_kube, execute_build_push


app = typer.Typer(
    add_completion=False, no_args_is_help=True, pretty_exceptions_enable=False
)

path = os.path.abspath(os.path.join(__file__, "../../../"))
os.chdir(path)


@app.command()
def up(
    local: Annotated[
        bool, typer.Option(help="Create local version of docker-compose")
    ] = False
) -> None:
    """
    Start docker compose and K8s applications
    """
    if local:
        execute("up --build")
    else:
        execute_kube("up --build", "install")


@app.command()
def down(
    local: Annotated[
        bool, typer.Option(help="Destroy local version of docker-compose")
    ] = False
) -> None:
    """
    Stop docker compose and K8s applications
    """
    if local:
        execute("down")
    else:
        execute_kube("down", "uninstall")


@app.command()
def push_cp() -> None:
    """
    Build and Push codepod build and deploy base images
    """
    os.chdir("utils/docker/codepod")
    # build and push codepod-build image
    execute_build_push("build")

    # build and push codepod-deploy image
    execute_build_push("deploy")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Manage dx related commands for Kodiko application development
    """
    if ctx.invoked_subcommand is None:
        print("Initializing database")


if __name__ == "__main__":
    app()
