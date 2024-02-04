import typing

import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,

    CollectionProperty,
    StringProperty,

)
# class OperatorFileListElement(bpy.types.PropertyGroup):
    # name: typing.Union[str, typing.Any] = None
# class FilePathPropertyGroup(bpy.types.PropertyGroup):
#     path: StringProperty()
class drag_import_prop(bpy.types.PropertyGroup):
    pop_menu:BoolProperty(
        name="Pop-up menu",
        description="Pop-up Import Settings Window",
        default=False
    )
    files: CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
    )
    files_string=[]

def register():
    # bpy.utils.register_class(OperatorFileListElement)
    bpy.utils.register_class(drag_import_prop)
    bpy.types.Scene.drag_import_prop = bpy.props.PointerProperty(type=drag_import_prop)


def unregister():


    del bpy.types.Scene.drag_import_prop
    bpy.utils.unregister_class(drag_import_prop)
    # bpy.utils.unregister_class(OperatorFileListElement)
