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
@click.option('--nombre', default='miAnalyzer', help="nombre del analyzer")
@pass_config
def coresec(config, nombre):
    "desplegar medidas de seguridad core"
    sess = config.session
    
    analyzerclient = sess.client('accessanalyzer')

    click.echo('creando analyzer')
    analyzerclient.create_analyzer(
                                    analyzerName= nombre,
                                    type= 'ACCOUNT'
                                )
                
    click.echo('creado analyzer')


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
                                        'ComparisonOperator': 'GREATER_THAN',
                                        'Threshold': 60,
                                        'ThresholdType': 'PERCENTAGE',
                                        'NotificationState': 'ALARM' 
                                    },
                                Subscribers=[
                                                {
                                                    'SubscriptionType': 'EMAIL',
                                                    'Address': email
                                                }
                                    ]
                              )

    budget.create_notification(
                                AccountId= id,
                                BudgetName= nombre,
                                Notification= {
                                        'NotificationType': 'ACTUAL',
                                        'ComparisonOperator': 'EQUAL_TO',
                                        'Threshold': 90,
                                        'ThresholdType': 'PERCENTAGE',
                                        'NotificationState': 'ALARM' 
                                    },
                                Subscribers= [
                                    {
                                        'SubscriptionType': 'EMAIL',
                                        'Address': email
                                    }
                                ]
                            )

    click.echo("notificaciones creadas")
    click.echo("subscriptores a notificacion agregados")


@cli.group('network')
@pass_config
def network(config):
    """Comandos networking"""


