# /usr/bin/python3

from typing import Annotated
import typer
import os
from helper.helper import execute, execute_kube, execute_build_push
from helper.kube_helper import KubeCMD


app = typer.Typer(
    add_completion=False, no_args_is_help=True, pretty_exceptions_enable=False
)

# set application home path
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


@app.command()
def install_argocd(
    local: Annotated[bool, typer.Option(help="Patch SVC type for local argocd")] = False
) -> None:
    """
    Install ArgoCD
    """
    k = KubeCMD()
    k.create("ns", "argocd")
    k.apply(
        "https://raw.githubusercontent.com/argoproj/argo-cd/v2.8.4/manifests/install.yaml",
        "argocd",
    )
    k.patch(
        obj="cm",
        obj_name="argocd-cm",
        patch_file="kubernetes/argocd/argocd_cm_patch.yaml",
        namespace="argocd",
    )

    if local:
        k.patch(
            obj="svc",
            obj_name="argocd-server",
            patch_file="kubernetes/argocd/argocd_svc_patch.yaml",
            namespace="argocd",
            strategy="merge",
        )
        k.patch(
            obj="cm",
            obj_name="argocd-cmd-params-cm",
            patch_file="kubernetes/argocd/argocd_cmd_cm_patch.yaml",
            namespace="argocd",
        )


@app.command()
def uninstall_argocd() -> None:
    """
    Uninstall ArgoCD
    """
    k = KubeCMD()
    k.delete(
        file_path="https://raw.githubusercontent.com/argoproj/argo-cd/v2.8.4/manifests/install.yaml",
        namespace="argocd",
    )

    k.delete(obj="ns", obj_name="argocd")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Manage dx related commands for Kodiko application development
    """
    if ctx.invoked_subcommand is None:
        print("Initializing Kodiko CLI")


if __name__ == "__main__":
    app()
