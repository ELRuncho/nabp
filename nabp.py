import click

@click.group()
def cli():
    click.echo("nabp")


@cli.command()
@click.option('--string', default='World')
def core():
    click.echo('command core')