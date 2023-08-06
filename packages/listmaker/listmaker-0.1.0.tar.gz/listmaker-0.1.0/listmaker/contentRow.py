from entry import Entry

class ContentRow:
    '''A ViewModel which represents a single row of content'''

    def __init__(self, 
                 entry: Entry, 
                 indent_lvl: int) -> None:
        self.entry = entry
        self.indent_lvl = indent_lvl


