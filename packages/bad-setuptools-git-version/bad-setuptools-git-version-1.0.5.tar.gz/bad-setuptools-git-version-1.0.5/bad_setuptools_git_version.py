"""Methods to extract version information from a git repository."""
import subprocess
import collections


def _get_command_output(command):
    """ Compatibility wrapper for grabbing process output across multiple python versions. """

    # python2.7 versions lack _get_command_output, so we'll emulate it by using check_output
    # and ignoring the process' return status
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    if isinstance(output, bytes):
        output = output.decode("utf-8")

    return output.rstrip('\r\n')


def get_tag():
    """Return the last tag for the git repository reachable from HEAD."""
    return _get_command_output(['git', 'describe', 'HEAD', '--abbrev=0', '--tags'])


def get_count_commit():
    return _get_command_output(['git', 'rev-list', 'HEAD', '--count'])


def get_version(template="{tag}.{cc}", starting_version="0.1.0"):
    """
    Return the full git version using the given template. If there are no annotated tags, the version specified by
    starting_version will be used. If HEAD is at the tag, the version will be the tag itself. If there are commits ahead
    of the tag, the first 8 characters of the sha of the HEAD commit will be included.

    In all of the above cases, if the working tree is also dirty or contains untracked files, a "+dirty" suffix will be
    appended to the version.

    Args:
        template: the string format template to use. It can use these keys:
            {tag}: the tag from the git repository
            {sha}: first 8 characters of the sha key of HEAD
        starting_version: the starting version to use if there are no existing tags.

    Returns:
        the formatted version based on tags in the git repository.

    """

    tag = get_tag()
    cc = get_count_commit()
    if len(tag) == 0:
        version = starting_version
    else:
        version = template.format(tag=tag, cc=cc)

    return version


def validate_version_config(dist, _, config):
    """Validate the `version_config` keyword in a client setup.py script."""
    if not isinstance(config, collections.Mapping):
        raise TypeError("Config should be a dictionary with `version_format` and `starting_version` keys.")

    if "starting_version" not in config:
        starting_version = "0.1.0"
    else:
        starting_version = config["starting_version"]

    if "version_format" not in config:
        template = "{tag}.{cc}"
    else:
        template = config["version_format"]

    dist.metadata.version = get_version(template, starting_version)


# explicitly define the outward facing API of this module
__all__ = [
    get_tag.__name__,
    get_version.__name__,
    validate_version_config.__name__,
]
