from utils import *

################################################################################


def bootstrap_os():
    if windows():
        from os import windows
        windows.bootstrap()
    elif darwin():
        from os import darwin
        darwin.bootstrap()
    elif debian_dist():
        from os import debian
        debian.bootstrap()
    elif redhat_dist():
        from os import redhat
        redhat.bootstrap()
