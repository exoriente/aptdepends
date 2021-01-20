import typer


def output_exception(error: Exception):
    typer.secho(f"Error: {error}", fg=typer.colors.RED)
