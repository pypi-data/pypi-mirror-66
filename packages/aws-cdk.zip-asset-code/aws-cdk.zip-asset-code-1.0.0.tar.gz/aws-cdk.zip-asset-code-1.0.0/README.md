```python
from aws_cdk import aws_lambda as lambda_
from aws_cdk.zip_asset_code import ZipAssetCode

lambda_.Function(stack, 'ExampleLambdaFunction',
                 code=ZipAssetCode('example-lambda/'),
                 handler='handler.handler',
                 runtime=lambda_.Runtime.PYTHON_3_8)
```
(snippet from [example-cdk-lambda.py](examples/example-cdk-lambda.py))
