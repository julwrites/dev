import platform
import webbrowser
import subprocess

Common = ['git', 'vscode', 'cmake', 'conan', 'nodejs']
Windows = [
    'python3', 'cmdermini', 'neovim', 'llvm'
]
Darwin = ['python3', 'llvm']
Debian = ['python3.6', 'python3-pip', 'clang-7', 'lldb-7', 'lld-7']
RedHat = [
    'gettext-devel', 'openssl-devel', 'perl-CPAN', 'perl-devel', 'zlib-devel',
    'python36', 'devtoolset-7', 'llvm-toolset-7'
]


def windows():
    return platform.uname()[0] in ['Windows']


def darwin():
    return platform.uname()[0] in ['Darwin']


def linux():
    return platform.uname()[0] in ['Linux']


def debian():
    return linux() and platform.linux_distribution()[0] in ['Debian']


def ubuntu():
    return linux() and platform.linux_distribution()[0] in ['Ubuntu']


def debian_dist():
    return linux() and platform.linux_distribution()[0] in ['Debian', 'Ubuntu']


def redhat():
    return linux() and platform.linux_distribution()[0] in ['RedHat']


def centos():
    return linux() and platform.linux_distribution()[0] in ['CentOS']


def redhat_dist():
    return linux() and platform.linux_distribution()[0] in ['RedHat', 'CentOS']


def run(cmd):
    return subprocess.call(cmd, shell=True)


def init():
    format_cmd = ''

    if windows():
        format_cmd = 'choco install {} -y'
    elif darwin():
        format_cmd = 'brew install {}'
    elif debian_dist():
        format_cmd = 'apt-get install {} -y -qq'
    elif redhat_dist():
        if redhat():
            run('yum-config-manager --enable rhel-server-rhscl-7-rpms')
            run('subscription-manager repos --enable rhel-7-server-optional-rpms'
                )
            run('subscription-manager repos --enable rhel-server-rhscl-7-rpms')

        format_cmd = 'yum -y install {}'

    return format_cmd


def package():
    package = Common

    if windows():
        package.extend(Windows)
    elif darwin():
        package.extend(Darwin)
    elif debian_dist():
        package.extend(Debian)
    elif redhat_dist():
        if redhat():
            package = ['epel-release'].extend(package)
        elif centos():
            package = [
                'centos-release-scl',
                'https://centos7.iuscommunity.org/ius-release.rpm'
            ].extend(package)
        package.extend(RedHat)

    return package


def install():
    format_cmd = init()

    for pkg in package():
        for i in range(3):
            if run(format_cmd.format(pkg)) == 0:
                break


# webbrowser.open_new('https://tehj.org')
install()