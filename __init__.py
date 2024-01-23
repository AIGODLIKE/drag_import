from . import hook
from . import timer

bl_info = {
    "name": "My Drag and Drop Plugin",
    "description": "Handles drag and drop files into Blender.",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "Import-Export"
}

import bpy
# Your existing code for handling drag and drop goes here
# ...

# ... (all your existing functions and logic)
# while True:
#     # Timer.run1()
#     pass
#     # func = func_queue.get()  # 这将阻塞直到队列中有数据
#     # func()
from io_scene_fbx import ImportFBX


class Dragpanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        return True

    bl_idname = "VIEW3D_PT_test_2"
    bl_label = "Cupcko:反馈群536440291"

    def draw(self, context):
        layout = self.layout
        label = layout.label(text="Drag and Drop Files Here")
        layout.prop(ImportFBX, "global_scale")


classes = [
    Dragpanel,
]
from .format import fbx, gltf, dae, obj,abc,usd,ply,stl,x3d,bvh,svg


def register():
    # Register handlers, UI elements, etc.
    # bpy.utils.register_class(...)Dragpanel
    from bpy.utils import register_class
    for c in classes:
        register_class(c)
    fbx.register()
    gltf.register()
    dae.register()
    obj.register()
    abc.register()
    usd.register()
    ply.register()
    stl.register()
    x3d.register()
    bvh.register()
    svg.register()
    timer.timer_reg()
    t = hook.Thread(target=hook.track, daemon=True)
    t.start()


def unregister():
    # Unregister handlers, UI elements, etc.
    # bpy.utils.unregister_class(...)
    from bpy.utils import unregister_class
    for c in classes:
        unregister_class(c)
    fbx.unregister()
    gltf.unregister()
    timer.timer_unreg()


if __name__ == "__main__":
    register()
