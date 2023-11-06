# Create local tunnel for argocd + GitHub webhook
import subprocess


def tunnel(on: bool = True):
    if on:
        command = "ngrok http --domain=pleasant-crab-champion.ngrok-free.app 8080"
        subprocess.Popen(
            command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
    else:
        subprocess.run("killall ngrok".split(" "))
