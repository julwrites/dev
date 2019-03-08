import platform
import webbrowser
import subprocess

Common = ['git', 'cmake', 'conan', 'nodejs']
Windows = ['python3', 'vscode', 'cmdermini', 'neovim', 'llvm']
Darwin = ['python3', 'llvm']
DarwinCask = ['visual-studio-code']
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
    return subprocess.call(cmd, shell=True) == 0


def init():
    format_cmd = ''
    post_cmd = ''

    if windows():
        format_cmd = 'choco install {} -y'
    elif darwin():
        run('xcode-select --install')

        run('brew tap caskroom/cask')
        format_cmd = 'brew {} install {}'
        post_cmd = 'brew link {}'
    elif debian_dist():
        run('apt-get update -y')
        run('apt-get upgrade -y --force-yes -q')
        run('curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg')
        run('install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/')
        run('echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list')

        format_cmd = 'apt-get install {} -y -q'
    elif redhat_dist():
        if redhat():
            run('yum-config-manager --enable rhel-server-rhscl-7-rpms')
            run('subscription-manager repos --enable rhel-7-server-optional-rpms'
                )
            run('subscription-manager repos --enable rhel-server-rhscl-7-rpms')
            run('yum install epel-release')
        if centos():
            run('yum -y install centos-release-scl')
            run('yum -y install https://centos7.iuscommunity.org/ius-release.rpm')

        run('yum update -y')
        run('yum upgrade -y')
        run('rpm --import https://packages.microsoft.com/keys/microsoft.asc')
        run('echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo')

        format_cmd = 'yum -y install {}'

    return format_cmd, post_cmd


def packages():
    package = Common

    if windows():
        package.extend(Windows)
    elif darwin():
        package.extend(Darwin)
        package.extend(DarwinCask)
    elif debian_dist():
        package.extend(Debian)
    elif redhat_dist():
        package.extend(RedHat)

    return package

def exists(pkg):
    if windows():
        return False
    elif darwin():
        return run('brew list {}'.format(pkg))
    elif debian_dist():
        return run('apt-cache show {}'.format(pkg))
    elif redhat_dist():
        return run('yum list installed {}'.format(pkg))

    return False

def format_install(format_cmd, pkg):
    if darwin():
        return format_cmd.format('cask' if (pkg in DarwinCask) else '', pkg)
    else:
        return format_cmd.format(pkg)

def install():
    format_cmd, post_cmd = init()

    for pkg in packages():
        for i in range(3):
            if exist(pkg) or run(format_install(format_cmd, pkg)):
                break

    for pkg in packages():
        run(post_cmd.format(pkg))


# webbrowser.open_new('https://tehj.org')
install()