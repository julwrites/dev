################################################################################

from common import *

################################################################################

Windows = [
    # Dev Tools
    'vscode',
    'visualstudio2019buildtools',
    'visualstudio2019-workload-vctools',
    # Vim Tools
    'fzf,
    # Programming Tools
    'python3',
    'pip',
    'llvm',
    'activeperl',
    'nodejs',
    'ruby',
    'flutter',
    'dart-sdk',
    # Common Tools
    '7zip.install',
    'miktex',
    'synctrayzor',
    # Fonts
    'Hasklig',
    'FiraCode'
]
################################################################################

from utils import *

################################################################################


def bootstrap():
    run('@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString(\'https://chocolatey.org/install.ps1\'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"'
        )
    run('choco upgrade chocolatey')
    run('choco upgrade -y')


def packages():
    return merge(Common, Windows)
