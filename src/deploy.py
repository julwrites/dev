import platform
import webbrowser
import subprocess
import os
import shutil
import requests
import zipfile

################################################################################

from config.bootstrap import *
from config.packages import *
from config.utils import *

from config.pkg.node import *
from config.pkg.python import *
from config.pkg.ruby import *

################################################################################


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


def checkout_config(dest):
    run('git clone https://github.com/julwrites/nvim ' + dest)


def scatter_config():
    src = os.path.join(script_path(), 'nvim')

    if windows():
        dest = os.path.join(os.getenv('LOCALAPPDATA'), 'nvim')
    else:
        dest = '~/.config/nvim'

    if not os.path.exists(dest):
        checkout_config(dest)

    os.chdir(dest)

    if not run('git pull'):
        os.chdir(script_path())
        shutil.rmtree(dest)
        checkout_config(dest)

    os.chdir(dest)

    if windows():
        dest = os.path.join(os.getenv('LOCALAPPDATA'), '..')
    else:
        dest = '~/.vim'

    distutils.dir_util.copy_file('.vimrc', )

    os.chdir(script_path())


################################################################################


def init():
    bootstrap_os()


Session = {"installed": [], "updated": [], "failed": []}


def python_pkg():
    select = Pip

    return select


def ruby_pkg():
    select = Gem

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


def ruby_cmd():
    pkg_cmd = 'gem'
    if not windows():
        pkg_cmd = 'sudo gem'
    install_cmd = pkg_cmd + ' install {}'
    check_cmd = pkg_cmd + ' list {}'
    update_cmd = pkg_cmd + ' update {}'
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


def deploy():
    init()

    install_cmd, check_cmd, update_cmd, post_cmd = pkgmgr_cmd()
    packages = os_packages()
    install(install_cmd, check_cmd, update_cmd, post_cmd, packages)

    install_cmd, check_cmd, update_cmd, post_cmd = python_cmd()
    packages = python_pkg()
    install(install_cmd, check_cmd, update_cmd, post_cmd, packages)

    install_cmd, check_cmd, update_cmd, post_cmd = node_cmd()
    packages = node_pkg()
    install(install_cmd, check_cmd, update_cmd, post_cmd, packages)

    install_cmd, check_cmd, update_cmd, post_cmd = ruby_cmd()
    packages = ruby_pkg()
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

scatter_config()

report()
