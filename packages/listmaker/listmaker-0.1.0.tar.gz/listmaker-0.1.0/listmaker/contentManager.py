from typing import List, Tuple
from entry import Entry
from contentRow import ContentRow
from anytree import RenderTree
from storageManager import StorageManager
import sys


class ContentManager:
    '''This class manages the content for the listMaker
    '''

    def __init__(self, store: StorageManager):
        self.root = store.read()
        if(self.root == None):
            self.root = Entry('root', None)
            a = Entry('Topic 01', self.root)
            b = Entry('Subtopic', a)
            c = Entry('Topic 02', self.root)
        if(self.root.children == None):
            a = Entry(' ', self.root)
        self.selected_row = 0
        self.render()


    def render(self) -> Tuple[List[ContentRow], int]:
        cl = list()
        for pre, _, entry in RenderTree(self.root):
            indent_lvl = int(len(pre) / 4)
            row = ContentRow(entry, indent_lvl)
            cl.append(row)
        self.content_list = cl
        return (self.content_list, self.selected_row)


    def traverse_up(self) -> int:
        if self.selected_row > 0:
            self.selected_row -= 1
        return self.selected_row


    def traverse_down(self) -> int:
        last_row = len(self.content_list) - 1
        if self.selected_row < last_row:
            self.selected_row += 1
        return self.selected_row
            

    def add_child(self) -> Tuple[List[ContentRow], int]:
        cr = self.content_list[self.selected_row]
        e = cr.entry
        child = Entry('', e)
        self.render()
        self.selected_row = self.find_entry_pos(child)       
        return (self.content_list, self.selected_row)


    def add_sibling(self) -> Tuple[List[ContentRow], int]:
        cr = self.content_list[self.selected_row]
        e = cr.entry
        if e != self.root:
            p = e.parent
            child = Entry('', p)
            self.render()
            self.selected_row = self.find_entry_pos(child)       
        return (self.content_list, self.selected_row)

    
    def delete_node(self) -> Tuple[List[ContentRow], int]:
        cr = self.content_list[self.selected_row]
        e = cr.entry
        p = e.parent
        if e == self.root:
            # Can't do
            return (self.content_list, self.selected_row)
        if len(e.children) > 0:
            # Reassign children to node's parent.
            for x in e.children:
                x.parent = p
        if self.selected_row == len(self.content_list) - 1:
            # If selection is at last row, we'll need to move it up
            self.selected_row -= 1
        # The following line removes the node
        e.parent = None
        self.render()
        return (self.content_list, self.selected_row)


    def get_selected_row(self) -> Tuple[int, ContentRow]:
        return (self.selected_row, self.content_list[self.selected_row])


    def traverse_right(self) -> Tuple[int, ContentRow]:
        self.content_list[self.selected_row].entry.curs_right()
        return (self.selected_row, self.content_list[self.selected_row])


    def traverse_left(self) -> Tuple[int, ContentRow]:
        self.content_list[self.selected_row].entry.curs_left()
        return (self.selected_row, self.content_list[self.selected_row])


    def backspace(self) -> Tuple[int, ContentRow]:
        self.content_list[self.selected_row].entry.backspace()
        return (self.selected_row, self.content_list[self.selected_row])


    def del_char(self) -> Tuple[int, ContentRow]:
        self.content_list[self.selected_row].entry.del_char()
        return (self.selected_row, self.content_list[self.selected_row])


    def insert(self, char) -> Tuple[int, ContentRow]:
        entry = self.content_list[self.selected_row].entry
        entry.insert(char)
        return (self.selected_row, self.content_list[self.selected_row])


    def delete(self) -> Tuple[List[ContentRow], int]:
        return (self.content_list, self.selected_row)


    def find_entry_pos(self, ent: Entry) -> int:
        pos = 0
        for x in self.content_list:
            if x.entry == ent:
                return pos
            pos += 1
        return -1


