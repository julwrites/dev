################################################################################

from common import *

################################################################################

Darwin = [
    # Programming Tools
    'python3',
    'llvm',
    'node',
    'ruby',
    'flutter',
    'dart',
    # Vim Tools
    'fzf'
]

DarwinCask = [
    # Common Tools
    'slack',
    # Dev Tools
    'visual-studio-code',
    # Fonts
    'font-hasklig',
    'font-fira-code',
    'font-iosevka'
]

################################################################################

from utils import *

################################################################################


def bootstrap():
    run('xcode-select --install')

    run('brew tap caskroom/cask')
    run('brew tap caskroom/fonts')


def packages():
    return merge(merge(Common, Darwin), DarwinCask)
