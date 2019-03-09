import platform
import webbrowser
import subprocess

Common = ['git', 'cmake', 'conan', 'nodejs', 'slack', 'neovim']
Windows = [
    'python3', '7zip.install', 'windows-sdk-10.0', 'llvm', 'vscode',
    'cmdermini', 'activeperl', 'miktex', 'xamarin', 'synctrayzor'
]
Darwin = ['python3', 'llvm']
DarwinCask = ['visual-studio-code']
Debian = ['python3.6', 'python3-pip', 'clang-7', 'lldb-7', 'lld-7']
DebianSnap = ['vscode']
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
    update_cmd = ''
    post_cmd = ''

    if windows():
        format_cmd = 'choco install {} -y'
        update_cmd = 'choco upgrade {} -y'
    elif darwin():
        run('xcode-select --install')

        run('brew tap caskroom/cask')

        format_cmd = 'brew {} install {}'
        update_cmd = 'brew upgrade {}'
        post_cmd = 'brew link --overwrite {}'
    elif debian_dist():
        run('curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg'
            )
        run('install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/'
            )
        run('echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
            )
        run('apt-get update -y')

        format_cmd = 'apt-get install {} -y -q'
        update_cmd = 'apt-get update {} -y -q'
    elif redhat_dist():
        if redhat():
            run('yum-config-manager --enable rhel-server-rhscl-7-rpms')
            run('subscription-manager repos --enable rhel-7-server-optional-rpms'
                )
            run('subscription-manager repos --enable rhel-server-rhscl-7-rpms')
            run('yum install epel-release')
        if centos():
            run('yum -y install centos-release-scl')
            run('yum -y install https://centos7.iuscommunity.org/ius-release.rpm'
                )

        run('rpm --import https://packages.microsoft.com/keys/microsoft.asc')
        run('echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
            )
        run('yum update -y')

        format_cmd = 'yum -y install {}'
        format_cmd = 'yum -y upgrade {}'

    return format_cmd, update_cmd, post_cmd


Session = {"installed": [], "updated": [], "failed": []}


def packages():
    select = Common

    if windows():
        select.extend(Windows)
    elif darwin():
        select.extend(Darwin)
        select.extend(DarwinCask)
    elif debian_dist():
        select.extend(Debian)
        select.extend(DebianSnap)
    elif redhat_dist():
        select.extend(RedHat)

    return select


def exists(pkg):
    if windows():
        return run('choco list -lo {}'.format(pkg))
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
    format_cmd, update_cmd, post_cmd = init()

    for pkg in packages():
        for i in range(3):
            if exists(pkg):
                run(update_cmd.format(pkg))
                Session['updated'].append(pkg)
                break
            elif run(format_install(format_cmd, pkg)):
                if pkg in Session['failed']:
                    Session['failed'].remove(pkg)
                Session['installed'].append(pkg)
                break
            elif not pkg in Session['failed']:
                Session['failed'].append(pkg)

    for pkg in packages():
        run(post_cmd.format(pkg))


def report():
    print('\n\t+\t'.join(['Installed:'] + Session['installed']))
    print('\n\t^\t'.join(['Updated:'] + Session['updated']))
    print('\n\t!\t'.join(['Failed'] + Session['failed']))

    if darwin():
        print('Please take note that XCode has to be installed separately')


install()

report()
