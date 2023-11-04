# /usr/bin/python3

from typing import Annotated
import typer
import os
from helper.helper import execute, execute_kube, execute_build_push
from helper.kube_helper import HelmCMD, KubeCMD
from helper.boto3_helper import createAK, deleteAK


app = typer.Typer(
    add_completion=False, no_args_is_help=True, pretty_exceptions_enable=False
)

# set application home path
# all path should be relative to home path
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
def deploy_argocd(
    local: Annotated[bool, typer.Option(help="Patch SVC type for local argocd")] = False
) -> None:
    """
    Install ArgoCD
    """
    k = KubeCMD()
    k.create(obj="ns", obj_name="argocd")
    k.apply(
        file_path="https://raw.githubusercontent.com/argoproj/argo-cd/v2.8.4/manifests/install.yaml",
        namespace="argocd",
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
def delete_argocd() -> None:
    """
    Uninstall ArgoCD
    """
    k = KubeCMD()
    k.delete(
        file_path="https://raw.githubusercontent.com/argoproj/argo-cd/v2.8.4/manifests/install.yaml",
        ns="argocd",
    )

    k.delete(obj="ns", obj_name="argocd")


@app.command()
def deploy_config(
    local: Annotated[
        bool, typer.Option(help="Install system config for local cluster")
    ] = False
) -> None:
    """
    Install System Config
    """
    h = HelmCMD()
    h.install(
        release_name="system-config-main",
        HelmPath="kubernetes/system-config/system-config-main",
        ns="argocd",
        dev="true" if local else "false",
    )


@app.command()
def delete_config(
    local: Annotated[
        bool, typer.Option(help="Install system config for local cluster")
    ] = False
) -> None:
    """
    Uninstall System Config
    """
    h = HelmCMD()
    h.uninstall(release_name="system-config-main", ns="argocd")


@app.command()
def deploy_app(
    local: Annotated[
        bool, typer.Option(help="Install system config for local cluster")
    ] = False
) -> None:
    """
    Deploy application
    """
    # deploy AWS creds secret for ESO
    if local:
        print("Creating AWS credentials")
        k = KubeCMD()
        cred = createAK()
        aws_key, aws_secret = cred.get("AccessKeyId"), cred.get("SecretAccessKey")
        k.create(
            ns="kodiko-backend",
            obj="secret",
            type="generic",
            obj_name="awssm-secret",
            from_literal={"access-key": aws_key, "secret-access-key": aws_secret},
        )

    h = HelmCMD()
    h.install(
        release_name="backend",
        HelmPath="kubernetes/application/application-main",
        ns="argocd",
        dev="true" if local else "false",
    )


@app.command()
def delete_app(
    local: Annotated[
        bool, typer.Option(help="Install system config for local cluster")
    ] = False
) -> None:
    """
    Delete application
    """
    h = HelmCMD()
    h.uninstall(release_name="backend", ns="argocd")

    # delete AWS creds secret for ESO
    if local:
        print("Deleting AWS credentials")
        k = KubeCMD()
        cred = deleteAK()
        k.delete(
            obj="secret",
            obj_name="awssm-secret",
            ns="kodiko-backend",
        )


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Manage dx related commands for Kodiko application development
    """
    if ctx.invoked_subcommand is None:
        print("Initializing Kodiko CLI")


if __name__ == "__main__":
    app()
