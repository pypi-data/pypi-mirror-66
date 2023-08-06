import codecs
import re

from pathlib import Path
from setuptools import setup, find_namespace_packages

here = Path(__file__).parent


def read(*parts):
    return codecs.open(here.joinpath(*parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='aws-cdk.zip-asset-code',
    version=find_version('aws_cdk', 'zip_asset_code', '__init__.py'),

    description='AWS CDK extension for aws-cdk.aws-lambda',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    packages=find_namespace_packages(include='aws-cdk/*'),

    python_requires='>=3.8',
    install_requires=[
        'aws-cdk.aws-lambda'
    ]
)
