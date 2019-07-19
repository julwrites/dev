import platform
import webbrowser
import subprocess
import os
import shutil
import requests
import zipfile

################################################################################

# Python specific tools
Pip = ['conan', 'cmake', 'ninja', 'lizard', 'pynvim', 'jedi']

Npm = ['@vue/cli']

Common = [
    # Dev Tools
    'git',
    'nodejs',
    # Common Tools
    'slack',
    'neovim'
]

Windows = [
    # Dev Tools
    'pip'
    'python3',
    'visualstudio2019buildtools',
    'visualstudio2019-workload-vctools',
    'llvm',
    'vscode',
    'activeperl',
    'nodejs',
    'ruby'
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
    'llvm',
    'node',
    "ruby"
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
    'make',
    'gcc',
    'clang-7',
    'lldb-7',
    'lld-7',
    'visual-studio-code',
    'nodejs',
    'ruby-full'
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
    'python-pip',
    'devtoolset-7',
    'llvm-toolset-7',
    'nodejs',
    'ruby'
]

################################################################################


def match(platform, candidate):
    return platform.find(candidate) != -1


def windows():
    return 'Windows' in platform.uname()[0]


def darwin():
    return 'Darwin' in platform.uname()[0]


def linux():
    return 'Linux' in platform.uname()[0]


def debian():
    return linux() and match(platform.linux_distribution()[0], 'Debian')


def ubuntu():
    return linux() and match(platform.linux_distribution()[0], 'Ubuntu')


def debian_dist():
    return debian() or ubuntu()


def redhat():
    return linux() and match(platform.linux_distribution()[0], 'Red Hat')


def centos():
    return linux() and match(platform.linux_distribution()[0], 'CentOS')


def redhat_dist():
    return redhat() or centos()


def run(cmd):
    print('calling: ' + cmd)
    return subprocess.call(cmd, shell=True) == 0


def copy_folder(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)

    shutil.copytree(src, dst)


def copy_file(src, dst):
    if os.path.exists(dst):
        os.remove(dst)

    shutil.copy(src, dst)


def script_path():
    return os.path.dirname(os.path.realpath(__file__))


################################################################################


def init():
    if windows():
        run('choco upgrade -y')
    elif darwin():
        run('xcode-select --install')

        run('brew tap caskroom/cask')
        run('brew tap caskroom/fonts')
    elif debian_dist():
        run('wget https://packages.microsoft.com/keys/microsoft.asc')
        run('cat microsoft.asc | gpg --dearmor > microsoft.gpg')
        run('sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/'
            )
        run('sudo sh -c \'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list\''
            )
        run('sudo apt-get install apt-transport-https')
        run('sudo apt-get update -y')
    elif redhat_dist():
        if redhat():
            run('sudo yum install')
            run('sudo yum-config-manager --enable rhel-server-rhscl-7-rpms')
            run('sudo subscription-manager repos --enable rhel-7-server-optional-rpms'
                )
            run('sudo subscription-manager repos --enable rhel-server-rhscl-7-rpms'
                )
            run('wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm'
                )
            run('sudo yum install epel-release-latest-7.noarch.rpm')
            run('sudo yum install epel-release')
        if centos():
            run('sudo yum -y install centos-release-scl')
            run('sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm'
                )

        run('sudo yum -y gcc-c++ make')
        run('curl -sL https://rpm.nodesource.com/setup_10.x | sudo -E bash -')
        run('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc'
            )
        run('sudo echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
            )
        run('sudo yum check-update')


Session = {"installed": [], "updated": [], "failed": []}


def merge(orig, add):
    orig.extend([p for p in add if p not in orig])
    return orig


def pkgmgr_pkg():
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


def python_pkg():
    select = Pip

    return select


def node_pkg():
    select = Npm

    return select


