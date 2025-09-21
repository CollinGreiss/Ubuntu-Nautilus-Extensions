from gi.repository import Nautilus, GObject
import os
from typing import List
from PIL import Image

class CustomActionExtension(GObject.GObject, Nautilus.MenuProvider):

    supported_formats = [".png", ".jpg", ".jpeg", ".webp"]

    def convert_image(self, menu, files, format):

        for file in files:
            filepath = file.get_location().get_path()
            base, ext = os.path.splitext(filepath)
            new_filepath = base + "." + format

            if ext.lower() == "." + format: continue
            if not ext.lower() in self.supported_formats: continue
            if os.path.exists(new_filepath): continue

            img = Image.open(filepath)
            img.save(new_filepath, format.upper())

    def get_file_items ( self, files: List[Nautilus.FileInfo],) -> List[Nautilus.MenuItem]:

        if len(files) != 1:

            any_supported = False
            for file in files:
                filepath = file.get_location().get_path()
                file_ext = os.path.splitext(filepath)[1].lower()
                if file_ext in self.supported_formats:
                    any_supported = True
                    break

            if not any_supported: return []

            submenu = Nautilus.Menu()
            convert_to_png = Nautilus.MenuItem(
                name="cgreiss::ConvertToPNG",
                label="Convert to PNG",
                tip="",
                icon="",
            )
            convert_to_png.connect("activate", self.convert_image, files, "png")
            submenu.append_item(convert_to_png)

            convert_to_jpg = Nautilus.MenuItem(
                name="cgreiss::ConvertToJPG",
                label="Convert to JPG",
                tip="",
                icon="",
            )
            convert_to_jpg.connect("activate", self.convert_image, files, "jpg")
            submenu.append_item(convert_to_jpg)

            convert_to_webp = Nautilus.MenuItem(
                name="cgreiss::ConvertToWEBP",
                label="Convert to WEBP",
                tip="",
                icon="",
            )
            convert_to_webp.connect("activate", self.convert_image, files, "webp")
            submenu.append_item(convert_to_webp)

            menu_item = Nautilus.MenuItem(
                name="cgreiss::ConvertImage",
                label="Convert Images",
                tip="Supports: PNG, JPG, WEBP",
                icon="",
            )
            menu_item.set_submenu(submenu)
            return [menu_item]

        file = files[0]
        filepath = file.get_location().get_path()

        file_ext = os.path.splitext(filepath)[1].lower()
        if not file_ext in self.supported_formats: return []
        
        submenu = Nautilus.Menu()

        if (file_ext != ".png"):

            convert_to_png = Nautilus.MenuItem(
                name="cgreiss::ConvertToPNG",
                label="Convert to PNG",
                tip="",
                icon="",
            )
            convert_to_png.connect("activate", self.convert_image, [file], "png")
            submenu.append_item(convert_to_png)

        if (file_ext != ".jpg" and file_ext != ".jpeg"):

            convert_to_jpg = Nautilus.MenuItem(
                name="cgreiss::ConvertToJPG",
                label="Convert to JPG",
                tip="",
                icon="",
            )
            convert_to_jpg.connect("activate", self.convert_image, [file], "jpg")
            submenu.append_item(convert_to_jpg)

        if (file_ext != ".webp"):

            convert_to_webp = Nautilus.MenuItem(
                name="cgreiss::ConvertToWEBP",
                label="Convert to WEBP",
                tip="",
                icon="",
            )
            convert_to_webp.connect("activate", self.convert_image, [file], "webp")
            submenu.append_item(convert_to_webp)

        menu_item = Nautilus.MenuItem(
            name="cgreiss::ConvertImage",
            label="Convert Image",
            tip="Supports: PNG, JPG, WEBP",
            icon="",
        )
        menu_item.set_submenu(submenu)

        return [menu_item]
