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

        pkgr=brew
        silent=''
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        admin

        if [ -n "$(command -v yum)" ]; then
            pkgr=yum

            $pkgr upgrade -y
        elif [ -n "$(command -v apt-get)" ]; then
            pkgr=apt-get

            $pkgr upgrade -y --force-yes -qq
        fi
        silent='-y'
    fi

    $pkgr $silent install curl
    $pkgr $silent install python

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

exit