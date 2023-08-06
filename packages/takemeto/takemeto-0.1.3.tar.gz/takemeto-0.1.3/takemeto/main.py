import typer
import json

from .local_storage import LocalStorage

app = typer.Typer()


@app.command()
def add(name, destination, ctx: typer.Context):
    storage = ctx.obj["storage"]
    destinations = storage.destinations
    destinations[name] = destination
    storage.write(json.dumps(destinations))
    typer.secho(f"Added destination with name: {name}", fg="green")


@app.command()
def remove(name, ctx: typer.Context):
    storage = ctx.obj["storage"]
    destinations = storage.destinations
    try:
        del destinations[name]
        storage.write(json.dumps(destinations))
        typer.secho(f"Removed destination with name: {name}", fg="green")
    except KeyError:
        typer.secho(f"No destination found with name: {name}", fg="red")


@app.command()
def list_all(ctx: typer.Context):
    storage = ctx.obj["storage"]
    for name, destination in storage.destinations.items():
        typer.echo(f"{name}: {destination}")


@app.command()
def update(name, destination, ctx: typer.Context):
    storage = ctx.obj["storage"]
    destinations = storage.destinations
    if destinations.get(name, False):
        destinations[name] = destination
        storage.write(json.dumps(destinations))
        typer.secho(f"Updated destination with name: {name}", fg="green")
    else:
        typer.secho(f"No destination found with name: {name}.", fg="red")


@app.command()
def dest(name, ctx: typer.Context):
    storage = ctx.obj["storage"]
    destinations = storage.destinations
    if destinations.get(name, False):
        typer.secho(f"Taking you to {destinations[name]}. 🚀")
        typer.launch(destinations[name])
    else:
        typer.secho(f"No destination found with name: {name}", fg="red")


@app.callback()
def main(ctx: typer.Context):
    ctx.obj = {
        "storage": LocalStorage()
    }