def pkgmgr_cmd():
    install_cmd = ''
    update_cmd = ''
    post_cmd = ''

    if windows():
        install_cmd = 'choco install {} -y'
        check_cmd = 'choco list -lo {}'
        update_cmd = 'choco upgrade {} -y'
    elif darwin():
        install_cmd = 'brew {} install {}'
        check_cmd = 'brew {} list {}'
        update_cmd = 'brew upgrade {}'
        post_cmd = 'brew link --overwrite {}'
    elif debian_dist():
        install_cmd = 'sudo apt-get install {} -y -q'
        check_cmd = 'sudo apt-cache show {}'
        update_cmd = 'sudo apt-get update {} -y -q'
    elif redhat_dist():
        install_cmd = 'sudo yum -y install {}'
        check_cmd = 'sudo yum list installed {}'
        update_cmd = 'sudo yum -y upgrade {}'

    return install_cmd, check_cmd, update_cmd, post_cmd


def python_cmd():
    pkg_cmd = 'pip'
    if not windows():
        pkg_cmd = 'sudo pip'
    install_cmd = pkg_cmd + ' install {} -q'
    check_cmd = pkg_cmd + ' list {} -q'
    update_cmd = pkg_cmd + ' install {} -q'
    post_cmd = ''

    return install_cmd, check_cmd, update_cmd, post_cmd


def node_cmd():
    pkg_cmd = 'npm'
    if not windows():
        pkg_cmd = 'sudo npm'
    install_cmd = pkg_cmd + ' install {} -g'
    check_cmd = pkg_cmd + ' list {} -g'
    update_cmd = pkg_cmd + ' update {} -g'
    post_cmd = ''

    return install_cmd, check_cmd, update_cmd, post_cmd


def format_install(format_cmd, pkg):
    if darwin():
        return format_cmd.format('cask' if (pkg in DarwinCask) else '', pkg)
    else:
        return format_cmd.format(pkg)


def format_check(check_cmd, pkg):
    if darwin():
        return check_cmd.format('cask' if pkg in DarwinCask else '', pkg)
    else:
        return check_cmd.format(pkg)


def install(install_cmd, check_cmd, update_cmd, post_cmd, packages):
    for pkg in packages:
        if run(format_check(check_cmd, pkg)):
            run(update_cmd.format(pkg))
            Session['updated'].append(pkg)
        elif run(format_install(install_cmd, pkg)):
            if pkg in Session['failed']:
                Session['failed'].remove(pkg)
            Session['installed'].append(pkg)
        elif not pkg in Session['failed']:
            Session['failed'].append(pkg)

    for pkg in packages:
        run(post_cmd.format(pkg))


def retrieve(url):
    zip_dst = os.path.join(script_path(), os.path.split(url)[1])

    req = requests.get(url)

    with open(zip_dst, "wb") as out:
        out.write(req.content)

    with zipfile.ZipFile(zip_dst, 'r') as zip_ref:
        zip_ref.extractall(script_path())

    return os.path.join(script_path(), "dev-master")


def copy_config():
    location = retrieve('https://github.com/julwrites/dev/archive/master.zip')

    src = os.path.join(location, 'nvim')

    if windows():
        dest = os.path.join(os.getenv('LOCALAPPDATA'), 'nvim')
    else:
        dest = '~/.config/nvim'

    copy_folder(src, dest)


def deploy():
    init()

    install_cmd, check_cmd, update_cmd, post_cmd = pkgmgr_cmd()
    packages = pkgmgr_pkg()
    install(install_cmd, check_cmd, update_cmd, post_cmd, packages)

    install_cmd, check_cmd, update_cmd, post_cmd = python_cmd()
    packages = python_pkg()
    install(install_cmd, check_cmd, update_cmd, post_cmd, packages)

    install_cmd, check_cmd, update_cmd, post_cmd = node_cmd()
    packages = node_pkg()
    install(install_cmd, check_cmd, update_cmd, post_cmd, packages)


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

deploy()

copy_config()

report()
