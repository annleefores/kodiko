# import subprocess, os


import subprocess
from typing import Any, List


class KubeBase:
    def __init__(self) -> None:
        self.cmd: List[str]
        self.cmd_start: str

    def method_init(self, method_name: str):
        self.cmd = []
        self.cmd.append(self.cmd_start)
        self.cmd.append(method_name)

    def ns(self, ns: str):
        if ns != "":
            self.cmd += ["-n", ns]

    def obj(self, obj: str, obj_name: str):
        self.cmd += [obj, obj_name]

    def file(self, file_path: str):
        self.cmd += ["-f", file_path]

    def patch_file(self, patch_file: str):
        self.cmd += ["--patch-file", patch_file]

    def patch_merge_stategy(self):
        self.cmd += ["--type", "merge"]


class KubeCMD(KubeBase):
    def __init__(self, cmd: str = "kubectl") -> None:
        self.cmd_start = cmd

    @classmethod
    def helm(cls):
        return cls("helm")

    def create(self, obj: str, obj_name: str) -> None:
        """
        create for kubectk
        """

        self.method_init("create")
        self.obj(obj, obj_name)
        subprocess.run(self.cmd)

    def apply(self, file_path: str, namespace: str = "") -> None:
        """
        apply for kubectl
        """
        self.method_init("apply")
        self.ns(namespace)
        self.file(file_path)
        subprocess.run(self.cmd)

    def delete(
        self,
        file_path: str = "",
        obj: str = "",
        obj_name: str = "",
        namespace: str = "",
    ) -> None:
        """
        delete for kubectl
        """
        self.method_init("delete")

        self.ns(namespace)

        if file_path != "":
            self.file(file_path)
        else:
            self.obj(obj=obj, obj_name=obj_name)

        subprocess.run(self.cmd)

    def patch(
        self,
        obj: str,
        obj_name: str,
        patch_file: str,
        namespace: str = "",
        strategy: Any = None,
    ) -> None:
        """
        patch for kubectl
        """
        self.method_init("patch")
        self.ns(namespace)
        self.obj(obj=obj, obj_name=obj_name)
        if strategy:
            self.patch_merge_stategy()
        self.patch_file(patch_file=patch_file)
        subprocess.run(self.cmd)