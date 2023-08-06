from aws_cdk import (
    aws_lambda as lambda_,
    core
)
from aws_cdk.zip_asset_code import ZipAssetCode

app = core.App()
stack = core.Stack(app, 'ExampleLambdaStack')
lambda_.Function(stack, 'ExampleLambdaFunction',
                 code=ZipAssetCode('example-lambda/'),
                 handler='handler.handler',
                 runtime=lambda_.Runtime.PYTHON_3_8)
app.synth()
