"""
Universe Release Versioning - Version Information
"""

import functools
import sys

from universe.dev import DevelopmentMetadata


@functools.total_ordering
class VersionInfo(tuple):
    """Provide information about a version

    This subclasses a tuple to be compliant with other expectations of
    ``__version_info__``
    """
    def __new__(cls, args, **kwargs):
        if not isinstance(args, tuple):
            args = (args,)
        return tuple.__new__(cls, (args,))

    def __init__(self, args, **kwargs):
        if not isinstance(args, tuple):
            args = (args,)
        self.branch = None
        self.dev = None
        try:
            self.major = int(args[0])
        except ValueError:
            branches = str(args[0]).split('-')
            point_info = branches.pop(0).split('.')
            self.major = int(point_info[0])
            self.minor = int(point_info[1])
            self.true_patch = self.patch = int(point_info[2])
            if self.patch == 0:
                try:
                    self.true_patch = int(branches.pop(0))
                except (IndexError, ValueError):
                    raise ValueError(
                        'Development version requires original patch after'
                    )
                try:
                    self.dev = DevelopmentMetadata(branches.pop(0))
                except IndexError:
                    raise ValueError('Development metadata must be present')
                if branches:
                    raise ValueError('Patch cannot be 0 in non-tip')
            if branches:
                self.branch = VersionInfo('-'.join(branches))
        else:
            self.minor = int(args[1])
            self.true_patch = self.patch = int(args[2])
        if kwargs.get('branch'):
            self.branch = VersionInfo(kwargs['branch'])
        if kwargs.get('dev'):
            self.dev = DevelopmentMetadata(kwargs['dev'])
            self.patch = 0
        elif self.true_patch == 0:
            raise ValueError('Patch cannot be 0 in true tip')

    def __getitem__(self, key):
        return (self.major, self.minor, self.patch)[key]

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))

    def __lt__(self, other):
        return self[:3] < other[:3]

    def __eq__(self, other):
        return self[:3] == other[:3]

    def __str__(self):
        return str(self[:3])

    def __repr__(self):
        return repr(self[:3])


def module_version_info(module):
    """Gets a ``VersionInfo`` object from this module. It expects to see
    a ``__version__`` attribute with the respective string
    """
    return VersionInfo(module.__version__)


def package_version_info(package):
    """Gets a ``VersionInfo`` object from this package name. It expects to
    see a ``__version__`` attribute with the respective string.
    """
    return module_version_info(sys.modules[package])
