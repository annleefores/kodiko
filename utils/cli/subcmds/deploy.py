import typer
from helper.kube_helper import HelmCMD, KubeCMD
from helper.boto3_helper import get_eks_vpc, SSM
from typing import Annotated, List

from helper.ngrok_helper import tunnel

deploy = typer.Typer()


@deploy.command()
def argocd(
    local: Annotated[bool, typer.Option(help="Patch SVC for local argocd")] = False
) -> None:
    """
    Deploy ArgoCD
    """
    k = KubeCMD()
    k.create(obj="ns", obj_name="argocd")
    k.apply(
        file_path="https://raw.githubusercontent.com/argoproj/argo-cd/v2.8.4/manifests/install.yaml",
        ns="argocd",
    )
    k.patch(
        obj="cm",
        obj_name="argocd-cm",
        patch_file="kubernetes/argocd/argocd_cm_patch.yaml",
        ns="argocd",
    )

    if local:
        k.patch(
            obj="svc",
            obj_name="argocd-server",
            patch_file="kubernetes/argocd/argocd_svc_patch.yaml",
            ns="argocd",
            strategy="merge",
        )
        k.patch(
            obj="cm",
            obj_name="argocd-cmd-params-cm",
            patch_file="kubernetes/argocd/argocd_cmd_cm_patch.yaml",
            ns="argocd",
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
    # deploy AWS creds secret for ESO
    ssm = SSM()

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

    h = HelmCMD()
    print("Adding Jenkins Admin Password")
    keyVal = {"JenkinsAdminPassword": ssm.get_jenkins_passwd()}
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
        tunnel()

    h = HelmCMD()
    h.install(
        release_name="backend",
        HelmPath="kubernetes/application/main",
        ns="argocd",
        dev="true" if local else "false",
    )


if __name__ == "__main__":
    deploy()
