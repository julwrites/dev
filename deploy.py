import platform
import webbrowser
import subprocess

################################################################################

Common = [
    # Dev Tools
    'git',
    'cmake',
    'conan',
    'nodejs',
    # Common Tools
    'slack',
    'neovim'
]

Windows = [
    # Dev Tools
    'python3',
    'visualstudio2017buildtools',
    'visualstudio2017-workload-vctools',
    'llvm',
    'vscode',
    'activeperl',
    'xamarin',
    # Common Tools
    '7zip.install',
    'cmdermini',
    'miktex',
    'synctrayzor'
    # Fonts
    'Hasklig',
    'FiraCode'
]

Darwin = [
    # Dev Tools
    'python3',
    'llvm'
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

Debian = [
    # Dev Tools
    'python3.6',
    'python3-pip',
    'clang-7',
    'lldb-7',
    'lld-7',
    'code',
    # Fonts
    'fonts-firacode',
    'fonts-iosevka',
    'fonts-hasklig'
]

RedHat = [
    # Dev Tools
    'code',
    'gettext-devel',
    'openssl-devel',
    'perl-CPAN',
    'perl-devel',
    'zlib-devel',
    'python36',
    'devtoolset-7',
    'llvm-toolset-7'
]

################################################################################


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


################################################################################


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
        run('wget https://packages.microsoft.com/keys/microsoft.asc')
        run('cat microsoft.asc | gpg --dearmor > microsoft.gpg')
        run('sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/'
            )
        run('sudo sh -c \'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list\''
            )
        run('sudo apt-get install apt-transport-https')
        run('sudo apt-get update -y')

        format_cmd = 'sudo apt-get install {} -y -q'
        update_cmd = 'sudo apt-get update {} -y -q'
    elif redhat_dist():
        if redhat():
            run('sudo yum-config-manager --enable rhel-server-rhscl-7-rpms')
            run('sudo subscription-manager repos --enable rhel-7-server-optional-rpms'
                )
            run('sudo subscription-manager repos --enable rhel-server-rhscl-7-rpms'
                )
            run('sudo yum install epel-release')
        if centos():
            run('sudo yum -y install centos-release-scl')
            run('sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm'
                )

        run('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc'
            )
        run('sudo echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
            )
        run('sudo yum update -y')

        format_cmd = 'sudo yum -y install {}'
        format_cmd = 'sudo yum -y upgrade {}'

    return format_cmd, update_cmd, post_cmd


Session = {"installed": [], "updated": [], "failed": []}


def merge(orig, add):
    return orig + [p for p in add if p not in orig]


def packages():
    select = Common

    if windows():
        select = merge(select, Windows)
    elif darwin():
        select = merge(select, Darwin)
        select = merge(select, DarwinCask)
    elif debian_dist():
        select = merge(select, Debian)
    elif redhat_dist():
        select = merge(select, RedHat)

    return select


def exists(pkg):
    if windows():
        return run('choco list -lo {}'.format(pkg))
    elif darwin():
        return run('brew {} list {}'.format(
            'cask' if pkg in DarwinCask else '', pkg))
    elif debian_dist():
        return run('sudo apt-cache show {}'.format(pkg))
    elif redhat_dist():
        return run('sudo yum list installed {}'.format(pkg))

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


################################################################################


def report():
    print('\n\t+\t'.join(['Installed:'] + Session['installed']))
    print('\n\t^\t'.join(['Updated:'] + Session['updated']))
    print('\n\t!\t'.join(['Failed'] + Session['failed']))

    if darwin():
        print('Please take note that XCode has to be installed separately')

    print("""
 -----------------------------------------------------------------------------------
       _____                                  ______               ______)          
      (, /      /)           ,               (, /    )            (, /        /)    
        /      // _   _ __    _/_  _  _        /    /  _ _ _        /  ______//  _  
    ___/__(_(_(/_ (_(/ / (__(_(___(/_/_)_    _/___ /__(/_(/__    ) /  (_)(_)(/_ /_)_
  /   /                                    (_/___ /             (_/                 
 (__ /                                                                              
 -----------------------------------------------------------------------------------
    """)

    print("""
        ## Mantra
        1. Development Tools are an essential part of any workflow
        2. Developers should struggle with code, not tools
        3. Good tools enable and enhance developers
    """)


################################################################################

install()

report()
