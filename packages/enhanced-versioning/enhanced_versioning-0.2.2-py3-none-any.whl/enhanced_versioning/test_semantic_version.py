import json

from pytest import raises

from enhanced_versioning.base_version import VersionError
from enhanced_versioning.semantic_version import SemanticVersion


def test_section_2():
    """Section 2: Major, minor, patch.

    A normal version number MUST take the form X.Y.Z where
    X, Y, and Z are non-negative integers. X is the major
    version, Y is the minor version, and Z is the patch
    version. Each element MUST increase numerically by
    increments of one. For instance: 1.9.0 -> 1.10.0 ->
    1.11.0.

    """

    assert str(SemanticVersion('0.0.0')) == '0.0.0'
    assert repr(SemanticVersion('0.0.0')) == "SemanticVersion('0.0.0')"
    assert str(SemanticVersion('999.999.999')) == '999.999.999'
    assert repr(SemanticVersion('999.999.999')) == "SemanticVersion('999.999.999')"

    with raises(VersionError):
        SemanticVersion('X.Y.Z')

    assert SemanticVersion('1.2.3').major == 1
    assert SemanticVersion('1.2.3').minor == 2
    assert SemanticVersion('1.2.3').patch == 3

    assert SemanticVersion('1.9.0') < SemanticVersion('1.10.0') < SemanticVersion('1.11.0')


def test_section_8():
    """Section 8.

    When a major version number is incremented, the minor
    version and patch version MUST be reset to zero. When a
    minor version number is incremented, the patch version
    MUST be reset to zero. For instance: 1.1.3 -> 2.0.0 and
    2.1.7 -> 2.2.0.

    """
    assert SemanticVersion('1.1.3') < SemanticVersion('2.0.0')
    assert SemanticVersion('2.1.7') < SemanticVersion('2.2.0')


def test_section_9():
    """Section 9: Pre-release version.

    A pre-release version MAY be denoted by appending a dash
    and a series of dot separated identifiers immediately
    following the patch version. Identifiers MUST be
    comprised of only ASCII alphanumerics and dash
    [0-9A-Za-z-]. Pre-release versions satisfy but have a
    lower precedence than the associated normal version.
    Examples: 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7,
    1.0.0-x.7.z.92.

    """

    assert SemanticVersion('1.0.0').pre_release == []
    assert SemanticVersion('1.0.0-alpha').pre_release == ['alpha']
    assert SemanticVersion('1.0.0-alpha.1').pre_release == ['alpha', 1]
    assert SemanticVersion('1.0.0-0.3.7').pre_release == [0, 3, 7]
    assert SemanticVersion('1.0.0-x.7.z.92').pre_release == ['x', 7, 'z', 92]
    assert str(SemanticVersion('1.0.0-x.7.z.92')) == '1.0.0-x.7.z.92'

    with raises(VersionError):
        SemanticVersion('1.0.0-')
    with raises(VersionError):
        SemanticVersion('1.0.0-$#%')

    assert SemanticVersion('1.0.0') > SemanticVersion('1.0.0-alpha')
    assert SemanticVersion('1.0.0-alpha') < SemanticVersion('1.0.0')


def test_section_10():
    """Section 10: Build version.

    A build version MAY be denoted by appending a plus sign
    and a series of dot separated identifiers immediately
    following the patch version or pre-release version.
    Identifiers MUST be comprised of only ASCII
    alphanumerics and dash [0-9A-Za-z-]. Build versions
    satisfy and have a higher precedence than the associated
    normal version. Examples: 1.0.0+build.1,
    1.3.7+build.11.e0f985a.

    """
    assert SemanticVersion('1.0.0+build.1').build == ['build', 1]
    assert SemanticVersion('1.0.0+build.11.e0f985a').build == ['build', 11, 'e0f985a']


def test_section_11():
    """Section 11: Precedence rules.

    Precedence MUST be calculated by separating the version
    into major, minor, patch, pre-release, and build
    identifiers in that order. Major, minor, and patch
    versions are always compared numerically. Pre-release
    and build version precedence MUST be determined by
    comparing each dot separated identifier as follows:
    identifiers consisting of only digits are compared
    numerically and identifiers with letters or dashes are
    compared lexically in ASCII sort order. Numeric
    identifiers always have lower precedence than
    non-numeric identifiers. Example: 1.0.0-alpha <
    1.0.0-alpha.1 < 1.0.0-beta.2 < 1.0.0-beta.11 <
    1.0.0-rc.1 < 1.0.0-rc.1+build.1 < 1.0.0 < 1.0.0+0.3.7 <
    1.3.7+build < 1.3.7+build.2.b8f12d7 <
    1.3.7+build.11.e0f985a.

    """
    presorted = [
        '1.0.0-alpha',
        '1.0.0-alpha.1',
        '1.0.0-beta.2',
        '1.0.0-beta.11',
        '1.0.0-rc.1',
        '1.0.0-rc.1+build.1',
        '1.0.0',
        '1.0.0+0.3.7',
        '1.3.7+build',
        '1.3.7+build.2.b8f12d7',
        '1.3.7+build.11.e0f985a',
    ]
    from random import shuffle
    randomized = list(presorted)
    shuffle(randomized)
    fixed = list(map(str, sorted(map(SemanticVersion, randomized))))
    assert fixed == presorted


def test_comparing_against_non_version():

    with raises(TypeError) as exception:
        SemanticVersion('1.0.0') > None
    assert 'cannot compare' in repr(exception.value)

    with raises(TypeError) as exception:
        SemanticVersion('1.0.0') == object()
    assert 'cannot compare' in repr(exception.value)


def test_json_serialization():
    """Test json serialization.

    """
    assert json.dumps(SemanticVersion('0.0.0')) == '"0.0.0"'
    assert json.dumps(SemanticVersion('999.999.999')) == '"999.999.999"'
    assert json.dumps(SemanticVersion('1.0.0-alpha')) == '"1.0.0-alpha"'
    assert json.dumps(SemanticVersion('1.0.0-alpha.1')) == '"1.0.0-alpha.1"'
    assert json.dumps(SemanticVersion('1.0.0+build.1')) == '"1.0.0+build.1"'
    assert json.dumps(SemanticVersion('1.0.0-alpha.beta-gamma+build.11.e0f985a')) == '"1.0.0-alpha.beta-gamma+build.11.e0f985a"'
