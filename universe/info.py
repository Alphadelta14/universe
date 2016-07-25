"""
Universe Release Versioning - Version Information
"""

import sys

from universe.dev import DevelopmentMetadata


class VersionInfo(tuple):
    """Provide information about a version

    This subclasses a tuple to be compliant with other expectations of
    ``__version_info__``
    """
    def __new__ (cls, *args, **kwargs_):
        return tuple.__new__(cls, args)

    def __init__(self, *args, **kwargs):
        # tuple.__init__(self, *args)
        self.branch = None
        self.dev = None
        try:
            self.major = int(self[0])
        except ValueError:
            branches = str(self[0]).split('-')
            point_info = branches.pop(0).split('.')
            self.major = int(point_info[0])
            self.minor = int(point_info[1])
            self.patch = int(point_info[2])
            if self.patch == 0:
                try:
                    point_info = branches.pop(0).split('.')
                except IndexError:
                    raise ValueError(
                        'Development version (p=0) requires true tip after'
                    )
                if (self.major != int(point_info[0])
                        or self.minor != int(point_info[1])):
                    raise ValueError(
                        'Major and Minor version should match development tip'
                    )
                self.patch = int(point_info[2])
                if self.patch == 0:
                    raise ValueError('Patch cannot be 0 in true tip')
                try:
                    self.dev = DevelopmentMetadata(branches.pop(0))
                except IndexError:
                    raise ValueError('Development metadata must be present')
                if branches:
                    raise ValueError('Patch must be 0 in branch tip')
            if branches:
                self.branch = VersionInfo('-'.join(branches))
        else:
            self.minor = int(self[1])
            self.patch = int(self[2])
            if self.patch == 0:
                raise ValueError('Patch cannot be 0 in true tip')
        if kwargs.get('branch'):
            self.branch = VersionInfo(kwargs['branch'])
        if kwargs.get('dev'):
            self.dev = DevelopmentMetadata(kwargs['dev'])


def module_version_info(module, detect_dev=True):
    """Gets a ``VersionInfo`` object from this module. It expects to see
    a ``__version__`` attribute with the respective string
    """
    if detect_dev:
        dev = DevelopmentMetadata.detect()
    return VersionInfo(module.__version__, dev=dev)


def package_version_info(package, detect_dev=True):
    """Gets a ``VersionInfo`` object from this package name. It expects to
    see a ``__version__`` attribute with the respective string.
    """
    return module_version_info(sys.modules[package], detect_dev)