@network.command('crear')
@click.option('--rango', default= '10.0.0.0/16', help= 'rango ipv4 para la vpc')
@click.option('--region', default='use-east-1', help='Region sobre la que se desplegara la VPC')
@pass_config
def crear(config, rango, region):
    "crea VPC con CIDR /16 y subnets con rango /24"
    sess= config.session
    _ec2 = sess.client('ec2')

    vpc = _ec2.create_vpc(
        CidrBlock=rango,
        TagSpecifications = [
            {
                'ResourceType': 'vpc',
                'Tags': [
                        {
                            'Key':'Name',
                            'Value':'NABPVPC'
                        },
                        {
                            'Key':'Project',
                            'Value':'NetworkBase'
                        },
                    ]
            },
        ]
    )

    
    click.echo("Creada VPC " + vpc['Vpc']['VpcId'])

    igw= _ec2.create_internet_gateway(
                                        TagSpecifications= [
                                            {
                                                'ResourceType': 'internet-gateway',
                                                'Tags': [
                                                    {
                                                        'Key':'Name',
                                                        'Value':'NABPIGW'
                                                    },
                                                ]
                                            },
                                        ]
                                    )

    _ec2.attach_internet_gateway(   
                                    VpcId= vpc['Vpc']['VpcId'],
                                    InternetGatewayId= igw['InternetGateway']['InternetGatewayId']
                                )

    click.echo('credo gateway '+ igw['InternetGateway']['InternetGatewayId'] + 'y asignado a VPC '+ vpc['Vpc']['VpcId'])

    publicroute= _ec2.create_route_table(
                                            VpcId= vpc['Vpc']['VpcId'],
                                            TagSpecifications= [
                                                {
                                                    'ResourceType': 'route-table',
                                                    'Tags': [
                                                        {
                                                            'Key':'Name',
                                                            'Value':'NABPublicRoute'
                                                        },
                                                    ]
                                                },
                                            ]
                                        )

    privateroute= _ec2.create_route_table(
                                            VpcId= vpc['Vpc']['VpcId'],
                                            TagSpecifications= [
                                                {
                                                    'ResourceType': 'route-table',
                                                    'Tags': [
                                                        {
                                                            'Key':'Name',
                                                            'Value':'NABPrivateRoute'
                                                        },
                                                    ]
                                                },
                                            ]
                                        )

    click.echo('Creadas tablas de enrutamiento')

    eip= _ec2.allocate_address(
                                Domain='vpc',
                                TagSpecifications= [
                                                {
                                                    'ResourceType': 'elastic-ip',
                                                    'Tags': [
                                                        {
                                                            'Key':'Name',
                                                            'Value':'NABPEIP'
                                                        },
                                                    ]
                                                },
                                            ]
                            )

    click.echo('Creadas EIP')

    PublicSubnetA = _ec2.create_subnet(
                                        CidrBlock= rango[0:5]+'10.0/24',
                                        VpcId= vpc['Vpc']['VpcId'],
                                        AvailabilityZone= region+'a',
                                        TagSpecifications= [
                                            {
                                                'ResourceType': 'subnet',
                                                'Tags': [
                                                    {
                                                        'Key':'Name',
                                                        'Value':'NABPublicSubA'
                                                    },
                                                ]
                                            },
                                        ]
                                    )

    click.echo('creada subnet publica '+ PublicSubnetA['Subnet']['SubnetId'])
    
    PublicSubnetB = _ec2.create_subnet(
                                        CidrBlock= rango[0:5]+'20.0/24',
                                        VpcId= vpc['Vpc']['VpcId'],
                                        AvailabilityZone= region+'b',
                                        TagSpecifications= [
                                            {
                                                'ResourceType': 'subnet',
                                                'Tags': [
                                                    {
                                                        'Key':'Name',
                                                        'Value':'NABPublicSubB'
                                                    },
                                                ]
                                            },
                                        ]
                                    )

    click.echo('creada subnet publica '+ PublicSubnetB['Subnet']['SubnetId'])

    PublicSubnetC = _ec2.create_subnet(
                                        CidrBlock= rango[0:5]+'30.0/24',
                                        VpcId= vpc['Vpc']['VpcId'],
                                        AvailabilityZone= region+'c',
                                        TagSpecifications= [
                                            {
                                                'ResourceType': 'subnet',
                                                'Tags': [
                                                    {
                                                        'Key':'Name',
                                                        'Value':'NABPublicSubC'
                                                    },
                                                ]
                                            },
                                        ]
                                    )

    click.echo('creada subnet publica '+ PublicSubnetC['Subnet']['SubnetId'])

    PrivateSubnetA = _ec2.create_subnet(
                                        CidrBlock= rango[0:5]+'40.0/24',
                                        VpcId= vpc['Vpc']['VpcId'],
                                        AvailabilityZone= region+'a',
                                        TagSpecifications= [
                                            {
                                                'ResourceType': 'subnet',
                                                'Tags': [
                                                    {
                                                        'Key':'Name',
                                                        'Value':'NABPrivSubA'
                                                    },
                                                ]
                                            },
                                        ]
                                    )

    click.echo('creada subnet privada '+ PrivateSubnetA['Subnet']['SubnetId'])

    PrivateSubnetB = _ec2.create_subnet(
                                        CidrBlock= rango[0:5]+'50.0/24',
                                        VpcId= vpc['Vpc']['VpcId'],
                                        AvailabilityZone= region+'b',
                                        TagSpecifications= [
                                            {
                                                'ResourceType': 'subnet',
                                                'Tags': [
                                                    {
                                                        'Key':'Name',
                                                        'Value':'NABPrivSubB'
                                                    },
                                                ]
                                            },
                                        ]
                                    )

    click.echo('creada subnet privada '+ PrivateSubnetB['Subnet']['SubnetId'])

    PrivateSubnetC = _ec2.create_subnet(
                                        CidrBlock= rango[0:5]+'60.0/24',
                                        VpcId= vpc['Vpc']['VpcId'],
                                        AvailabilityZone= region+'c',
                                        TagSpecifications= [
                                            {
                                                'ResourceType': 'subnet',
                                                'Tags': [
                                                    {
                                                        'Key':'Name',
                                                        'Value':'NABPrivSubC'
                                                    },
                                                ]
                                            },
                                        ]
                                    )
    
    click.echo('creada subnet privada '+ PrivateSubnetC['Subnet']['SubnetId'])

    natgw= _ec2.create_nat_gateway(
                                    AllocationId=eip['AllocationId'],
                                    SubnetId=PublicSubnetA['Subnet']['SubnetId'],
                                    TagSpecifications= [
                                                {
                                                    'ResourceType': 'natgateway',
                                                    'Tags': [
                                                        {
                                                            'Key':'Name',
                                                            'Value':'NABNat'
                                                        },
                                                    ]
                                                },
                                            ]
                                )

    private_route= _ec2.create_route(
                                        DestinationCidrBlock='0.0.0.0/0',
                                        GatewayId= natgw['NatGateway']['NatGatewayId'],
                                        RouteTableId= privateroute['RouteTable']['RouteTableId']
                                    )

    public_route= _ec2.create_route(
                                        DestinationCidrBlock='0.0.0.0/0',
                                        GatewayId= igw['InternetGateway']['InternetGatewayId'],
                                        RouteTableId= publicroute['RouteTable']['RouteTableId']
                                    )