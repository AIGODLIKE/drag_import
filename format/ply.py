import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)
from  ..prop import drag_import_prop

class drag_import_ply_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    global_scale: FloatProperty(
        name='Scale',
        description='',
        default=1.0
    )

    use_scene_unit: BoolProperty(
        name='Scene Unit',
        description="Apply current scene's unit (as defined by unit scale) to imported data",
        default=False
    )
    forward_axis: EnumProperty(
        name='Forward Axis',
        items=(
            ("X", "X", "Positive X axis"),
            ("Y", "Y", "Positive Y axis"),
            ("Z", "Z", "Positive Z axis"),
            ("NEGATIVE_X", "-X", "Negative X axis"),
            ("NEGATIVE_Y", "-Y", "Negative Y axis"),
            ("NEGATIVE_Z", "-Z", "Negative Z axis"),
        ),
        description='',
        default="Y"
    )
    up_axis: EnumProperty(
        name='Up Axis',
        items=(
            ("X", "X", "Positive X axis"),
            ("Y", "Y", "Positive Y axis"),
            ("Z", "Z", "Positive Z axis"),
            ("NEGATIVE_X", "-X", "Negative X axis"),
            ("NEGATIVE_Y", "-Y", "Negative Y axis"),
            ("NEGATIVE_Z", "-Z", "Negative Z axis"),
        ),
        description='',
        default="Z"
    )
    merge_verts: BoolProperty(
        name='Merge Vertices',
        description='Merges vertices by distance',
        default=False
    )
    import_colors: EnumProperty(
        name='Vertex Colors',
        items=(
            ("NONE", "None", "Do not import/export color attributes"),
            ("SRGB", "sRGB", "Vertex colors in the file are in sRGB color space"),
            ("LINEAR", "Linear", "Vertex colors in the file are in linear color space"),
        ),
        description='Import vertex color attributes',
        default="SRGB"
    )



class Drag_import_ply(bpy.types.Operator, drag_import_ply_prop,drag_import_prop):
    """Load a ply file"""
    bl_idname = 'drag_import.ply'
    bl_label = 'Import ply'
    bl_options = {'REGISTER','PRESET','UNDO'}
    def draw(self, context):
        option = self.layout.box()
        prop = context.scene.drag_import_ply_prop
        option.prop(prop, "global_scale")
        option.prop(prop, "use_scene_unit")
        option.prop(prop, "forward_axis")
        option.prop(prop, "up_axis")
        option.prop(prop, "merge_verts")
        option.prop(prop, "import_colors")

    def invoke(self, context, event):
        # 弹出菜单
        # return context.window_manager.invoke_props_dialog(self)
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        # ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        for f in self.files:
            bpy.ops.wm.ply_import(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret

        # return self.import_ply(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_ply_prop
        self.global_scale = prop.global_scale
        self.use_scene_unit = prop.use_scene_unit
        self.forward_axis = prop.forward_axis
        self.up_axis = prop.up_axis
        self.merge_verts = prop.merge_verts
        self.import_colors = prop.import_colors


def register():
    bpy.utils.register_class(drag_import_ply_prop)
    bpy.types.Scene.drag_import_ply_prop = bpy.props.PointerProperty(type=drag_import_ply_prop)
    # bpy.utils.register_class(Drag_import_ply_panel)
    bpy.utils.register_class(Drag_import_ply)


def unregister():
    # bpy.utils.unregister_class(Drag_import_ply_panel)
    bpy.utils.unregister_class(Drag_import_ply)
    del bpy.types.Scene.drag_import_ply_prop
    bpy.utils.unregister_class(drag_import_ply_prop)
