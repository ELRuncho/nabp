import email
from email.policy import default
import click
import boto3

class Config(object):
    def __init__(self):
        self.profile = 'default'
        self.session = boto3.Session(profile_name=self.profile)


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--profile', help='perfil preferido de awscli')
@pass_config
def cli(config,profile):
    if profile is None:
        profile='default'
    config.profile = profile
    click.echo("nabp ")

@cli.group('core')
@pass_config
def core(config):
    """comandos seguridad core"""
    

@core.command('seguridad')
@click.option('--tag', default=None, help="agregar tag a recursos desplegados")
@pass_config
def coresec(config,tag):
    "desplegar medidas de seguridad core"
    sess = config.session
    
    analyzerclient = sess.client('accessanalyzer')
    
    click.echo('creado bucket')


@core.command('presupuesto')
@click.option('--id', default=None, help="id de la cuenta de aws")
@click.option('--nombre', default=None, help='mnombre del presupuesto a crear')
@click.option('--monto', default=None, help='monto, en USD, del presupuesto a crear')
@click.option('--email', default=None, help='email para enviar notificaciones relacionadas con el presupuesto')
@pass_config
def presupuesto(config, id, nombre,monto, email):
    "establece presupuesto y alertas"
    sess = config.session
    budget=sess.client("budgets")

    click.echo(" creando budget y alerta asociada")
    #monto debe ser string
    budget.create_budget(   
                            AccountId=id,
                            Budget={
                                'BudgetName': nombre,
                                'BudgetLimit': {
                                    'Amount': monto,
                                    'Unit':'USD'
                                },
                                'TimeUnit': 'MONTHLY',
                                'BudgetType': 'COST'
                            }
                        )

    click.echo("budget creado")

    budget.create_notification(
                                AccountId=id,
                                BudgetName= nombre,
                                Notification= {
                                        'NotificationType': 'ACTUAL',
                                        'ComparisonOperator': 'GRATHER_THAN',
                                        'Treshold': 60,
                                        'TresholdType': 'PERCENTAGE',
                                        'NotificationState': 'ALARM' 
                                    },
                                Subscribers=[
                                                {
                                                    'SubscriptionType': 'EMAIL',
                                                    'Address': item
                                                }
                                    ]
                              )

    click.echo("notificacion creadas")

    #for item in email:
    #    budget.create_subscriber(
    #                                AccountId= id,
    #                                BudgetName= nombre,
    #                                Notification= {
    #                                    'NotificationType': 'ACTUAL',
    #                                    'ComparisonOperator': 'GRATHER_THAN',
    #                                    'Treshold': 60,
    #                                    'TresholdType': 'PERCENTAGE',
    #                                    'NotificationState': 'ALARM' 
    #                                },
    #                                Subscriber={
    #                                    'SubscriptionType': 'EMAIL',
    #                                    'Address': item
    #                                }
    #                            )

    click.echo("subscriptores a notificacion agregados")

    