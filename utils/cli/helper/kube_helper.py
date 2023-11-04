import subprocess
from typing import Dict, List


class Base:
    def __init__(self) -> None:
        self.cmd: List[str]
        self.cmd_start: str

    def method_init(self, method_name: str):
        self.cmd = []
        self.cmd.append(self.cmd_start)
        self.cmd.append(method_name)

    def ns(self, ns: str | None = None):
        if ns:
            self.cmd += ["-n", ns]


class KubeArgs(Base):
    def obj(self, obj: str, obj_name: str, type: str | None = None):
        objList = [obj, obj_name]

        if type:
            objList.insert(1, type)

        self.cmd += objList

    def file(
        self,
        file_path: str,
        option: str | None = None,
    ):
        """
        option: \n
        Default => -f \n
        p => --patch-file

        """
        match option:
            case "p":
                opt_val = "--patch-file"
            case _:
                opt_val = "-f"

        self.cmd += [opt_val, file_path]

    def patch_merge_stategy(self, strategy: str):
        """
        strategy: \n
        Default => merge \n
        """
        match strategy:
            case _:
                strategy_type = "merge"

        self.cmd += ["--type", strategy_type]

    def from_literal(self, from_literal: Dict[str, str]):
        for key, val in from_literal.items():
            self.cmd.append(f"--from-literal={key}={val}")


class KubeCMD(KubeArgs):
    def __init__(self, cmd: str = "kubectl") -> None:
        self.cmd_start = cmd

    def create(
        self,
        obj: str,
        obj_name: str,
        type: str | None = None,
        ns: str | None = None,
        from_literal: Dict[str, str] = {},
    ) -> None:
        """
        create for kubectl
        """

        self.method_init("create")
        self.obj(obj=obj, type=type, obj_name=obj_name)
        self.from_literal(from_literal=from_literal)
        self.ns(ns=ns)
        subprocess.run(self.cmd)

    def apply(self, file_path: str, ns: str | None = None) -> None:
        """
        apply for kubectl
        """
        self.method_init("apply")
        self.ns(ns)
        self.file(file_path)
        subprocess.run(self.cmd)

    def delete(
        self,
        file_path: str | None = None,
        obj: str = "",
        obj_name: str = "",
        ns: str | None = None,
    ) -> None:
        """
        delete for kubectl
        """
        self.method_init("delete")

        self.ns(ns)

        if file_path:
            self.file(file_path)
        else:
            self.obj(obj=obj, obj_name=obj_name)

        subprocess.run(self.cmd)

    def patch(
        self,
        obj: str,
        obj_name: str,
        patch_file: str,
        ns: str | None = None,
        strategy: str | None = None,
    ) -> None:
        """
        patch for kubectl
        """
        self.method_init("patch")
        self.ns(ns)
        self.obj(obj=obj, obj_name=obj_name)
        if strategy:
            self.patch_merge_stategy(strategy)
        self.file(option="p", file_path=patch_file)
        subprocess.run(self.cmd)


class HelmArgs(Base):
    def release_name(self, release_name: str):
        self.cmd.append(release_name)

    def values(self, valueFile: str | None = None):
        if valueFile:
            self.cmd += ["--values", valueFile]

    def setVal(self, keyVal: Dict[str, str]):
        for key, val in keyVal.items():
            self.cmd += ["--set", f"{key}={val}"]


class HelmCMD(HelmArgs):
    def __init__(self, cmd: str = "helm") -> None:
        self.cmd_start = cmd

    def install(
        self,
        release_name: str,
        HelmPath: str,
        dev: str,
        valFile: str | None = None,
        ns: str | None = None,
    ) -> None:
        """
        install for helm
        """

        self.method_init("install")
        self.release_name(release_name)
        self.ns(ns)
        self.values(valFile)
        self.setVal({"dev": dev})
        self.cmd.append(f"./{HelmPath}")
        subprocess.run(self.cmd)

    def uninstall(self, release_name: str, ns: str | None = None) -> None:
        """
        uninstall for helm
        """

        self.method_init("uninstall")
        self.release_name(release_name)
        self.ns(ns)
        subprocess.run(self.cmd)
