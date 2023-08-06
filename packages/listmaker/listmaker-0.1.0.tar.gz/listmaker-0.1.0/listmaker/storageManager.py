from anytree import Node
from entry import Entry
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter, DictImporter
from pathlib import Path
import sys
import os

class StorageManager(object):
    '''This class manages the persistence for content.'''

    def __init__(self, filepath):
        self._filepath = filepath


    def read(self) -> Entry:
       content = None
       if os.path.isfile(self._filepath):
           fp = open(Path(self._filepath))
           d_imp = DictImporter(nodecls = Entry)
           importer = JsonImporter(dictimporter = d_imp)
           content = importer.import_(fp.read())
           fp.close()
       return content


    def write(self, content: Entry):
        fp = open(Path(self._filepath), mode='w')
        exporter = JsonExporter(indent=2)
        fp.write(exporter.export(content))
        fp.close()

