from importlib.metadata import entry_points
from setuptools import setup

setup(
    name='Nabp',
    version='1.0',
    py_modules=['nabp'],
    install_requires=[
        'Click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        nabp=nabp:cli
    ''',
)