import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)
from  ..prop import drag_import_prop

class drag_import_x3d_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()


    axis_forward: EnumProperty(
        name='Forward Axis',
        items=(
            ("X", "X", "Positive X axis"),
            ("Y", "Y", "Positive Y axis"),
            ("Z", "Z", "Positive Z axis"),
            ("-X", "-X", "Negative X axis"),
            ("-Y", "-Y", "Negative Y axis"),
            ("-Z", "-Z", "Negative Z axis"),
        ),
        description='',
        default="Z"
    )
    axis_up: EnumProperty(
        name='Up Axis',
        items=(
            ("X", "X", "Positive X axis"),
            ("Y", "Y", "Positive Y axis"),
            ("Z", "Z", "Positive Z axis"),
            ("-X", "-X", "Negative X axis"),
            ("-Y", "-Y", "Negative Y axis"),
            ("-Z", "-Z", "Negative Z axis"),
        ),
        description='',
        default="Y"
    )



class Drag_import_x3d(bpy.types.Operator, drag_import_x3d_prop,drag_import_prop):
    """Load a x3d file"""
    bl_idname = 'drag_import.x3d'
    bl_label = 'Import x3d'
    bl_options = {'REGISTER','PRESET','UNDO'}
    def draw(self, context):
        layout = self.layout.box()
        prop = context.scene.drag_import_x3d_prop
        layout.label(text='Transform')
        layout.prop(prop, "axis_forward")
        layout.prop(prop, "axis_up")


    def invoke(self, context, event):
        # 弹出菜单
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        for f in self.files:
            bpy.ops.import_scene.x3d(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret

        # return self.import_x3d(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_x3d_prop

        self.axis_forward = prop.axis_forward
        self.axis_up = prop.axis_up



def register():
    bpy.utils.register_class(drag_import_x3d_prop)
    bpy.types.Scene.drag_import_x3d_prop = bpy.props.PointerProperty(type=drag_import_x3d_prop)
    # bpy.utils.register_class(Drag_import_x3d_panel)
    bpy.utils.register_class(Drag_import_x3d)


def unregister():
    # bpy.utils.unregister_class(Drag_import_x3d_panel)
    bpy.utils.unregister_class(Drag_import_x3d)
    del bpy.types.Scene.drag_import_x3d_prop
    bpy.utils.unregister_class(drag_import_x3d_prop)
