from utils import *

################################################################################


def os_packages():
    if windows():
        from os import windows
        return windows.packages()
    elif darwin():
        from os import darwin
        return darwin.packages()
    elif debian_dist():
        from os import debian
        return debian.packages()
    elif redhat_dist():
        from os import redhat
        return redhat.packages()
