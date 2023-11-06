import subprocess
from typing import List


class Base:
    def __init__(self) -> None:
        self.cmd: List[str]
        self.cmd_start: str

    def method_init(self, method_name: str):
        self.cmd = []
        self.cmd.append(self.cmd_start)
        self.cmd.append(method_name)

    def file(
        self,
        file_path: str,
    ):
        self.cmd += ["-f", f"./{file_path}"]

    def complete_image_name(self, username: str, container_name: str, version: str):
        self.cmd.append(f"{username}/{container_name}:{version}")

    def tag(self, username: str, container_name: str, version: str):
        self.cmd.append("-t")
        self.complete_image_name(
            username=username, container_name=container_name, version=version
        )

    def build_file_context(self, filePath: str):
        """
        build file context should be relative to root path
        """
        self.cmd.append(f"./{filePath}")


class DockerCMD(Base):
    def __init__(self, cmd: str = "docker") -> None:
        self.cmd_start = cmd

    def build(
        self,
        container_name: str,
        dockerfile_path: str,
        username: str,
        version: str,
        build_file_path: str | None = None,
    ):
        """
        Build for docker
        """
        self.method_init(method_name="build")
        self.file(file_path=dockerfile_path)
        self.tag(username=username, container_name=container_name, version=version)
        if build_file_path:
            self.build_file_context(build_file_path)
        subprocess.run(self.cmd)

    def compose(self, func: str = "up", compose_file_path: List[str] | None = None):
        """
        func: up or down
        """
        self.method_init(method_name="compose")
        if compose_file_path:
            for val in compose_file_path:
                self.file(file_path=val)
        self.cmd.append(func)
        subprocess.run(self.cmd)

    def push(self, container_name: str, username: str, version: str):
        """
        Push for docker
        """
        self.method_init(method_name="push")
        self.complete_image_name(
            username=username, container_name=container_name, version=version
        )
        subprocess.run(self.cmd)

    def run(self):
        pass
