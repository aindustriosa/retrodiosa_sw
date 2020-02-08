#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import logging
import subprocess
from curses import wrapper


def volume_up():
    """ Perform a volume up """
    try:
    
        subprocess.run("echo r > /dev/ttyUSB0", shell=True, check=True)
        subprocess.run("echo r > /dev/ttyUSB0", shell=True, check=True)
        subprocess.run("echo r > /dev/ttyUSB0", shell=True, check=True)

    except Exception:
        pass

def volume_down():
    """ Perform a volume down """

    try:
        subprocess.run("echo t > /dev/ttyUSB0", shell=True, check=True)
        subprocess.run("echo t > /dev/ttyUSB0", shell=True, check=True)
        subprocess.run("echo t > /dev/ttyUSB0", shell=True, check=True)

    except Exception:
        pass


def refresh_window(win, stdscr):
    """ Refresh the window """
    win.clear()
    win.bkgd(' ', curses.color_pair(1) | curses.A_BOLD | curses.A_DIM)
    win.border("|", "-")
    win.addstr(2, 8, "WAITING COMMAND!", curses.color_pair(2)| curses.A_BLINK)
    win.syncok(True)
    win.overlay(stdscr)
    win.refresh()

def main(stdscr):
    """ Intializing curses and static menu """
    
    # Clear screen
    stdscr.clear()

    # pick curses dimensions
    max_lines = curses.LINES - 1
    max_cols = curses.COLS - 1

    begin_menu_x = int(max_cols * 0.5) - 10
    begin_menu_y = max([int(max_lines*0.5) - 15, 2])
    
    stdscr.addstr(begin_menu_y, begin_menu_x, "TV Volumen Control:",
                  curses.A_REVERSE)

    stdscr.addstr(begin_menu_y + 2, begin_menu_x + 3, "1) <- to set down TV volume")
    stdscr.addstr(begin_menu_y + 3, begin_menu_x + 3, "2) -> to set up TV volume")
    stdscr.addstr(begin_menu_y + 4, begin_menu_x + 3, "3) Joystick A button to exit")
    stdscr.addstr(begin_menu_y + 6, begin_menu_x + 4, " /\_/\\")    
    stdscr.addstr(begin_menu_y + 7, begin_menu_x + 3, " (='_' )")
    stdscr.addstr(begin_menu_y + 8, begin_menu_x + 3, "o(,(\")(\")")    
    
    begin_win_x = int(max_cols * 0.5) - 15
    begin_win_y = max(int(max_lines * 0.5) - 5, 13)
                      
    height = 5; width = 30
    win = curses.newwin(height, width, begin_win_y, begin_win_x)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
    
    refresh_window(win, stdscr)
    
    # Emit a short beep
    curses.beep()
    while(True):
        
        key_str = stdscr.getkey()

        refresh_window(win, stdscr)
        if key_str != "\n":        
            win.addstr(3,2, key_str, curses.color_pair(1) | curses.A_BLINK)
            
        if key_str == "KEY_LEFT":
            win.addstr(2, 8, "VOLUME DOWN!    ", curses.color_pair(2)| curses.A_BLINK)
            win.addstr(3,15, "<('-'<)", curses.color_pair(3) | curses.A_BLINK)
            volume_down()
            curses.beep()

            

        elif key_str == "KEY_RIGHT":
            win.addstr(2, 8, "VOLUME UP!      ", curses.color_pair(2)| curses.A_BLINK)
            win.addstr(3,15, "(>'-')>", curses.color_pair(3) | curses.A_BLINK)
            volume_up()
            curses.beep()


        elif key_str == "KEY_DOWN" or key_str == "KEY_UP":
            pass
            
        else:
            break
            
        win.refresh()

    
wrapper(main)


