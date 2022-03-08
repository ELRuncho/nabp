from email.policy import default
import click

@click.group()
def cli():
    click.echo("nabp")


@cli.group('core')
def core():
    """comandos seguridad core"""
    

@core.command('desplegar')
@click.option('--tag', default=None, help="agregar tag a recursos desplegados")
def coresec(tag):
    "desplegar medidas core"
    click.echo("testing de comando desplegar")
