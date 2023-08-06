import os
import shlex
import subprocess
import sys
import zipfile
from contextlib import contextmanager
from pathlib import Path

from aws_cdk.aws_lambda import AssetCode

__all__ = ['ZipAssetCode']
__version__ = '1.0.0'

# packages that are already part of the Lambda runtime which we thus do not need to package
EXCLUDE_PACKAGES = {'boto3', 'botocore', 'docutils', 'jmespath', 'pip', 'python-dateutil', 's3transfer', 'setuptools'}


@contextmanager
def current_directory(new_dir):
    old_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        yield os.getcwd()
    finally:
        os.chdir(old_dir)


def zipd(root_dir, handle):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for p in EXCLUDE_PACKAGES.intersection(dirnames):
            dirnames.remove(p)
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            handle.write(filepath, arcname=os.path.relpath(filepath, root_dir), compress_type=zipfile.ZIP_DEFLATED)


def package(path_to_code: Path) -> Path:
    with current_directory(path_to_code) as cwd:
        subprocess.check_call(shlex.split(f'{sys.executable} -m pip install -qq --upgrade . --target {cwd}/dist/site-packages'))
    target = path_to_code / 'dist'
    archive = target / 'lambda.zip'
    with zipfile.ZipFile(archive, 'w') as handle:
        zipd(target, handle)
    return archive


class ZipAssetCode(AssetCode):
    """Build and package a Lambda function deployment archive with dependencies."""
    def __init__(self, path_to_code: str):
        path_to_code = Path(path_to_code)
        if not path_to_code.is_dir():
            raise ValueError(f'{path_to_code} does not exist.')
        super().__init__(package(path_to_code).as_posix())

    @property
    def is_inline(self) -> bool:
        return False

