#!/bin/bash
set -e

# Default release targets "master"
RELEASE="master"
# Default requirements
REQUIREMENTS="default.txt"

# Command help
function usage()
{
    echo "'recalbox-manager' installer"
    echo ""
    echo "./install.sh"
    echo "    -h --help"
    echo ""
    echo "    --release=$RELEASE"
    echo "      Optionnal, force a specific release instead of latest version ($RELEASE)"
    echo ""
    echo "    --compatible"
    echo "      Optionnal, use requirements compatible with Recalbox 3.2.11"
    echo ""
}

# Checking given arguments
while [ "$1" != "" ]; do
    PARAM=`echo $1 | awk -F= '{print $1}'`
    VALUE=`echo $1 | awk -F= '{print $2}'`
    case $PARAM in
        -h | --help)
            usage
            exit
            ;;
        --release)
            RELEASE=$VALUE
            ;;
        --compatible)
            REQUIREMENTS="default_3-2-0.txt"
            ;;
        *)
            echo "ERROR: unknown parameter \"$PARAM\""
            usage
            exit 1
            ;;
    esac
    shift
done


echo "* Installing pip and virtualenv"
python -m ensurepip
pip install virtualenv
echo

echo "* Downloading release $RELEASE"
wget https://github.com/sveetch/recalbox-manager/archive/$RELEASE.zip
unzip $RELEASE.zip
echo

echo "* Initialize virtual environment for project"
cd recalbox-manager-$RELEASE/
virtualenv --system-site-packages .
echo

echo "* Installing project requirements"
bin/pip install -r pip-requirements/$REQUIREMENTS
echo

echo "* Initialize project"
bin/python manage.py migrate
echo

echo
echo "DONE!"
echo "Go into directory 'recalbox-manager-$RELEASE/' and you can start the server with the following command:"
echo
echo "bin/python manage.py runserver 0.0.0.0:80 --settings=project.settings_production --noreload"
echo