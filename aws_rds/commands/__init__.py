import click

from .servers import servers


@click.group()
def aws_rds():
    """Generate IAM tokens for RDS instances with awscli and aws-okta."""
    pass


aws_rds.add_command(servers)
