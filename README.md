
# Universe Release Versioning 1.0.0
This versioning system is meant to handle the aspect of release branching and unique development versions.

Initial implementation shall be provided in Python, but may be extended to other languages.

# Versioning Requirements

## Absolute Ordering
Versions must be ordered in such a way that there is always an upgrade version. Development versions should never be sorted as the highest version.

## Arbitrary Insertion
*Releases are only linear in an ideal world*

Versions must allow an arbitrary number of insertions between any other given versions to account for patches, minor updates, and backported features.

## Development Builds cannot conflict
Every development build is expectedly unique and should be allowed to have an associated release.

## Every Release has a unique version
Releases are not allowed to be overwritten because as soon as something is released, it is possible that something has already obtained the invalid build and will not know to upgrade.

# Version Specification

## Major.Minor.Patch Version Triple
This is a typical semantic approach to versioning (SemVer). Version starts at 0.1.0 when in rapid development phase; Minor version is updated for each released change. Major version becomes 1 when the API is public and then is incremented for each backward incompatible release. Minor version starts at 0 for each Major version bump. When a backwards compatible change is made, Minor version is bumped. Patch is set to 0 for each Minor version bump and is incremented for an internal update to fix unexpected behavior without making any updating changes. All three numbers should be present and are treated as distinct integers, so 9 goes to 10 instead of forcing a roll-over.

## -Major.Minor.Patch Branches
When changes are made to a version that is not the most recent one, they should be suffixed with another version triple. The new branch should be considered a tip release and can be incremented normally. This format can be recursed with caution.

### Example
A package was just released at 3.0.0. There are a number of clients still using the 2.0.0 version. The new version contains a feature that has been a good-to-have for a while now. Clients using 2.0.0 code request that that feature be backported since it is still compatible with the current API.
A version 2.0.0-0.1.0 version would be released as a feature update.

### Example 2
Like above, except that there was a bugfix soon after that needed to be applied to that feature, and the backported one. The new version would be 2.0.0-0.1.1.

## Development Builds
Any local version shall be considered a development build.
In order to accommodate absolute ordering while maintaining strict implementation rules, versions will hop back 1e-N patches in degree notation before suffixing development information. Development versions shall use a hyphen to separate the main version information from the development metadata. For VCS controlled builds, use -sha as the prefix followed immediately by the sha-sum of the current version.

### Example
2.1.0 Release build

2.0.99-sha.2c3fa0dd96e08273f8531db160e6236440f8f1d9 Development build for next release (either 2.2.0, 2.1.1 or 3.0.0)

## Pre-release Versions
Pre-releases should be considered as published development builds. Use the metadata prefixes a.N, b.N, rc.N


## Post-release Versions
Post-releases should be treated as patches.