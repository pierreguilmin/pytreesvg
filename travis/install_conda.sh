#!/bin/bash

# Install and setup conda on a Travis CI Windows, Linux or macOS virtual machine.
#
# Warnings
# --------
# The Windows implementation is still not working.
#
# See Also
# --------
# - conda doc to use Travis CI: https://conda.io/docs/user-guide/tasks/use-conda-with-travis-ci.html
# - conda doc to install in silent mode on macOS: https://conda.io/docs/user-guide/install/macos.html#install-macos-silent
# - conda doc to install in silent mode on Windows: https://conda.io/docs/user-guide/install/windows.html#installing-in-silent-mode
# - chocolatey doc to install conda on Windows: https://chocolatey.org/packages/miniconda3


# exit the script if any command returns a non-zero status
set -e

if [[ "$TRAVIS_OS_NAME" == "osx" ]] || [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    # install Miniconda
    echo "Installing Miniconda..."
    if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
        DOWNLOAD_LINK="https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    else
        DOWNLOAD_LINK="https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    fi
    wget "$DOWNLOAD_LINK" -O miniconda3.sh
    bash miniconda3.sh -b -p "$HOME/miniconda3"
else
    echo "Not working yet, exiting..."
    exit 1

    # choco install miniconda3 --params="'/InstallationType:JustMe /AddToPath:1 /RegisterPython:0'"
    # choco install miniconda3 --params="'/AddToPath:1'"
    # refreshenv

    # echo "Installing Miniconda..."
    # Miniconda3-4.5.12-Windows-x86_64.exe  
    # wget -nv https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe -O miniconda3.exe
    # echo "Start..."
    # start /wait "" .\miniconda3.exe /InstallationType=JustMe /AddToPath=0 /RegisterPython=0 /S /D=.\
    # echo "Done!"
fi

# configure Miniconda
echo "Configuring Miniconda..."
conda config --set always_yes true --set changeps1 false

# update Miniconda
echo "Updating Miniconda..."
conda update conda
conda info -a
