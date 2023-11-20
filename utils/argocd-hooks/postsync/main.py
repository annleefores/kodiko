from ast import Tuple
from typing import Dict
import requests
from dotenv import load_dotenv
import os

load_dotenv()


class SonarPostHook:
    def __init__(
        self,
        jenkins_sonar_webhook: str,
        sonarqube_url: str,
        name: str,
    ) -> None:
        self.token = ""
        self.jenkins_sonar_webhook = jenkins_sonar_webhook
        self.name = name
        self.sonarqube_url = sonarqube_url
        self.sonarqube_auth = (
            os.getenv("SONAR_USERNAME"),
            os.getenv("SONAR_PASSWORD"),
        )

    def req(
        self,
        url: str,
        http_method: str = "post",
        data: Dict[str, str] | None = None,
        auth: Tuple | None = None,
    ):
        try:
            req = getattr(requests, http_method)
            return req(url=url, data=data, auth=auth if auth else self.sonarqube_auth)
        except requests.exceptions.RequestException as err:
            print("RequestException Else:", err)

    def update_sonar_password(self):
        url = f"{self.sonarqube_url}/api/users/change_password"
        data = {
            "login": "admin",
            "password": self.sonarqube_auth[1],
            "previousPassword": "admin",
        }

        try:
            resp = self.req(url=url, data=data, auth=("admin", "admin"))
            if resp.status_code == 204:
                print("Password changed!")
            elif resp.status_code == 401:
                print("Password already changed!")
        except requests.exceptions.RequestException as e:
            print("RequestException", e)

    def get_sonar_token(self):
        url = f"{self.sonarqube_url}/api/user_tokens/generate"
        data = {"name": self.name}
        resp = self.req(url=url, data=data).json()
        if "errors" in resp:
            print(resp["errors"][0]["msg"])
        else:
            print("Token created!")
            return resp.get("token")

    def check_sonar_webhook(self) -> bool:
        """
        returns true if the url webhook does not exist
        """
        url = f"{self.sonarqube_url}/api/webhooks/list"
        webhooks = self.req(url=url, http_method="get").json()
        if webhooks:
            for i in webhooks.get("webhooks"):
                if i.get("url") == self.jenkins_sonar_webhook:
                    return False
        return True

    def create_sonar_webhook(self) -> None:
        # check if there's already a webhook for the same url
        if self.check_sonar_webhook():
            # if not create a new webhook
            url = f"{self.sonarqube_url}/api/webhooks/create"
            data = {"name": self.name, "url": self.jenkins_sonar_webhook}
            print("Webhook created!")
            print(self.req(url=url, data=data).json())
        else:
            print("Webhook already exists!")


if __name__ == "__main__":
    hook = SonarPostHook(
        jenkins_sonar_webhook=os.getenv(
            "JENKINS_SONAR_WEBHOOK",
            "http://jenkins.jenkins.svc.cluster.local:8080/sonarqube-webhook",
        ),
        name=os.getenv("NAME", "jenkins"),
        sonarqube_url=os.getenv(
            "SONAR_URL", "http://sonarqube-sonarqube.sonarqube.svc.cluster.local:9000"
        ),
    )
    hook.update_sonar_password()
    hook.get_sonar_token()
    hook.create_sonar_webhook()
