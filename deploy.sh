#!/bin/bash

# BashScriptPlatform
################################################################################
function init () {
    if [ "$(uname)" == "Darwin" ]; then
        cd /tmp

        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

        brew update

        curl -o deploy.py "https://raw.githubusercontent.com/julwrites/tools/master/deploy.py"

        brew install python@2
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        cd /tmp

        if [ -n "$(command -v yum)" ]; then

            sudo yum clean all

            # Skip installing Python, Debian distros have it natively
        elif [ -n "$(command -v apt-get)" ]; then
            sudo killall dpkg

            sudo apt-get -y install python2.7
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

    sudo chmod 777 deploy.py

    python deploy.py

    sudo rm -rf deploy.py
}
################################################################################

deploy

read -p "Press any key to continue..."

exit