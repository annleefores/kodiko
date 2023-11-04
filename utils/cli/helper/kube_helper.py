# import subprocess, os


import subprocess
from typing import Any, Dict, List


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

    def obj(self, obj: str, obj_name: str, type: str = ""):
        if type != "":
            self.cmd += [obj, type, obj_name]
        else:
            self.cmd += [obj, obj_name]

    def file(self, file_path: str):
        self.cmd += ["-f", file_path]

    def patch_file(self, patch_file: str):
        self.cmd += ["--patch-file", patch_file]

    def patch_merge_stategy(self):
        self.cmd += ["--type", "merge"]

    def from_literal(self, key: str, val: str):
        self.cmd += [f"--from-literal={key}={val}"]


class HelmCMD(KubeBase):
    def __init__(self, cmd: str = "helm") -> None:
        self.cmd_start = cmd

    def release_name(self, release_name: str):
        self.cmd.append(release_name)

    def values(self, valueFile: str):
        if valueFile != "":
            self.cmd += ["--values", valueFile]

    def setVal(self, key: str, val: str):
        if val:
            self.cmd += ["--set", f"{key}={val}"]

    def install(
        self,
        release_name: str,
        HelmPath: str,
        dev: str,
        valFile: str = "",
        ns: str = "",
    ) -> None:
        """
        install for helm
        """

        self.method_init("install")
        self.release_name(release_name)
        self.ns(ns)
        self.values(valFile)
        self.setVal("dev", dev)
        self.cmd.append(f"./{HelmPath}")
        subprocess.run(self.cmd)

    def uninstall(self, release_name: str, ns: str = "") -> None:
        """
        uninstall for helm
        """

        self.method_init("uninstall")
        self.release_name(release_name)
        self.ns(ns)
        subprocess.run(self.cmd)


class KubeCMD(KubeBase):
    def __init__(self, cmd: str = "kubectl") -> None:
        self.cmd_start = cmd

    def create(
        self,
        obj: str,
        obj_name: str,
        type: str = "",
        ns: str = "",
        from_literal: Dict[str, str] = {},
    ) -> None:
        """
        create for kubectl
        """

        self.method_init("create")
        self.obj(obj=obj, type=type, obj_name=obj_name)
        for key, val in from_literal.items():
            self.from_literal(key=key, val=val)
        self.ns(ns=ns)
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
        ns: str = "",
    ) -> None:
        """
        delete for kubectl
        """
        self.method_init("delete")

        self.ns(ns)

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
