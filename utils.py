import platform
import webbrowser
import subprocess
import os
import shutil
import requests
import zipfile

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


def copy_folder(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)

    shutil.copytree(src, dst)


def copy_file(src, dst):
    if os.path.exists(dst):
        os.remove(dst)

    shutil.copy(src, dst)


def script_path():
    return os.path.dirname(os.path.realpath(__file__))


################################################################################
