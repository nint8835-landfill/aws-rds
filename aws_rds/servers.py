import json
import pathlib
from enum import Enum
from typing import List

import click
from pydantic import BaseModel


class ServerRegion(Enum):
    us_east_1 = "us-east-1"
    us_east_2 = "us-east-2"
    us_west_1 = "us-west-1"
    us_west_2 = "us-west-2"
    ap_east_1 = "ap-east-1"
    ap_south_1 = "ap-south-1"
    ap_northeast_1 = "ap-northeast-1"
    ap_northeast_2 = "ap-northeast-2"
    ap_northeast_3 = "ap-northeast-3"
    ap_southeast_1 = "ap-southeast-1"
    ap_southeast_2 = "ap-southeast-2"
    ca_central_1 = "ca-central-1"
    eu_west_1 = "eu-west-1"
    eu_west_2 = "eu-west-2"
    eu_west_3 = "eu-west-3"
    eu_north_1 = "eu-north-1"
    me_south_1 = "me-south-1"
    sa_east_1 = "sa-east-1"


class Server(BaseModel):
    name: str
    profile: str
    hostname: str
    port: int
    region: ServerRegion
    username: str

    def format(self) -> str:
        return "\n".join(
            [
                click.style(self.name, fg="blue"),
                f"    {click.style('Profile:', fg='yellow')} {self.profile}",
                f"    {click.style('Hostname:', fg='yellow')} {self.hostname}",
                f"    {click.style('Port:', fg='yellow')} {self.port}",
                f"    {click.style('Region:', fg='yellow')} {self.region.value}",
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
