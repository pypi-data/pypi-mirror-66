from setuptools import setup

setup(
    name='aws-cdk-example-lambda',
    version='1.0.0',

    description='A really simple no-op lambda function',

    data_files=['handler.py'],

    python_requires='>=3.8',
)
