from typing import List

import typer

from aptmarkreason.commands.install import install_packages

app = typer.Typer()


@app.command()
def install(
    reason: str = typer.Argument(
        ...,
        help='Short keyword or text describing installation reason. Should be enclosed in double quotes (") if it contains spaces.',
    ),
    packages: List[str] = typer.Argument(..., help="List of packages to install"),
):
    install_packages(app, reason, packages)


@app.command()
def uninstall(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


@app.command()
def list(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


if __name__ == "__main__":
    app()
