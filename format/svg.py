import os

import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)
from  ..prop import drag_import_prop

class drag_import_svg_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    resolution: IntProperty(
        name="Resolution",
        description="Resolution of the generated strokes",
        min=1, max=30,
        soft_min=1, soft_max=20,
        default=10,
    )
    scale: FloatProperty(
        name="Scale",
        description="Scale of the final strokes",
        min=0.001, max=100.0,
        soft_min=0.001, soft_max=100.0,
        default=10.0,
    )



class Drag_import_svg(bpy.types.Operator, drag_import_svg_prop,drag_import_prop):
    """Load a svg file"""
    bl_idname = 'drag_import.svg'
    bl_label = 'Import svg'
    bl_options = {'REGISTER','PRESET','UNDO'}
    def draw(self, context):
        prop = context.scene.drag_import_svg_prop
        option=self.layout.box()
        option.prop(prop, "resolution")
        option.prop(prop, "scale")
    def invoke(self, context, event):
        # 弹出菜单
        # return context.window_manager.invoke_props_dialog(self)
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)

        if self.pop_menu:
            keywords = self.as_keywords(ignore=('filepath','files','pop_menu',))
            for f in self.files:
                bpy.ops.wm.gpencil_import_svg(directory=os.path.dirname(f.name), filepath="", files=[{"name": os.path.basename(f.name)}],**keywords)

        else:
            keywords = self.as_keywords(ignore=('filepath','files','pop_menu','resolution','scale'))
            for f in self.files:
                bpy.ops.import_curve.svg(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret

        # return self.import_svg(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_svg_prop
        self.resolution = prop.resolution
        self.scale = prop.scale



def register():
    bpy.utils.register_class(drag_import_svg_prop)
    bpy.types.Scene.drag_import_svg_prop = bpy.props.PointerProperty(type=drag_import_svg_prop)
    # bpy.utils.register_class(Drag_import_svg_panel)
    bpy.utils.register_class(Drag_import_svg)


def unregister():
    # bpy.utils.unregister_class(Drag_import_svg_panel)
    bpy.utils.unregister_class(Drag_import_svg)
    del bpy.types.Scene.drag_import_svg_prop
    bpy.utils.unregister_class(drag_import_svg_prop)
