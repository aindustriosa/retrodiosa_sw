# Software for the Retrodiosa

## Introduction

This script install additional scripts and themes for the retrodiosa arcade machine, a flamboyant arcade made in A Industriosa.

The most important feature is that it allows the execution of libgdx games in an arcade machine with retropie.

In the tv_control directory you can find an Arduino sketch and a python script for controlling the Retrodiosa's TV by directly interfacing with the IR sensor board in the TV.

## Features

- Custom themes for A Industriosa
- Integration of games made with LIBGDX (playable directly from  emulation station). This only works for non-arm architectures
- HTTP server for uploading games to the arcade machine (http://<your-server-ip>:8000)

More detailed instructions (Spanish) can be found in https://github.com/aindustriosa/retrodiosa_docs/blob/master/modificaciones_retropie.md


## Installation

1) Install retroach following the instructions https://retropie.org.uk/docs/Debian/

2) Execute the script

```
./install_script.sh
```

The script assumes the directory of installation is /opt/retropie. If this is not in the case, change the RETROPIE_INSTALL parameter (aprox. line 4.)

## Known Issues

Currently, only x64 architectures are supported.

Installation script only tested in debian-like distributions

<b>Proxecto patrocinado por Xunta de Galicia e Amtega Axencia para a Modernización Tecnolóxica</b>
