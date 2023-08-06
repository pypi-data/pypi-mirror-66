from anytree import NodeMixin, RenderTree
import sys

class Entry(NodeMixin):
    def __init__(self, 
                 name: str, 
                 parent = None, 
                 decorations: list = None, 
                 text: str = None,
                 children = None,
                 curs: int = 0):
        self.name = name
        self.parent = parent
        if decorations:
            self.decorations = decorations
        if text:
            self.text = text
        if children:
            self.children = children
        self.curs = curs


    def insert(self, char):
        self.name = self.name[:self.curs] + \
                    char + self.name[self.curs:]
        self.curs += len(char)


    def backspace(self):
        if self.curs == 0:
            return
        self.name = self.name[:self.curs - 1] + self.name[self.curs:]
        self.curs -= 1


    def del_char(self):
        if len(self.name) == 0:
            return
        self.name = self.name[:self.curs] + self.name[self.curs + 1:]
        if self.curs > len(self.name) - 1:
            self.curs = len(self.name)

    def curs_right(self):
        if self.curs == len(self.name) - 1:
            return
        self.curs += 1


    def curs_left(self):
        if self.curs == 0:
            return
        self.curs -= 1


