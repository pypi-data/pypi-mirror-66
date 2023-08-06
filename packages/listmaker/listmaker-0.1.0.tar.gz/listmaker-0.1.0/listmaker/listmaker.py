#!/usr/bin/env python3
from contentManager import ContentManager
from screenManager import ScreenManager
from storageManager import StorageManager
from enum import Enum
import sys
import os
import time
import curses
import traceback
import string
import logging

class Modes(Enum):
    EDIT = 1
    NORMAL = 2

class ListMaker:
    def __init__(self):
        self.store = None
        self.cm = None
        self.sm = None
        self.em: EditManager = None
        self.mode = Modes.NORMAL 
        os.environ.setdefault('ESCDELAY', '25')
        logging.basicConfig(filename='app.log', level = logging.DEBUG)
    
    def main(self, filepath):
        try:
            self.store = StorageManager(filepath)
            self.cm = ContentManager(self.store)
            self.sm = ScreenManager()
            self.sm.update_status('Normal Mode')
            content = self.cm.render()
            self.sm.update_content(content)
            while True:
                if self.mode == Modes.NORMAL:
                    self.normal_loop()
                elif self.mode == Modes.EDIT:
                    self.edit_loop()
        except:
            curses.endwin()
            print('Exception in application')
            print('-'*50)
            traceback.print_exc()
            print('-'*50)


    def normal_loop(self):
        sm = self.sm
        cm = self.cm
        key = self.process_input()
        if key == 'KEY_DOWN' or key == 'j':
            sm.update_selected(cm.traverse_down())
        elif key == 'KEY_UP' or key == 'k':
            sm.update_selected(cm.traverse_up())
        elif key == 'c':
            content = self.cm.add_child()
            self.sm.update_content(content)
            self.start_edit()
        elif key == 's':
            self.store.write(self.cm.root)
        elif key == 'e':
            self.start_edit()
        elif key == 'Enter' or key == 'b':
            content = self.cm.add_sibling()
            self.sm.update_content(content)
            self.start_edit()
        elif key == 'd':
            content = self.cm.delete_node()
            self.sm.update_content(content)


    def edit_loop(self):
        key = self.process_input()
        if key == 'KEY_LEFT':
            target = self.cm.traverse_left()
            self.sm.show_cursor(target)
        elif key == 'KEY_RIGHT':
            target = self.cm.traverse_right()
            self.sm.show_cursor(target)
        elif key == 'Escape':
            self.end_edit()
        elif key == 'KEY_BACKSPACE':
            target = self.cm.backspace()
            self.sm.update_line(target)
            self.sm.show_cursor(target)
        elif key == 'KEY_DC':
            target = self.cm.del_char()
            self.sm.update_line(target)
            self.sm.show_cursor(target)
        elif key == 'Enter':
            self.end_edit()
            self.sm.update_content(self.cm.add_sibling())
            self.start_edit()
        elif key in string.printable:
            target = self.cm.insert(key)
            self.sm.update_line(target)
            self.sm.show_cursor(target)


    def start_edit(self):
        self.mode = Modes.EDIT
        self.sm.update_status('Edit Mode')
        edit_target = self.cm.get_selected_row()
        self.sm.show_cursor(edit_target)

    def end_edit(self):
        self.mode = Modes.NORMAL
        self.sm.update_status('Normal Mode')
        self.sm.hide_cursor()


    def process_input(self):
        ch = self.sm.getch()
        result = self.process_ch(ch)
        if result == None:
            result = self.sm.getkey()
        return result


    def process_ch(self, ch) -> str:
        if ch == 27:
            # Escape key
            return 'Escape'
        elif ch == 8:
            # Backspace key
            return 'Backspace'
        elif ch == 10:
            # Enter key
            return 'Enter'
        else:
            curses.ungetch(ch)
        return None


if __name__ == '__main__':
    argv = sys.argv
    if(len(argv) < 2):
        print('Please provide the path of the file you want to edit, or path to new file.')
        sys.exit(-1)
    elif(len(argv) > 2):
        print('Program accepts only one argument, which should be the file you want to edit or create.')
        sys.exit(-1)
    lm = ListMaker()
    lm.main(argv[1])

