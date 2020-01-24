import click

from ..servers import ServerList


@click.group()
def servers():
    """Manage the saved server list."""
    pass


@servers.command()
def list():
    """List saved servers."""
    server_list = ServerList.load()
    print(server_list.json())
