#!/usr/bin/env bash

RETROPIE_ROMS="RetroPie/roms"
RETROPIE_INSTALL="/opt/retropie"
TEST=""


# FIXME delete
function install_systems() {
    ## copy the file with the systems (we are going to create a new one)

    $SUDO cp /etc/emulationstation/es_systems.cfg $RETROPIE_INSTALL/configs/all/emulationstation/es_systems.cfg$TEST

    LAST_SYSTEM=$(cat $RETROPIE_INSTALL/configs/all/emulationstation/es_systems.cfg$TEST | grep -n "</system>" | cut -f1 -d: | tail -n 1)
    echo "$LAST_SYSTEM"
    
    AINDUSTRIOSA_SYSTEMS=" \
  <system>\n \
    <name>aindustriosa</name>\n \
    <fullname>A industriosa Games</fullname>\n \
    <path>$ROMPATH/aindustriosa</path>\n \
    <extension>.7z .nes .zip .7Z .NES .ZIP</extension>\n \
    <command>$RETROPIE_INSTALL/supplementary/runcommand/runcommand.sh 0 _SYS_ nes %ROM%</command>\n \
    <platform>favs</platform>\n \
    <theme>aindustriosa</theme>\n \
  </system>\n \
\n \
  <system>\n \
    <name>aindustriosalibgdx</name>\n \
    <fullname>A industriosa Games for LIBGDX</fullname>\n \
    <path>$ROMPATH/aindustriosa</path>\n \
    <extension>.sh</extension>\n \
    <command>%ROM%</command>\n \
    <platform>favs</platform>\n \
    <theme>aindustriosa_libgdx</theme>\n \
  </system>\n"

    $SUDO sed -i "$LAST_SYSTEM a $AINDUSTRIOSA_SYSTEMS" $RETROPIE_INSTALL/configs/all/emulationstation/es_systems.cfg$TEST

    # copy the themes if they dont exist
    if [[ ! -e $RETROPIE_INSTALL/configs/all/emulationstation/themes ]]; then
	$SUDO cp -r /etc/emulationstation/themes $RETROPIE_INSTALL/configs/all/emulationstation/themes

    else
	echo "Folder (themes) already exists"
    fi

    # copy the aindustriosa themes to the themes folder
    MYPATH=$(dirname "$0")

    $SUDO cp -r $MYPATH/themes/* /etc/emulationstation/themes $RETROPIE_INSTALL/configs/all/emulationstation/themes/
    
}

SUDO=''

# check if we are running as root
if [ $EUID -ne 0 ]; then
    # user is not root, running with sudo
    SUDO="sudo"
fi

function install_env() {
    $SUDO apt-get install virtualenv openjdk-8-jdk python-dev python3-http-parser
    MYPATH=$(dirname "$0")

    # using a virtual environment
    virtualenv -p python2 venv

    $MYPATH/venv/bin/pip install--upgrade pip
    
    $MYPATH/venv/bin/pip install pyautogui pyudev xlib psutil
}

function install_scripts() {

    MYPATH=$(dirname "$0")

    $SUDO chmod +x $MYPATH/scripts/run_libgdx_game.sh
    $SUDO chmod +x $MYPATH/scripts/joy2libgdxkey.py

    MYREALPATH=$(realpath $MYPATH)
        
    $SUDO cp $MYPATH/scripts/* $RETROPIE_INSTALL/supplementary/runcommand/

    $SUDO sed -i "1 s~^.*$~#! $MYREALPATH/venv/bin/python~" $RETROPIE_INSTALL/supplementary/runcommand/joy2libgdxkey.py
    
}

function install_server() {

    MYUSER=$(whoami)

    MYPATH=$(dirname "$0")
    MYREALPATH=$(realpath $MYPATH)

    SERVICE_FILE_PATH=$MYREALPATH/server/retrodiosa.service

    SERVICE_FILE="[Unit]\nDescription=Servidor RetroDiosa\nAfter=network.target\n\n[Service]\nType=simple\nUser=$MYUSER\nWorkingDirectory=$HOME\nExecStart=$MYREALPATH/server/servidor_retrodiosa.py 8000 $ROMPATH/aindustriosa $MYREALPATH/server/\nRestart=on-failure\n# Other Restart options: or always, on-abort, etc \n\n[Install]\nWantedBy=multi-user.target"

    echo -e $SERVICE_FILE > $MYREALPATH/server/retrodiosa.service

    chmod +x $MYREALPATH/server/servidor_retrodiosa.py

    $SUDO cp $MYREALPATH/server/retrodiosa.service /etc/systemd/system/

    $SUDO systemctl enable retrodiosa
    $SUDO systemctl start retrodiosa
    
    # TODO
}

echo "$SUDO"

# find the path to retropie roms
ROMPATH=$(find ~ -name "roms" | grep -FzZ $RETROPIE_ROMS)     

echo "$ROMPATH"

# create the folder to store aindustriosa roms
if [[ ! -e $ROMPATH/aindustriosa ]]; then
    mkdir $ROMPATH/aindustriosa

else
    echo "Folder already exists"
fi

# add the aindustriosa systems after the last original one
install_systems
install_env
install_scripts
install_server

