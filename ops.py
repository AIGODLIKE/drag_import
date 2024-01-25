import bpy
from bpy.props import (
    CollectionProperty,
    BoolProperty,
)
class Drag_import_files(bpy.types.Operator):
    """Load a FBX file"""
    bl_idname = "drag_import.file"
    bl_label = "Import FBX"
    bl_options = {'UNDO','REGISTER'}
    pop_menu:BoolProperty(
        name="Pop-up menu",
        description="Pop-up Import Settings Window",
        default=False
    )
    files:CollectionProperty(
        name="files",
        description="",
        default=[]
    )
    def invoke(self, context, event):
        if event.ctrl:
            self.pop_menu=True
        else:
            return self.execute(context)
    def execute(self,context):
        pass
def register():

    bpy.utils.register_class(Drag_import_files)


def unregister():

    bpy.utils.unregister_class(Drag_import_files)
