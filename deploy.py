import platform
import webbrowser
import subprocess

Common = ['git', 'vscode', 'cmake', 'conan', 'nodejs']
Windows = ['python3', 'cmdermini', 'neovim', 'llvm']
Darwin = ['python3', 'llvm']
Debian = ['python3.6', 'python3-pip', 'clang-7', 'lldb-7', 'lld-7']
RedHat = [
    'gettext-devel', 'openssl-devel', 'perl-CPAN', 'perl-devel', 'zlib-devel',
    'python36', 'devtoolset-7', 'llvm-toolset-7'
]


def windows():
    return 'Windows' in platform.uname()[0]


def darwin():
    return 'Darwin' in platform.uname()[0]


def linux():
    return 'Linux' in platform.uname()[0]


def debian():
    return linux() and 'Debian' in platform.linux_distribution()[0]


def ubuntu():
    return linux() and 'Ubuntu' in platform.linux_distribution()[0]


def debian_dist():
    return linux() and (debian() or ubuntu())


def redhat():
    return linux() and 'Red Hat' in platform.linux_distribution()[0]


def centos():
    return linux() and 'CentOS' in platform.linux_distribution()[0]


def redhat_dist():
    return linux() and (redhat() or centos())


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