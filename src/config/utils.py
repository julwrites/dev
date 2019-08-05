import platform
import subprocess

################################################################################


def match(platform, candidate):
    return platform.find(candidate) != -1


def windows():
    return 'Windows' in platform.uname()[0]


def darwin():
    return 'Darwin' in platform.uname()[0]


def linux():
    return 'Linux' in platform.uname()[0]


def debian():
    return linux() and match(platform.linux_distribution()[0], 'Debian')


def ubuntu():
    return linux() and match(platform.linux_distribution()[0], 'Ubuntu')


def debian_dist():
    return debian() or ubuntu()


def redhat():
    return linux() and match(platform.linux_distribution()[0], 'Red Hat')


def centos():
    return linux() and match(platform.linux_distribution()[0], 'CentOS')


def redhat_dist():
    return redhat() or centos()


def run(cmd):
    print('calling: ' + cmd)
    return subprocess.call(cmd, shell=True) == 0


def merge(orig, add):
    orig.extend([p for p in add if p not in orig])
    return orig
