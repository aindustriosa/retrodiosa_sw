ROM=$1
JOYSTICK_MAPPINGS_FILE=$2
ROOTDIR="/opt/retropie"

echo "Joysticsk mappings $JOYSTICK_MAPPINGS_FILE"

function start_joy2key() {
    [[ "$JOYSTICK_MAPPINGS_FILE" -eq "" ]] && return
    # get the first joystick device (if not already set)
    if [[ -c "$__joy2key_dev" ]]; then
        JOY2KEY_DEV="$__joy2key_dev"
    else
        JOY2KEY_DEV="/dev/input/jsX"
    fi

    echo "Joysticsk DEV $JOY2KEY_DEV"

    # if joy2libgdxkey.py is installed run it with cursor keys for axis, and enter + tab for buttons 0 and 1
    if [[ -f "$ROOTDIR/supplementary/runcommand/joy2libgdxkey.py" && -n "$JOY2KEY_DEV" ]] && ! pgrep -f joy2libgdxkey.py >/dev/null; then

	echo "Launching program joylibgdx"
        # call joy2libgdxkey.py: arguments are curses capability names or hex values starting with '0x'
        # see: http://pubs.opengroup.org/onlinepubs/7908799/xcurses/terminfo.html
        "$ROOTDIR/supplementary/runcommand/joy2libgdxkey.py" "$JOY2KEY_DEV" "$JOYSTICK_MAPPINGS_FILE" "$ROM" &
        JOY2KEY_PID=$!
    fi
}

function stop_joy2key() {
    if [[ -n "$JOY2KEY_PID" ]]; then
        kill -INT "$JOY2KEY_PID"
    fi
}

# Execute the game
start_joy2key
fuse $ROM --full-screen
stop_joy2key
