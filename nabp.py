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
    """Core Comands"""

# limitregions with aws:RequestedRegion ?
# request tags 
@core.command('security')
@click.option('--analyzer_name', default='myAnalyzer', help="name for the iam analyzer")
@click.option('--admin_g_name', default='Administrators', help="name for the administrator group")
@click.option('--dev_g_name', default='Developers', help="name for the developer group")
@click.option('--audit_g_name', default='Auditors', help="name for the auditors group")
@click.option('--fin_g_name', default='Finance', help="name for the finance group")
@pass_config
def coresec(config, analyzer_name,admin_g_name,dev_g_name,audit_g_name,fin_g_name):
    "Deploys core security: Access analizer, 4 IAM groups and one IAM user for each group"
    sess = config.session
    
    analyzerclient = sess.client('accessanalyzer')

    iamclient = sess.client('iam')

    click.echo('Creating analyzer')

    try:
        analyzerclient.create_analyzer(
                                    analyzerName= analyzer_name,
                                    type= 'ACCOUNT'
                                   )
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('An analyzer with the specified name already exist... carrying on')
        else:
            print('Unexpected error creating the analyzer... exiting')
            pass

    click.echo('Analyzer Created')

    try:
        admingroup= iamclient.create_group(GroupName= admin_g_name)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The administrator group already exist.... Ill use the existing group')
        else:
            print('Unexpected Error creating the administrator group.. exiting ', error)
            return 'The group could not be created ', error

    try:
        devgroup= iamclient.create_group(GroupName= dev_g_name)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The Developers group already exist.... Ill use the existing group')
        else:
            print('Unexpected Error creating the developers group.. exiting ', error)
            return 'The group could not be created ', error

    try:
        auditgroup= iamclient.create_group(GroupName= audit_g_name)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The Auditors group already exist.... Ill use the existing group')
        else:
            print('Unexpected Error creating the auditors group.. exiting ', error)
            return 'The group could not be created ', error

    try:
        fingroup= iamclient.create_group(GroupName= fin_g_name)    
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The Finance group already exist.... Ill use the existing group')
        else:
            print('Unexpected Error creating the auditors group.. exiting ', error)
            return 'The group could not be created ', error
    
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

    click.echo('Groups and policies created')

    try:
        admin1= iamclient.create_user(UserName='Admin1',)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The user Admin1 already exists')
            return 'The user already exists'
        else:
            click.echo('Unexpected Error creating Admin1 user ', error)
            return 'The user could not be created ', error
    
    try:
        dev1= iamclient.create_user(UserName='dev1',)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The user dev1 already exists')
            return 'The user already exists'
        else:
            click.echo('Unexpected Error creating dev1 user ', error)
            return 'The user could not be created ', error 

    try:
        aud1= iamclient.create_user(UserName='aud1',)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The user aud1 already exists ')
            return 'The user already exists'
        else:
            click.echo('Unexpected Error creating aud1 user ', error)
            return 'The user could not be created ', error

    try:
        fin1= iamclient.create_user(UserName='fin1',)
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The user fin1 already exists ')
            return 'The user already exists'
        else:
            click.echo('Unexpected Error creating fin1 user ', error)
            return 'The user could not be created ', error

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
            click.echo('The login profile of admin1 already exists')
        else:
            print('Unexpected error...exiting ', error)
            return 'The login profile could not be created ', error

    click.echo('The user {0} has been created with temporary password: {1}'.format(admin1['User']['UserName'],adminpwd))

    try:
        dev1login=iamclient.create_login_profile(
            UserName=dev1['User']['UserName'],
            Password=devpwd,
            PasswordResetRequired= True
        )
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The login profile of dev1 already exists')
        else:
            print('Unexpected error...exiting ', error)
            return 'The login profile could not be created ', error

    click.echo('The user {0} has been created with temporary password: {1}'.format(dev1['User']['UserName'],devpwd))

    try:
        aud1login=iamclient.create_login_profile(
            UserName=aud1['User']['UserName'],
            Password=audpwd,
            PasswordResetRequired= True
        )
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The login profile of aud1 already exists')
        else:
            print('Unexpected error...exiting ', error)
            return 'The login profile could not be created ', error

    click.echo('The user {0} has been created with temporary password: {1}'.format(aud1['User']['UserName'],audpwd))

    try:
        fin1login=iamclient.create_login_profile(
            UserName=fin1['User']['UserName'],
            Password=finpwd,
            PasswordResetRequired= True
        )
    except ClientError as error:
        if error.response['Error']['Code']=='EntityAlreadyExist':
            click.echo('The login profile of fin1 already exists')
        else:
            print('Unexpected error...exiting ', error)
            return 'The login profile could not be created ', error

    click.echo('The user {0} has been created with temporary password: {1}'.format(fin1['User']['UserName'],finpwd))



