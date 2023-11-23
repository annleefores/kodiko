import typer
from typing import Annotated
from helper.kube_helper import HelmCMD, KubeCMD

delete = typer.Typer()


@delete.command()
def argocd(
    local: Annotated[bool, typer.Option(help="Delete argocd for local cluster")] = False
) -> None:
    """
    Delete ArgoCD
    """
    k = KubeCMD()
    k.delete(
        file_path="https://raw.githubusercontent.com/argoproj/argo-cd/v2.8.4/manifests/install.yaml",
        ns="argocd",
    )

    k.delete(obj="ns", obj_name="argocd")


@delete.command()
def config(
    local: Annotated[
        bool, typer.Option(help="Delete system config for local cluster")
    ] = False
) -> None:
    """
    Delete System Config
    """
    h = HelmCMD()
    h.uninstall(release_name="system-config-main", ns="argocd")

    # delete AWS creds secret for ESO
    if local:
        print("Deleting AWS credentials secret")
        k = KubeCMD()
        k.delete(
            obj="secret",
            obj_name="awssm-secret",
            ns="external-secrets",
        )


@delete.command()
def app(
    local: Annotated[
        bool, typer.Option(help="Delete application for local cluster")
    ] = False
) -> None:
    """
    Delete Application
    """
    h = HelmCMD()
    h.uninstall(release_name="backend", ns="argocd")


if __name__ == "__main__":
    delete()
