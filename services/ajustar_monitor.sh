#!/bin/sh

intern=LVDS-1
extern=VGA-1
serie=/dev/ttyUSB0

stty -F "$serie" 9600
echo 1 > "$serie"

while [ 1 ]
do
if xrandr |grep "$extern disconnected"; then
	echo "Enabling internal monitor"
	xrandr --output "$extern" --off --output "$intern" --auto
else
    if ! ps aux | grep "libgdx" | grep -v "grep"; then
	echo "Enabling external monitor"
	xrandr --output "$intern" --off --output "$extern" --auto
    fi
fi
sleep 5
done
