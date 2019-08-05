################################################################################

from common import *

################################################################################

Debian = [
    # Dev Tools
    'visual-studio-code',
    # Programming Tools
    'python3.6',
    'python3-pip',
    'make',
    'gcc',
    'clang-7',
    'lldb-7',
    'lld-7',
    'nodejs',
    'ruby-full',
    'flutter',
    'dart',
    # Fonts
    'fonts-firacode',
    'fonts-iosevka',
    'fonts-hasklig'
]

################################################################################

from utils import *

################################################################################


def bootstrap():
    run('wget https://packages.microsoft.com/keys/microsoft.asc')
    run('cat microsoft.asc | gpg --dearmor > microsoft.gpg')
    run('sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/'
        )
    run('sudo sh -c \'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list\''
        )
    run('sudo apt-get install apt-transport-https')
    run('sudo apt-get update -y')


def packages():
    return merge(Common, Debian)