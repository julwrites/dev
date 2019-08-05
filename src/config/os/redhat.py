################################################################################

from common import *

################################################################################

RedHat = [
    # Dev Tools
    'code',
    # Programming Tools
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

from utils import *

################################################################################


def bootstrap():
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
    run('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc')
    run('sudo echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
        )
    run('sudo yum check-update')


def packages():
    return merge(Common, RedHat)
