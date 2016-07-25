
# Universe Release Versioning 1.0.1
This versioning system is meant to handle the aspect of release branching
and unique development versions.

Initial implementation shall be provided in Python, but may be extended to
other languages.

## Why use Universe?
There are a lot of version specifications available. This is meant to
provide more specific support to package managers that have naive version
handling systems in place. It also is to support releasing software that
may have long lived versions that need additional support.

It is easy to convert from SemVer and related versioning to Universe. It
usually just involves replacing the 0 Patch with a 1 on the most recent
release.

### Concrete Example for Development Builds
```bash
$ cat <<INPUT | sort --version-sort
1.11.5
2.0.0-testing_for_2.1.0
1.5.4
2.0.0
INPUT

1.5.4
1.11.5
2.0.0
2.0.0-testing_for_2.1.0
```

Is this ideal? It is certainly expected. Except that one quickly realizes
that, despite the testing release being not ready, naively using the last
result will cause stability problems. Almost every package manager
does this however.

The recommended solution to this is to just not upload these to a
production package distributor, but that does not work well for testing.

So, using Universe's system for versioning:

```bash
$ cat <<INPUT | sort --version-sort
1.11.5
2.0.0-2.0.1-testing_for_2.1.1
1.5.4
2.0.1
INPUT

1.5.4
1.11.5
2.0.0-2.0.1-testing_for_2.1.1
2.0.1
```

This leaves `2.0.1` at the top where we want it.

### Concrete Example for Branches
```bash
$ cat <<INPUT | sort --version-sort
1.11.5-0.1.1
1.11.5
1.5.4
2.0.1
INPUT

1.5.4
1.11.5
1.11.5-0.1.1
2.0.1
```
As desired, we would like `1.11.5-0.1.1` to be the greatest release `<2.0.1`.

# Versioning Requirements

## Absolute Ordering
Versions must be ordered in such a way that there is always an upgrade
version. Development versions should never be sorted as the highest
version.

## Arbitrary Insertion
*Releases are only linear in an ideal world*

Versions must allow an arbitrary number of insertions between any other
given versions to account for patches, minor updates, and backported
features.

## Development Builds cannot conflict
Every development build is expectedly unique and should be allowed to have
an associated release.

## Every Release has a unique version
Releases are not allowed to be overwritten because as soon as something is
released, it is possible that something has already obtained the invalid
build and will not know to upgrade.

# Version Specification

## Major.Minor.Patch Version Triple
This is an approach close to SemVer (consider this a fork). Version starts
at `0.1.1` when in rapid development phase; `Minor` version is updated for each
released change. `Major` version becomes `1` when the API is public and then is
incremented for each backward incompatible release. Minor version starts at
`0` for each `Major` version bump. When a backwards compatible change is made,
`Minor` version is bumped. `Patch`es reserve the special number `0` for
development releases, so `Patch` is set to `1` for each `Minor` version bump and
is incremented for an internal update to fix unexpected behavior without
making any updating changes. All three numbers should be present and are
treated as distinct integers, so `9` goes to `10` instead of forcing a
roll-over. All three numbers are required.

## -Major.Minor.Patch Branches
When changes are made to a version that is not the most recent one, they
should be suffixed with another version triple. The new branch should be
considered a tip release and can be incremented normally. This format can
be recursed with caution.

### Example
A package was just released at `3.0.1`. There are a number of clients still
using the `2.0.1` version. The new version contains a feature that has been a
good-to-have for a while now. Clients using `2.0.1` code request that that
feature be backported since it is still compatible with the current API.
A version `2.0.1-0.1.1` version would be released as a feature update.

### Example 2
Like above, except that there was a bugfix soon after that needed to be
applied to that feature, and the backported one. The new version would be
`2.0.1-0.1.2`.

## Development Builds
Any local version shall be considered a development build. A special value
for `Patch` is reserved for Development builds; Patch is `0` here only. This
accommodates absolute ordering. To preserve information about the tip,
the tip information is appended similarly to a branch directly after the
development version. Lastly, a development identifier follows. Development
identifiers must not start with a number.

### Example
`2.1.1` Release build

`2.1.0-2.1.1-sha.2c3fa0dd96e08273f8531db160e6236440f8f1d9` Development
build for next release (either `2.2.1`, `2.1.2`, or `3.0.1`)

`2.45.56` Release build

`2.44.0-2.45.56-sha.4b30d1d59e796e8796b43916f1d153a90c34a38b` Development
build for next release (either `2.46.1`, `2.45.57`, or `3.1.1`)

`3.0.1` Release build

`3.0.0-3.0.1-sha.4b30d1d59e796e8796b43916f1d153a90c34a38b` Development
build for next release (either `3.0.2`, `3.1.1`, or `4.0.1`)

## Pre-release Versions
Pre-releases should be considered as published development builds. Use the
metadata prefixes `a.N`, `b.N`, `rc.N`

## Post-release Versions
Post-releases should be treated as normal patched releases.

## Syntax Summary
<!-- bnf rarely support, use XML highlighting -->
```xml
<post-release> ::= <release>
<pre-release> ::= <dev-branch> "-" <pre-release-metadata> | <release> "-" <dev-branch> "-" <pre-release-metadata>
<dev-release> ::= <dev-branch> "-" <dev-metadata> | <release> "-" <dev-branch> "-" <dev-metadata>
<release> ::= <branch> | <release> "-" <branch>

<dev-branch> ::= <major> "." <minor> "." <dev-patch> "-" <branch>
<branch> ::= <major> "." <minor> "." <patch>
<major> ::= <non-negative>
<minor> ::= <non-negative>
<patch> ::= <positive>
<dev-patch> ::= <zero>
<pre-release-metadata> ::= <pre-release-identifier> "." <non-negative>
<pre-release-identifier> ::= "a" | "b" | "rc"
<dev-metadata> ::= <dev-identifier> "." <metadata>
<dev-identifier> ::= <letters>
<metadata> ::= <metadata-chars> | <metadata-chars> "." <metadata>
<non-negative> ::= <positive> | <zero>
<metadata-chars> ::= <letter> | "_" | <metadata-chars> <digit> | <metadata-chars> <letter> | <metadata-chars> "_"
<alphanums> ::= <alphanum> | <alphanums> <alphanum>
<letters> ::= <letter> | <letters> <letter>
<alphanum> ::= <letter> | <digit>
<positive> ::= <pos-digit> | <positive> <digit>
<pos-digit> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<zero> ::= "0"
```
