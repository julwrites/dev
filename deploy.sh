#!/bin/bash

# BashScriptAdmin
################################################################################
function admin () {
    echo "$(whoami)"

    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

    if [ "$UID" -ne 0 ]; then
        cd $DIR && exec sudo ./deploy.sh
    fi
}
################################################################################

# BashScriptPlatform
################################################################################
function init () {
    if [ "$(uname)" == "Darwin" ]; then
        cd /tmp

        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

        brew update

        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/julwrites/tools/master/deploy.py)"

        brew install python@2
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        admin

        cd /tmp

        if [ -n "$(command -v yum)" ]; then

            yum clean all

            yum upgrade -y

            # Skip installing Python, Debian distros have it natively
        elif [ -n "$(command -v apt-get)" ]; then
            killall dpkg

            apt-get upgrade -y --force-yes -q

            apt-get -y install python2.7
        else
            echo Could not find package manager
        fi

        wget -O deploy.py "https://github.com/julwrites/tools/raw/master/deploy.py"
    else
        echo Platform not recognized
    fi
}
################################################################################

# BashScriptDeploy
################################################################################
function deploy () {
    init

    chmod 777 deploy.py

    python deploy.py

    rm -rf deploy.py
}
################################################################################

deploy

read -p "Press any key to continue..."

exit