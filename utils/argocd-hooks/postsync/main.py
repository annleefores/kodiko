from ast import Tuple
from typing import Dict
import requests
from dotenv import load_dotenv
import os

load_dotenv()


class SonarPostHook:
    def __init__(
        self,
        jenkins_sonar_webhook: str = "http://jenkins.jenkins.svc.cluster.local:8080/sonarqube-webhook",
        sonarqube_url: str = "http://sonarqube-sonarqube.sonarqube.svc.cluster.local:9000",
        name: str = "jenkins",
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
        auth: Tuple | None = None,
        data: Dict[str, str] | None = None,
    ):
        try:
            req = getattr(requests, http_method)
            resp = req(url=url, data=data, auth=auth or self.sonarqube_auth)
            resp_dict = resp.json()
            if "errors" in resp_dict:
                print(resp_dict["errors"][0]["msg"])
                resp.raise_for_status()  # This will raise an HTTPError if the response was an HTTP error
            else:
                return resp_dict
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something Else:", err)

    def update_sonar_password(self):
        url = f"{self.sonarqube_url}/api/users/change_password"
        data = {
            "login": "admin",
            "password": self.sonarqube_auth[1],
            "previousPassword": "admin",
        }
        try:
            self.req(url=url, data=data, auth=("admin", "admin"))
        except Exception as e:
            print("Password already changed!", e)

    def get_sonar_token(self):
        url = f"{self.sonarqube_url}/api/user_tokens/generate"
        data = {"name": self.name}
        resp = self.req(url=url, data=data)
        if resp:
            print("Token created!")
            return resp.get("token")

    def check_sonar_webhook(self) -> bool:
        """
        returns true if the url webhook does not exist
        """
        url = f"{self.sonarqube_url}/api/webhooks/list"
        webhooks = self.req(url=url, http_method="get")
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
            print(self.req(url=url, data=data))
        else:
            print("Webhook already exists!")


if __name__ == "__main__":
    hook = SonarPostHook(
        jenkins_sonar_webhook=os.getenv("JENKINS_SONAR_WEBHOOK") or "",
        name=os.getenv("NAME") or "",
    )
    hook.update_sonar_password()
    hook.get_sonar_token()
    hook.create_sonar_webhook()
