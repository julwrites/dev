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
        cd /usr/tmp

        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

        brew install python@2
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        admin

        cd /usr/tmp

        if [ -n "$(command -v yum)" ]; then
            yum upgrade -y

            # Skip installing Python, Debian distros have it natively

            yum -y install curl
        elif [ -n "$(command -v apt-get)" ]; then
            apt-get upgrade -y --force-yes -qq

            apt-get -y install python2.7

            apt-get -y install curl
        else
            echo Could not find package manager
        fi
    else
        echo Platform not recognized
    fi
}
################################################################################

# BashScriptDeploy
################################################################################
function deploy () {
    cd /usr/tmp

    curl -o deploy.py "https://raw.githubusercontent.com/julwrites/tools/master/deploy.py"

    chmod 777 deploy.py

    python deploy.py

    rm -rf deploy.py
}
################################################################################

init
deploy

read -p "Press any key to continue..."

exit