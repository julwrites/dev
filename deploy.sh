#!/bin/bash

# BashScriptBanner
################################################################################
function banner () {
    echo "-----------------------------------------------------------------------------------"
    echo "      _____                                  ______               ______)          "
    echo "     (, /      /)           ,               (, /    )            (, /        /)    "
    echo "       /      // _   _ __    _/_  _  _        /    /  _ _ _        /  ______//  _  "
    echo "   ___/__(_(_(/_ (_(/ / (__(_(___(/_/_)_    _/___ /__(/_(/__    ) /  (_)(_)(/_ /_)_"
    echo " /   /                                    (_/___ /             (_/                 "
    echo "(__ /                                                                              "
    echo "-----------------------------------------------------------------------------------"
}
################################################################################

# BashScriptPlatform
################################################################################
function init () {
    if [ "$(uname)" == "Darwin" ]; then
        cd /tmp

        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

        brew update

        sudo rm -rf deploy.py

        curl -o deploy.py "https://raw.githubusercontent.com/julwrites/dev/master/deploy.py"

        brew upgrade

        brew install python3
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        cd /tmp

        if [ -n "$(command -v yum)" ]; then

            sudo yum clean all

            sudo subscription-manager attach --auto

            sudo yum install python3

            sudo yum install -y gcc openssl-devel bzip2-devel
        elif [ -n "$(command -v apt-get)" ]; then
            sudo killall dpkg

            sudo apt-get -y install python2.7
        else
            echo Could not find package manager
        fi

        sudo rm -rf deploy.py

        wget -O deploy.py "https://raw.githubusercontent.com/julwrites/dev/master/deploy.py"

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

    if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        if [ -n "$(command -v python3)" ]; then
            python3 deploy.py
            python3 -m pip install requests
        elif [ -n "$(command -v python)" ]; then
            python deploy.py
            python -m pip install requests
        else
            echo Could not find python 3
        fi
    fi

    sudo rm -rf deploy.py
}
################################################################################

banner

deploy

read -p "Press any key to continue..."

exit