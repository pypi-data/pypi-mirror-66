from contentRow import ContentRow
from entry import Entry
from typing import List, Tuple
import curses
import sys


class AnnoWnd:
    def __init__(self, lines: int, cols: int, begin_y: int, begin_x: int) -> None:
        self.wnd = curses.newwin(lines, cols, begin_y, begin_x)
        self.wnd.keypad(True)
        self.selected_mrk = '>'
        self.selected_mrk_col = 0
        self.selected_mrk_row = 0
        self.edit_mrk_col = 1
        self.collapse_mrk_col = 2
    
    def update_selected(self, sel_row: int) -> None:
        x = self.selected_mrk_col
        # Erase previous annotation
        y = self.selected_mrk_row
        self.wnd.addstr(y, x, ' ')
        # Set new annotation
        y = self.selected_mrk_row = sel_row
        self.wnd.addstr(y, x, self.selected_mrk)
        self.wnd.refresh()


class ContentWnd:

    def __init__(self, lines: int, cols: int, begin_y: int, begin_x: int) -> None:
        self.wnd = curses.newwin(lines, cols, begin_y, begin_x)
        self.wnd.keypad(True)
        self.indent_size = 4

    def update_content(self, content_list: List[ContentRow]):
        self.wnd.clear()
        y = 0
        for content_row in content_list:
            text = content_row.entry.name
            x = content_row.indent_lvl * self.indent_size
            self.wnd.addstr(y, x, text)
            y += 1
        self.wnd.refresh()
   

    def getch(self):
        return self.wnd.getch()


    def getkey(self):
        return self.wnd.getkey()


    def move_cursor(self, target: Tuple[int, ContentRow]):
        y = target[0]
        cr = target[1]
        entry = cr.entry
        x = entry.curs + (cr.indent_lvl * self.indent_size)
        self.wnd.move(y, x)


    def update_line(self, target: Tuple[int, ContentRow]):
        y = target[0]
        cr = target[1]
        x = cr.indent_lvl * self.indent_size
        self.wnd.move(y, x)
        self.wnd.clrtoeol()
        self.wnd.addstr(y, x, cr.entry.name)
        self.wnd.move(y, x)
        self.wnd.refresh()


class StatusWnd:
    def __init__(self, lines: int, cols: int, begin_y: int, begin_x: int) -> None:
        self.wnd = curses.newwin(lines, cols, begin_y, begin_x)
        self.wnd.addstr(0, 0, '-------------------------------------------------------------')
        self.wnd.border()
        self.wnd.refresh()


    def update_status(self, status: str) -> None:
        self.wnd.clear()
        self.wnd.addstr(1, 2, status)
        self.wnd.border()
        self.wnd.refresh()

class NavWnd:
    def __init__(self, lines: int, cols: int, begin_y: int, begin_x: int) -> None:
        self.wnd = curses.newwin(lines, cols, begin_y, begin_x)
        self.wnd.keypad(True)

