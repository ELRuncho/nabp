from email.policy import Policy
import click
import boto3
import json, string, random
from botocore.exceptions import ClientError

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

@cli.group('core')
@pass_config
def core(config):
    """Comandos core"""


@core.command('seguridad')
@click.option('--analyzer_nombre', default='miAnalyzer', help="nombre del analyzer")
@click.option('--nombre_admin_g', default='Administradores', help="nombre para el grupo de administradores")
@click.option('--nombre_dev_g', default='Developers', help="nombre para el grupo de desarrolladores")
@click.option('--nombre_audit_g', default='Auditores', help="nombre para el grupo de auditores")
@click.option('--nombre_fin_g', default='Finanzas', help="nombre para el grupo de finanzas")
@pass_config
def coresec(config, analyzer_nombre,nombre_admin_g,nombre_dev_g,nombre_audit_g,nombre_fin_g):
    "Desplega medidas de seguridad core. Access analizer, 4 grupos IAM, y usuarios base de esos grupos"
    sess = config.session
    
    analyzerclient = sess.client('accessanalyzer')

    iamclient = sess.client('iam')

    click.echo('creando analyzer')
    analyzerclient.create_analyzer(
                                    analyzerName= analyzer_nombre,
                                    type= 'ACCOUNT'
                                )
                
    click.echo('creado analyzer')

    try:
        admingroup= iamclient.create_group(GroupName= nombre_admin_g)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('El groupo Administradores ya existe....usare el grupo existente')
        else:
            print('Error inesperado al crear el grupo.. saliendo', error)
            return 'No se pudo crear el grupo', error

    try:
        devgroup= iamclient.create_group(GroupName= nombre_dev_g)    
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('El groupo Developers ya existe....usare el grupo existente')
        else:
            print('Error inesperado al crear el grupo.. saliendo', error)
            return 'No se pudo crear el grupo', error

    try:
        auditgroup= iamclient.create_group(GroupName= nombre_audit_g)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('El groupo Auditores ya existe....usare el grupo existente')
        else:
            print('Error inesperado al crear el grupo.. saliendo', error)
            return 'No se pudo crear el grupo', error

    try:
        fingroup= iamclient.create_group(GroupName= nombre_fin_g)    
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('El groupo Finanzas ya existe....usare el grupo existente')
        else:
            print('Error inesperado al crear el grupo.. saliendo', error)
            return 'No se pudo crear el grupo', error
    
    iamclient.attach_group_policy(
                                    GroupName=admingroup['Group']['GroupName'],
                                    PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
                                )

    iamclient.attach_group_policy(
                                    GroupName=auditgroup['Group']['GroupName'],
                                    PolicyArn='arn:aws:iam::aws:policy/ReadOnlyAccess'
                                )

    iamclient.attach_group_policy(
                                    GroupName=fingroup['Group']['GroupName'],
                                    PolicyArn='arn:aws:iam::aws:policy/job-function/Billing'
                                )

    iamclient.attach_group_policy(
                                    GroupName=devgroup['Group']['GroupName'],
                                    PolicyArn='arn:aws:iam::aws:policy/PowerUserAccess'
                                )

    click.echo('Grupos y politicas creadas')

    try:
        admin1= iamclient.create_user(UserName='Admin1',)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('El usuario Admin1 ya existe')
            return 'el usuario ya existe'
        else:
            click.echo('Error inesperado al crear el usuario', error)
            return 'no se pudo crear el usuario', error
    
    try:
        dev1= iamclient.create_user(UserName='dev1',)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('El usuario dev1 ya existe')
            return 'el usuario ya existe'
        else:
            click.echo('Error inesperado al crear el usuario', error)
            return 'no se pudo crear el usuario', error 

    try:
        aud1= iamclient.create_user(UserName='aud1',)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('El usuario aud1 ya existe')
            return 'el usuario ya existe'
        else:
            click.echo('Error inesperado al crear el usuario', error)
            return 'no se pudo crear el usuario', error

    try:
        fin1= iamclient.create_user(UserName='fin1',)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('El usuario fin1 ya existe')
            return 'el usuario ya existe'
        else:
            click.echo('Error inesperado al crear el usuario', error)
            return 'no se pudo crear el usuario', error

    iamclient.add_user_to_group(
                                GroupName=admingroup['Group']['GroupName'],
                                UserName=admin1['User']['UserName']
                            )
    
    iamclient.add_user_to_group(
                                GroupName=devgroup['Group']['GroupName'],
                                UserName=dev1['User']['UserName']
                            )
    
    iamclient.add_user_to_group(
                                GroupName=auditgroup['Group']['GroupName'],
                                UserName=aud1['User']['UserName']
                            )

    iamclient.add_user_to_group(
                                GroupName=fingroup['Group']['GroupName'],
                                UserName=fin1['User']['UserName']
                            )

    characters = string.ascii_letters + string.digits + string.punctuation
    adminpwd= ''.join(random.choice(characters) for i in range(8))
    devpwd= ''.join(random.choice(characters) for i in range(8))
    audpwd= ''.join(random.choice(characters) for i in range(8))
    finpwd= ''.join(random.choice(characters) for i in range(8))
    
    try:
        admin1login=iamclient.create_login_profile(
            UserName=admin1['User']['UserName'],
            Password=adminpwd,
            PasswordResetRequired= True
        )
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('el perfil de login de admin1 ya existe')
        else:
            click.echo('error inesperado...saliendo', error)
            return 'perfil de login no se pudo crear', error

    click.echo('El usuario {0} se creo con password temporal: {1}'.format(admin1['User']['UserName'],adminpwd))

    try:
        dev1login=iamclient.create_login_profile(
            UserName=dev1['User']['UserName'],
            Password=devpwd,
            PasswordResetRequired= True
        )
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('el perfil de login de dev1 ya existe')
        else:
            click.echo('error inesperado...saliendo', error)
            return 'perfil de login no se pudo crear', error

    click.echo('El usuario {0} se creo con password temporal: {1}'.format(dev1['User']['UserName'],devpwd))

    try:
        aud1login=iamclient.create_login_profile(
            UserName=aud1['User']['UserName'],
            Password=audpwd,
            PasswordResetRequired= True
        )
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('el perfil de login de aud1 ya existe')
        else:
            click.echo('error inesperado...saliendo', error)
            return 'perfil de login no se pudo crear', error

    click.echo('El usuario {0} se creo con password temporal: {1}'.format(aud1['User']['UserName'],audpwd))

    try:
        fin1login=iamclient.create_login_profile(
            UserName=fin1['User']['UserName'],
            Password=finpwd,
            PasswordResetRequired= True
        )
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('el perfil de login de fin1 ya existe')
        else:
            click.echo('error inesperado...saliendo', error)
            return 'perfil de login no se pudo crear', error

    click.echo('El usuario {0} se creo con password temporal: {1}'.format(fin1['User']['UserName'],finpwd))



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

    natwaiter = _ec2.get_waiter('nat_gateway_available')
    click.echo('creando nat gateway')
    natwaiter.wait(
        NatGatewayIds= [natgw['NatGateway']['NatGatewayId'],],
        WaiterConfig= {
            'Delay': 30,
            'MaxAttempts': 30
        }
    )

    click.echo('nat creado')
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

    _ec2.associate_route_table(
        RouteTableId= publicroute['RouteTable']['RouteTableId'],
        SubnetId= PublicSubnetA['Subnet']['SubnetId'],
    )

    _ec2.associate_route_table(
        RouteTableId= publicroute['RouteTable']['RouteTableId'],
        SubnetId= PublicSubnetB['Subnet']['SubnetId'],
    )

    _ec2.associate_route_table(
        RouteTableId= publicroute['RouteTable']['RouteTableId'],
        SubnetId= PublicSubnetC['Subnet']['SubnetId'],
    )
    
    _ec2.associate_route_table(
        RouteTableId= privateroute['RouteTable']['RouteTableId'],
        SubnetId= PrivateSubnetA['Subnet']['SubnetId'],
    )

    _ec2.associate_route_table(
        RouteTableId= privateroute['RouteTable']['RouteTableId'],
        SubnetId= PrivateSubnetB['Subnet']['SubnetId'],
    )

    _ec2.associate_route_table(
        RouteTableId= privateroute['RouteTable']['RouteTableId'],
        SubnetId= PrivateSubnetC['Subnet']['SubnetId'],
    )
    click.echo('rutas asociadas')