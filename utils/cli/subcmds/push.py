import typer
from helper.docker_helper import DockerCMD

push = typer.Typer()


@push.command()
def codepod_base() -> None:
    """
    Build and Push codepod build and deploy base images
    """
    d = DockerCMD()

    username = "annleefores"
    version = "1.0.0"
    basePath = "utils/docker/codepod"

    d.build(
        dockerfile_path=f"{basePath}/build.Dockerfile",
        container_name="codepod-build",
        username=username,
        version=version,
    )
    d.push(
        container_name="codepod-build",
        username=username,
        version=version,
    )

    d.build(
        dockerfile_path=f"{basePath}//deploy.Dockerfile",
        container_name="codepod-deploy",
        username=username,
        version=version,
        build_file_path="server/codepod/",
    )
    d.push(
        container_name="codepod-deploy",
        username=username,
        version=version,
    )


@push.command()
def codepod() -> None:
    """
    Build and Push codepod images
    """
    d = DockerCMD()

    username = "annleefores"
    version = "1.0.0"
    basePath = "server/codepod"

    d.build(
        dockerfile_path=f"{basePath}/Dockerfile",
        container_name="codepod-prod",
        username=username,
        version=version,
        build_file_path=basePath,
    )
    d.push(
        container_name="codepod-prod",
        username=username,
        version=version,
    )


@push.command()
def backend() -> None:
    """
    Build and Push backend images
    """
    d = DockerCMD()

    username = "annleefores"
    version = "1.0.0"
    basePath = "server/backend"

    d.build(
        dockerfile_path=f"{basePath}/Dockerfile",
        container_name="backend",
        username=username,
        version=version,
        build_file_path=basePath,
    )
    d.push(
        container_name="backend",
        username=username,
        version=version,
    )
