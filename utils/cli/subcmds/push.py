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
