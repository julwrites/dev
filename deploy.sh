#!bin/bash

# BashScriptAdmin
################################################################################
function admin () {
    echo "$(whoami)"

    [ "$UID" -eq 0 ] || exec sudo "$0" "$@"
}
################################################################################

# BashScriptPlatform
################################################################################
function init () {
    cd /usr/tmp

    if [ "$(uname)" == "Darwin" ]; then
        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

        brew install python@2
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        admin

        if [ -n "$(command -v yum)" ]; then
            yum upgrade -y

            # Skip installing Python, Debian distros have it natively

            yum -y install curl
        elif [ -n "$(command -v apt-get)" ]; then
            apt-get upgrade -y --force-yes -qq

            apt-get -y install python2.7

            apt-get -y install curl
        fi
    fi


    echo Platform not recognized
}
################################################################################

# BashScriptDeploy
################################################################################
function deploy () {
    cd /usr/tmp

    curl https://github.com/julwrites/deploy.py deploy.py

    python deploy.py

    rm -rf deploy.py
}
################################################################################

init
deploy

read -p "Press any key to continue..."

exit