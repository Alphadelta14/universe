
import datetime
import os
import subprocess
import sys


class DevelopmentMetadata(object):
    """Metadata for Development Versions

    Example:
    >>> data = DevelopmentMetadata(
        'sha.2c3fa0dd96e08273f8531db160e6236440f8f1d9')
    >>> print(data.type)
    sha
    >>> print(data.value)
    2c3fa0dd96e08273f8531db160e6236440f8f1d9
    """
    def __init__(self, metadata):
        self.type, self.value = metadata.split('.')

    @staticmethod
    def detect(module):
        """Detects a if a pip package is locally installed as a dev version

        It does this by detecting if the path where the module exists was
        a customly added path

        `pip install -e .` and `setup.py develop` will add `cwd` to `sys.path`
        """
        package_dir = os.path.realpath(os.path.join(
            os.path.dirname(module.__file__), '..'))
        # If this has site-packages, then it is considered a release install
        if 'site-packages' in package_dir:
            return None
        if os.path.isdir(os.path.join(package_dir, '.git')):
            try:
                sha = subprocess.check_output(
                    ['git', 'rev-parse', 'HEAD'],
                    cwd=package_dir, stderr=subprocess.STDOUT
                ).strip()
                return 'sha.{}'.format(sha)
            except subprocess.CalledProcessError:
                pass
        return 'date.{}'.format(
            datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        )
