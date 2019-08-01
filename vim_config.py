import platform
import webbrowser
import subprocess
import os
import shutil
import requests
import zipfile
import * from utils

################################################################################

def checkout_config(dest):
    run('git clone https://github.com/julwrites/nvim ' + dest)


def scatter_config():
    src = os.path.join(script_path(), 'nvim')

    if windows():
        dest = os.path.join(os.getenv('LOCALAPPDATA'), 'nvim')
    else:
        dest = '~/.config/nvim'

    if not os.path.exists(dest):
        checkout_config(dest)

    os.chdir(dest)

    if not run('git pull'):
        os.chdir(script_path())
        distutils.dir_util.remove_tree(dest)
        checkout_config(dest)

    os.chdir(dest)

    if windows():
        dest = os.path.join(os.getenv('LOCALAPPDATA'), '..')
    else:
        dest = '~/.vim'

    distutils.dir_util.copy_file('.vimrc', )

    os.chdir(script_path())
