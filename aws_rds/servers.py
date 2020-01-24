import json
import pathlib
from typing import List

import click
from pydantic import BaseModel


class Server(BaseModel):
    name: str
    profile: str
    hostname: str
    port: int
    region: str
    username: str

    def format(self) -> str:
        return "\n".join(
            [
                click.style(self.name, fg="blue"),
                f"    {click.style('Profile:', fg='yellow')} {self.profile}",
                f"    {click.style('Hostname:', fg='yellow')} {self.hostname}",
                f"    {click.style('Port:', fg='yellow')} {self.port}",
                f"    {click.style('Region:', fg='yellow')} {self.region}",
                f"    {click.style('Username:', fg='yellow')} {self.username}",
            ]
        )


class ServerList(BaseModel):
    servers: List[Server]

    @classmethod
    def load(cls) -> "ServerList":
        app_dir = pathlib.Path(click.get_app_dir("aws-rds"))
        list_path = pathlib.Path(app_dir, "servers.json")

        if not list_path.is_file():
            server_list = cls(servers=[])
            server_list.save()
            click.secho(
                f"No server list was found. An empty one has been created at {list_path}.",
                fg="yellow",
            )
            return server_list
        else:
            with open(list_path, "r") as f:
                return cls(**json.load(f))

    def save(self) -> None:
        app_dir = pathlib.Path(click.get_app_dir("aws-rds"))
        app_dir.mkdir(parents=True, exist_ok=True)
        list_path = pathlib.Path(app_dir, "servers.json")
        with open(list_path, "w") as f:
            f.write(self.json())
