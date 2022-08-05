"""
 * 
 * SPDX-License-Identifier: Apache 2
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

from tokenize import Name
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

# limitregions with aws:RequestedRegion ?
# request tags 
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

    try:
        analyzerclient.create_analyzer(
                                    analyzerName= analyzer_nombre,
                                    type= 'ACCOUNT'
                                   )
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('Ya existe un analyzer con el nombre especificado... continuando')
        else:
            print('Error inesperado al crear el analyzer... saliendo')
            pass

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
    adminpwd = random.choice(string.ascii_lowercase)
    adminpwd += random.choice(string.ascii_uppercase)
    adminpwd += random.choice(string.digits)
    adminpwd += random.choice(string.punctuation)
    adminpwd+= ''.join(random.choice(characters) for i in range(4))

    devpwd = random.choice(string.ascii_lowercase)
    devpwd += random.choice(string.ascii_uppercase)
    devpwd += random.choice(string.digits)
    devpwd += random.choice(string.punctuation)
    devpwd += ''.join(random.choice(characters) for i in range(4))

    audpwd = random.choice(string.ascii_lowercase)
    audpwd += random.choice(string.ascii_uppercase)
    audpwd += random.choice(string.digits)
    audpwd += random.choice(string.punctuation)
    audpwd += ''.join(random.choice(characters) for i in range(4))

    finpwd = random.choice(string.ascii_lowercase)
    finpwd += random.choice(string.ascii_uppercase)
    finpwd += random.choice(string.digits)
    finpwd += random.choice(string.punctuation)
    finpwd += ''.join(random.choice(characters) for i in range(4))
    
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
            print('error inesperado...saliendo', error)
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
            print('error inesperado...saliendo', error)
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
            print('error inesperado...saliendo', error)
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
            print('error inesperado...saliendo', error)
            return 'perfil de login no se pudo crear', error

    click.echo('El usuario {0} se creo con password temporal: {1}'.format(fin1['User']['UserName'],finpwd))



@core.command('presupuesto')
@click.option('--nombre', default='nabpBudget',help='mnombre del presupuesto a crear')
@click.option('--monto', default=None, required=True, help='monto, en USD, del presupuesto a crear')
@click.option('--email', default=None, required=True, help='email para enviar notificaciones relacionadas con el presupuesto')
@pass_config
def presupuesto(config, nombre,monto, email):
    "establece presupuesto y alertas"
    sess = config.session
    id = sess.client('sts').get_caller_identity()['Account']
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
@click.option('--region', default='us-east-1', help='Region sobre la que se desplegara la VPC')
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


@cli.group('monitor')
@pass_config
def monitor(config):
    """Comandos monitoreo"""

@monitor.command('trail')
@click.option('--nombre', default= 'nabptrail', help= 'nombre de el trail')
@pass_config
def trail(config, nombre):
    "Habilita cloud trail y crea un bucket para guardar los logs de acceso"
    sess= config.session
    id = sess.client('sts').get_caller_identity()['Account']
    trail= sess.client('cloudtrail')
    s3= sess.client('s3')
    s3r= sess.resource('s3')
    trailBucketName= 'nabp-trail-bucket'+ ''.join(random.choice(string.digits) for i in range(8))
    
    while s3r.Bucket(trailBucketName) in s3r.buckets.all():
        trailBucketName= 'nabp-trail-bucket'+ ''.join(random.choice(string.digits) for i in range(8))
    
    #create s3 buckets to store trails
    trailbucket= s3.create_bucket(
        Bucket= trailBucketName,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-west-2'
        },
    )
    # defines bucket policy for trail bucket
    dict={
            "Version": "2012-10-17",
            "Statement": [
                    {
                        "Sid": "AWSCloudTrailAclCheck20150319",
                        "Effect": "Allow",
                        "Principal": {"Service": "cloudtrail.amazonaws.com"},
                        "Action": "s3:GetBucketAcl",
                        "Resource": "arn:aws:s3:::"+trailBucketName,
                        "Condition": {
                            "StringEquals": {
                                "aws:SourceArn": "arn:aws:cloudtrail:us-east-1:"+id+":trail/"+nombre
                            }
                        }
                    },
                    {
                        "Sid": "AWSCloudTrailWrite20150319",
                        "Effect": "Allow",
                        "Principal": {"Service": "cloudtrail.amazonaws.com"},
                        "Action": "s3:PutObject",
                        "Resource": "arn:aws:s3:::"+trailBucketName+"/new-account-trail/AWSLogs/"+id+"/*",
                        "Condition": {
                                        "StringEquals": {
                                            "s3:x-amz-acl": "bucket-owner-full-control",
                                            "aws:SourceArn": "arn:aws:cloudtrail:us-east-1:"+id+":trail/"+nombre
                                        }
                        }
                    }
                ]
        }

    bucketPolicy=json.dumps(dict)
    
    s3.put_bucket_policy(
        Bucket=trailBucketName,
        Policy= bucketPolicy
    )
    click.echo('trailbucket creado')

    # create trail for all regions
    nabptrail= trail.create_trail(
        Name=nombre,
        S3BucketName=trailBucketName,
        S3KeyPrefix='new-account-trail',
        #SNSTopicName='',
        IncludeGlobalServiceEvents=True,
        IsMultiRegionTrail=True,
        EnableLogFileValidation=True,
        #CloudWatchLogsLogGroupArn='string',
        #CloudWatchLogsRoleArn='string',
        #KmsKeyId='string',
        TagsList=[
            {
                'Key': 'Creator',
                'Value': 'NABP'
            },
        ]
    )

    trail.start_logging(
        Name= nombre
    )

    click.echo("creado el trail")


    


@monitor.command('config')
#@click.option('--rango', default= '10.0.0.0/16', help= 'rango ipv4 para la vpc')
@pass_config
def configuracion(config):
    "Habilita aws config para todos los recursos y crea reglas basicas para monitorear configuracion de recursos comunes como s3"
    sess= config.session
    iam = sess.client('iam')
    awsconfig =  sess.client('config')

    asume_policy = json.dumps({
        "Version":"2012-10-17",
        "Statement": [
            {
                "Effect":"Allow",
                "Principal":{
                    "Service":"config.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    })

    config_role=iam.create_role(
        RoleName='nabp_config_role',
        AssumeRolePolicyDocument=asume_policy,
    )

    iam.attach_role_policy(RoleName='nabp_config_role',PolicyArn='arn:aws:iam::aws:policy/service-role/AWSConfigRole')

    awsconfig.put_configuration_recorder(
        ConfigurationRecorder={
            'name': 'nabpRecorder',
            'roleARN': config_role['Role']['Arn'],
            'recordingGroup':{
                'allSupported': True,
                'includeGlobalResourceTypes': True,
            }
        }
    )

    awsconfig.start_configuration_recorder(
        COnfigurationRecorderName='nabpRecorder'
    )

    # alert on public s3 buckets
     #s3-bucket-public-read-prohibited
    awsconfig.put_config_rule(
        ConfigRule={
            'ConfigRuleName': 'S3PublicRead',
            'Description':'S3 Public Read Prohibited Bucket Rule',
            'Scope':{
                'ComplianceResourceTypes':['AWS::S3::Bucket']
            },
            'Source':{
                'Owner':'AWS',
                'SourceIdentifier': 'S3_BUCKET_PUBLIC_READ_PROHIBITED'
            },
            'InputParameters': '{}',
            'ConfigRuleState':'ACTIVE'

        }
    )
    awsconfig.put_config_rule(
        ConfigRule={
            'ConfigRuleName': 'S3logging',
            'Description':'S3 Public Read Prohibited Bucket Rule',
            'Scope':{
                'ComplianceResourceTypes':['AWS::S3::Bucket']
            },
            'Source':{
                'Owner':'AWS',
                'SourceIdentifier': 'S3_BUCKET_LOGGING_ENABLED'
            },
            'InputParameters': '{}',
            'ConfigRuleState':'ACTIVE'

        }
    )

     #s3-bucket-loggigng-enabled
     #s3-bucket-public-write-prohibited
     #s3-bucket-ssl-requests-only
    # alert open SG
    # RDS instances open to internet
    # automation on config rules
    # review MFA enabled
    # enforce MFA?

# Habilitar Guard duty
# guar duty findings
# security hub ?
# habilitar Macie ?
# Session Manager for ec2 ?
# patch manager ?
# rules for rotating IAM keys?
# activate aws SSO?

