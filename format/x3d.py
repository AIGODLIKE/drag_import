import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)


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



# class Drag_import_x3d_panel(bpy.types.Panel):
#     """创建一个面板在 N面板中"""
#     bl_label = "x3d_panel"
#     bl_idname = "x3dECT_PT_import_x3d"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Drag_import'  # N面板的标签
#
#     def draw(self, context):
#         layout = self.layout
#         drag_import_x3d_prop = context.scene.drag_import_x3d_prop
#
#         layout.prop(drag_import_x3d_prop, "global_scale")
#         layout.prop(drag_import_x3d_prop, "clamp_size")
#         layout.prop(drag_import_x3d_prop, "forward_axis")
#         layout.prop(drag_import_x3d_prop, "up_axis")
#         layout.prop(drag_import_x3d_prop, "use_split_x3dects")
#         layout.prop(drag_import_x3d_prop, "use_split_groups")
#         layout.prop(drag_import_x3d_prop, "import_vertex_groups")
#         layout.prop(drag_import_x3d_prop, "validate_meshes")


class Drag_import_x3d(bpy.types.Operator, drag_import_x3d_prop):
    """Load a x3d file"""
    bl_idname = 'drag_import.x3d'
    bl_label = 'Import x3d'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath',))

        if bpy.ops.import_scene.x3d(filepath=self.filepath, **keywords) == {'FINISHED'}:
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
