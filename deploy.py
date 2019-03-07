import platform
import webbrowser
import subprocess

Common = ['git', 'cmake', 'conan', 'nodejs']
Windows = ['python3', 'vscode', 'cmdermini', 'neovim', 'llvm']
Darwin = ['cask visual-studio-code', 'python3', 'llvm']
Debian = ['code', 'python3.6', 'python3-pip', 'clang-7', 'lldb-7', 'lld-7']
RedHat = [
    'code', 'gettext-devel', 'openssl-devel', 'perl-CPAN', 'perl-devel',
    'zlib-devel', 'python36', 'devtoolset-7', 'llvm-toolset-7'
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
        run('brew tap caskroom/cask')
        format_cmd = 'brew cask install {}'
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


def packages():
    package = Common

    if windows():
        package.extend(Windows)
    elif darwin():
        package.extend(Darwin)
    elif debian_dist():
        package.extend(Debian)
    elif redhat_dist():
        if redhat():
            prereq = ['epel-release']
            prereq.extend(package)
            package = prereq
        elif centos():
            prereq = [
                'centos-release-scl',
                'https://centos7.iuscommunity.org/ius-release.rpm'
            ]
            prereq.extend(package)
            package = prereq
        package.extend(RedHat)

    return package


def install():
    format_cmd = init()

    for pkg in packages():
        for i in range(3):
            if run(format_cmd.format(pkg)) == 0:
                break


# webbrowser.open_new('https://tehj.org')
install()