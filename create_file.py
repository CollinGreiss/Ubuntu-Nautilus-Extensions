from gi.repository import Nautilus, GObject
from typing import List
import os

class CreateFileExtension(GObject.GObject, Nautilus.MenuProvider):

    def create_file(self, menu, file):
        directory = file.get_location().get_path()
        new_file = os.path.join(directory, "new_file.txt")

        counter = 1
        while os.path.exists(new_file):
            new_file = os.path.join(directory, f"new_file_{counter}.txt")
            counter += 1

        with open(new_file, "w"):
            pass

    def get_background_items(self, current_folder: Nautilus.FileInfo) -> List[Nautilus.MenuItem]:

        menuitem = Nautilus.MenuItem(
            name="cgreiss::CreateFile",
            label="Create File",
            tip="",
            icon="",
        )
        menuitem.connect("activate", self.create_file, current_folder)

        return [ menuitem ]
    