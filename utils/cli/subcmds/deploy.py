import typer
from helper.kube_helper import HelmCMD, KubeCMD
from helper.boto3_helper import get_eks_vpc, SSM
from typing import Annotated, List

deploy = typer.Typer()


@deploy.command()
def argocd(
    local: Annotated[bool, typer.Option(help="Patch SVC for local argocd")] = False
) -> None:
    """
    Deploy ArgoCD
    """
    k = KubeCMD()
    h = HelmCMD()
    k.create(obj="ns", obj_name="argocd")

    if local:
        h.install(
            release_name="argocd",
            repo="argo/argo-cd",
            valFile="kubernetes/argocd/dev-values.yaml",
            ns="argocd",
            ChartVersion="5.51.4",
        )
    else:
        h.install(
            release_name="argocd",
            repo="argo/argo-cd",
            valFile="kubernetes/argocd/values.yaml",
            ns="argocd",
            ChartVersion="5.51.4",
        )


@deploy.command()
def config(
    local: Annotated[
        bool, typer.Option(help="Install system config for local cluster")
    ] = False
) -> None:
    """
    Deploy System Config
    """
    h = HelmCMD()
    ssm = SSM()

    keyVal = {}
    if not local:
        print("Adding EKS VPC ID")
        keyVal["vpcID"] = get_eks_vpc()
    h.install(
        release_name="system-config-main",
        HelmPath="kubernetes/system-config/main",
        ns="argocd",
        dev="true" if local else "false",
        keyVal=keyVal,
    )
    # deploy AWS creds secret for ESO

    if local:
        print("Creating AWS credentials secret")
        k = KubeCMD()

        cred: List[str] = ssm.getAK()
        aws_key, aws_secret = cred[0], cred[1]
        k.create(
            ns="external-secrets",
            obj="secret",
            type="generic",
            obj_name="awssm-secret",
            from_literal={"access-key": aws_key, "secret-access-key": aws_secret},
        )


@deploy.command()
def app(
    local: Annotated[
        bool, typer.Option(help="Install application for local cluster")
    ] = False
) -> None:
    """
    Deploy Application
    """
    # Launch ngrok tunnel for argocd
    if local:
        print("creating ngrok tunnel")

    h = HelmCMD()
    h.install(
        release_name="backend",
        HelmPath="kubernetes/application/main",
        ns="argocd",
        dev="true" if local else "false",
    )


if __name__ == "__main__":
    deploy()
