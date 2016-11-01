#!/usr/bin/python
#
# Intends to demonstrate basic use of the experience class
#

from .rleng.experience import experience_new
from .rleng.menu import menu_new

from solent.client.term.curses_term import curses_term_start, curses_term_end
from solent.client.term.window_term import window_term_start, window_term_end
from solent.exceptions import SolentQuitException

import os
import sys
import traceback

C_GAME_WIDTH = 78
C_GAME_HEIGHT = 25

def main():
    if '--tty' in sys.argv:
        fn_device_start = curses_term_start
        fn_device_end = curses_term_end
    elif '--win' in sys.argv:
        fn_device_start = window_term_start
        fn_device_end = window_term_end
    else:
        print('ERROR: specify --tty or --win')
        sys.exit(1)
    try:
        menu = menu_new()
        #
        term_shape = fn_device_start(
            game_width=C_GAME_WIDTH,
            game_height=C_GAME_HEIGHT)
        #
        experience = experience_new(
            term_shape=term_shape,
            width=C_GAME_WIDTH,
            height=C_GAME_HEIGHT,
            menu=menu)
        experience.go()
    except SolentQuitException:
        pass
    except:
        traceback.print_exc()
    finally:
        fn_device_end()

if __name__ == '__main__':
    main()
