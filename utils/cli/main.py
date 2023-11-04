# /usr/bin/python3

import typer
import os

import subcmds.deploy as deploy
import subcmds.delete as delete
import subcmds.push as push
import subcmds.local as local

app = typer.Typer(
    add_completion=False, no_args_is_help=True, pretty_exceptions_enable=False
)


app.add_typer(deploy.deploy, name="deploy", help="Deploy subcommand items")
app.add_typer(delete.delete, name="delete", help="Delete subcommand items")
app.add_typer(push.push, name="push", help="Push docker images")
app.add_typer(local.local, name="local", help="Up and down local dev env")

# set application home path
# all path should be relative to home path
path = os.path.abspath(os.path.join(__file__, "../../../"))
os.chdir(path)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Manage dx related commands for Kodiko application development
    """
    if ctx.invoked_subcommand is None:
        print("Initializing Kodiko CLI")


if __name__ == "__main__":
    app()
