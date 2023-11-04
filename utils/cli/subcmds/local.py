import typer
from helper.docker_helper import DockerCMD
from subcmds.deploy import app as deploy_app
from subcmds.delete import app as delete_app


local = typer.Typer()


@local.command()
def up() -> None:
    """
    Start docker compose and K8s applications
    """
    d = DockerCMD()

    username = "annleefores"
    version = "1.0.0"

    d.build(
        dockerfile_path="server/codepod/Dockerfile",
        container_name="codepod",
        username=username,
        version=version,
        build_file_path="server/codepod/",
    )
    d.build(
        dockerfile_path="server/backend/Dockerfile",
        container_name="backend",
        username=username,
        version=version,
        build_file_path="server/backend/",
    )

    deploy_app(local=True)

    d.compose(func="up")


@local.command()
def down() -> None:
    """
    Stop docker compose and K8s applications
    """

    d = DockerCMD()
    d.compose(func="down")

    delete_app(local=True)