@core.command('budget')
@click.option('--name', default='nabpBudget',help='name for the budget to be created')
@click.option('--amount', default=None, required=True, help='amount, in USD, for the new budget')
@click.option('--email', default=None, required=True, help='email to send notifications related to the budget')
@pass_config
def presupuesto(config, name,amount, email):
    "Creates a budget and alerts on said budget"
    sess = config.session
    id = sess.client('sts').get_caller_identity()['Account']
    budget=sess.client("budgets")

    click.echo("Creating Budget and Alerts")
    #monto debe ser string
    budget.create_budget(   
                            AccountId=id,
                            Budget={
                                'BudgetName': name,
                                'BudgetLimit': {
                                    'Amount': amount,
                                    'Unit':'USD'
                                },
                                'TimeUnit': 'MONTHLY',
                                'BudgetType': 'COST'
                            }
                        )

    click.echo("Budget created")

    budget.create_notification(
                                AccountId=id,
                                BudgetName= name,
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
                                BudgetName= name,
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

    click.echo("Alerts created")
    click.echo("Added email as subscribers to the alerts")


@cli.group('network')
@pass_config
def network(config):
    """Networking commands"""


@network.command('create')
@click.option('--range', default= '10.0.0.0/16', help= 'ipv4 range for the VPC')
@click.option('--region', default='us-east-1', help='Region where the VPC is to be deployed')
@pass_config
def crear(config, rango, region):
    "Creates a VPC with a CIDR /16  and subnets with a range of /24"
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

    
    click.echo("Created VPC: " + vpc['Vpc']['VpcId'])

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

    click.echo('Created internet gateway: '+ igw['InternetGateway']['InternetGatewayId'] + 'y asignado a VPC '+ vpc['Vpc']['VpcId'])

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

    click.echo('Routing tables created ')

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

    click.echo('EIP Created')

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

    click.echo('Created public subnet: '+ PublicSubnetA['Subnet']['SubnetId'])
    
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

    click.echo('Created public subnet: '+ PublicSubnetB['Subnet']['SubnetId'])

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

    click.echo('Created public subnet: '+ PublicSubnetC['Subnet']['SubnetId'])

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

    click.echo('Created private subnet: '+ PrivateSubnetA['Subnet']['SubnetId'])

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

    click.echo('Created private subnet: '+ PrivateSubnetB['Subnet']['SubnetId'])

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
    
    click.echo('Created private subnet: '+ PrivateSubnetC['Subnet']['SubnetId'])

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
    click.echo('Creating NAT gateway')
    natwaiter.wait(
        NatGatewayIds= [natgw['NatGateway']['NatGatewayId'],],
        WaiterConfig= {
            'Delay': 30,
            'MaxAttempts': 30
        }
    )

    click.echo('NAT gateway created')
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
    click.echo('Route tables asociated')


@cli.group('monitor')
@pass_config
def monitor(config):
    """Monitoring commands"""

@monitor.command('trail')
@click.option('--name', default= 'nabptrail', help= 'name for the trail to be created')
@pass_config
def trail(config, name):
    "Enables Cloud Trail and creates a bucket to store the access logs"
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
                                "aws:SourceArn": "arn:aws:cloudtrail:us-east-1:"+id+":trail/"+name
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
                                            "aws:SourceArn": "arn:aws:cloudtrail:us-east-1:"+id+":trail/"+name
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
    click.echo('trailbucket created')

    # create trail for all regions
    nabptrail= trail.create_trail(
        Name=name,
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
        Name= name
    )

    click.echo("New trail created")


    


@monitor.command('config')
#@click.option('--rango', default= '10.0.0.0/16', help= 'rango ipv4 para la vpc')
@pass_config
def configuracion(config):
    "Enables AWS Config for all resources and creates basic rules to monitor comon resources such as s3"
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
        ConfigurationRecorderName='nabpRecorder'
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

