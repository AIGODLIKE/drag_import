from . import hook
from . import timer
import bpy
bl_info = {
    "name": "DragImport",
    "description": "Handles drag and drop files into Blender.",
    "author": "AIGODLIKE Community:cupcko",
    "version": (1, 0,1),
    "blender": (3, 6, 0),
    "location": "View3D > Tool Shelf",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "Import-Export"
}
class TranslationHelper():
    def __init__(self, name: str, data: dict, lang='zh_CN'):
        self.name = name
        self.translations_dict = dict()

        for src, src_trans in data.items():
            key = ("Operator", src)
            self.translations_dict.setdefault(lang, {})[key] = src_trans
            key = ("*", src)
            self.translations_dict.setdefault(lang, {})[key] = src_trans

    def register(self):
        try:
            bpy.app.translations.register(self.name, self.translations_dict)
        except(ValueError):
            pass

    def unregister(self):
        bpy.app.translations.unregister(self.name)


from . import zh_CN

Drag_import_zh_CN = TranslationHelper('Drag_import_zh_CN', zh_CN.data)
Drag_import_zh_HANS = TranslationHelper('Drag_import_zh_HANS', zh_CN.data, lang='zh_HANS')
import threading
from . import reg
def register():
    if bpy.app.version < (4, 0, 0):
        Drag_import_zh_CN.register()
    else:
        Drag_import_zh_CN.register()
        Drag_import_zh_HANS.register()

    reg.register()
    timer.timer_reg()
    t = threading.Thread(target=hook.track, daemon=True)
    t.start()


def unregister():
    if bpy.app.version < (4, 0, 0):
        Drag_import_zh_CN.unregister()
    else:
        Drag_import_zh_CN.unregister()
        Drag_import_zh_HANS.unregister()
    reg.unregister()
    timer.timer_unreg()
    from .hook import my_dll_wrapper
    del my_dll_wrapper

if __name__ == "__main__":
    register()
