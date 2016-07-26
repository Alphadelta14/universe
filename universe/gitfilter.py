"""Git Filters for Smudging/ Cleaning version files
"""

import argparse
import os
import re
import subprocess
import sys


FILTER_DEFINITION = """
# run `cat .gitfilters >> .git/config`
[filter "universe-release"]
    clean = universe-clean %f
    smudge = universe-smudge %f
"""


def clean():
    """Replaces sha.SHABLOB with sha.$Id$ in the specified version file
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('version-file')
    args = parser.parse_args()
    with open(args.version_file, 'r+') as handle:
        contents = handle.read()
        contents = re.sub(r'sha.[0-9a-f]{40}', r'sha.\$Id\$', contents)
        handle.seek(0)
        handle.write(contents)


def smudge():
    """Replaces sha.$Id$ with sha.SHABLOB in the specified version file
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('version-file')
    args = parser.parse_args()
    with open(args.version_file, 'r+') as handle:
        contents = handle.read()
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
        contents = contents.replace('$Id$', sha, contents)
        handle.seek(0)
        handle.write(contents)


def main():
    """Add gitattributes for version file
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', help='Initial version')
    parser.add_argument('--version-file', default=None)
    parser.add_argument('package-dir')
    args = parser.parse_args()
    if not args.version_file:
        args.version_file = os.path.join(args.package_dir, 'version.py')
    with open('.gitattributes', 'a') as handle:
        handle.write('{}    filter=universe-release\n'.format(
            args.version_file))
    with open('.gitfilters', 'a') as handle:
        handle.write(FILTER_DEFINITION)
    return


if __name__ == '__main__':
    sys.exit(main())
