import sys
from enum import Enum

import click

from ..servers import Server, ServerList, ServerRegion


@click.group()
def servers():
    """Manage the saved server list."""
    pass


@servers.command()
@click.option(
    "--name", prompt=True, help="Alias used to refer to the server in all commands."
)
@click.option("--hostname", prompt=True, help="Hostname of the RDS instance to add.")
@click.option(
    "--port", prompt=True, default=5432, help="Port of the RDS instance to add."
)
@click.option(
    "--region",
    prompt=True,
    help="Region the RDS instance to add is located in.",
    type=click.Choice([i.replace("_", "-") for i in ServerRegion.__members__]),
    callback=lambda c, p, v: getattr(ServerRegion, v.replace("-", "_")) if v else None,
)
@click.option(
    "--username", prompt=True, help="Username to use to connect to the RDS instance."
)
@click.option(
    "--profile",
    prompt=True,
    help="Okta profile to use to generate a token for the RDS instance.",
)
def add(name, hostname, port, region, username, profile):
    """Add a new server to the server list."""
    server_list = ServerList.load()
    for server in server_list.servers:
        if server.name == name:
            click.secho(f"A server with the name {name} already exists.", fg="red")
            sys.exit(1)
    server_list.servers.append(
        Server(
            name=name,
            hostname=hostname,
            port=port,
            region=region,
            username=username,
            profile=profile,
        )
    )
    server_list.save()
    click.secho(f"Server {name} added to server list.", fg="green")


@servers.command()
@click.argument("server_name")
def remove(server_name):
    """Remove a server from the server list."""
    server_list = ServerList.load()

    server = next((s for s in server_list.servers if s.name == server_name), None)

    if not server:
        click.secho(f"No server with the name {server_name} exists.", fg="red")
        sys.exit(1)

    server_list.servers.remove(server)
    server_list.save()

    click.secho(f"Server {server_name} removed from server list.", fg="green")


@servers.command()
def list():
    """List saved servers."""
    server_list = ServerList.load()
    for server in server_list.servers:
        click.echo(server.format())
