import subprocess
import collections


def _get_command_output(command):
    try:
        output = subprocess.check_output(command, shell=False)
    except subprocess.CalledProcessError as e:
        output = e.output

    if isinstance(output, bytes):
        output = output.decode("utf-8")

    return output.rstrip('\r\n')


def get_tag():
    return _get_command_output('git describe HEAD --abbrev=0 --tags')


def get_count_commit():
    return _get_command_output('git rev-list HEAD --count')


def get_version(template="{tag}.{cc}", starting_version="0.1.0", **kwargs):
    tag = get_tag()
    cc = get_count_commit()
    if len(tag) == 0:
        version = starting_version
    else:
        version = template.format(tag=tag, cc=cc)

    return version


def validate_version_config(dist, _, config):
    if not isinstance(config, collections.Mapping):
        raise TypeError("Config should be a dictionary with `version_format` and `starting_version` keys.")

    dist.metadata.version = get_version(**config)


# explicitly define the outward facing API of this module
__all__ = [
    get_tag.__name__,
    get_count_commit.__name__,
    get_version.__name__,
    validate_version_config.__name__,
]
