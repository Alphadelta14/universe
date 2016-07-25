
import os
import subprocess


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
    def detect():
        dev_file = os.path.join(os.path.dirname(__file__), '..', 'local.txt')
        if os.path.exists(dev_file):
            with open(dev_file) as handle:
                local_type = handle.read()
            if local_type.strip() == 'git':
                sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
                return 'sha.{}'.format(sha.strip())
        return None
