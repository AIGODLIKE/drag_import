import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)


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


# class Drag_import_ply_panel(bpy.types.Panel):
#     """创建一个面板在 N面板中"""
#     bl_label = "ply_panel"
#     bl_idname = "plyECT_PT_import_ply"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Drag_import'  # N面板的标签
#
#     def draw(self, context):
#         layout = self.layout
#         drag_import_ply_prop = context.scene.drag_import_ply_prop
#
#         layout.prop(drag_import_ply_prop, "global_scale")
#         layout.prop(drag_import_ply_prop, "clamp_size")
#         layout.prop(drag_import_ply_prop, "forward_axis")
#         layout.prop(drag_import_ply_prop, "up_axis")
#         layout.prop(drag_import_ply_prop, "use_split_plyects")
#         layout.prop(drag_import_ply_prop, "use_split_groups")
#         layout.prop(drag_import_ply_prop, "import_vertex_groups")
#         layout.prop(drag_import_ply_prop, "validate_meshes")


class Drag_import_ply(bpy.types.Operator, drag_import_ply_prop):
    """Load a ply file"""
    bl_idname = 'drag_import.ply'
    bl_label = 'Import ply'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath',))

        if bpy.ops.wm.ply_import(filepath=self.filepath, **keywords) == {'FINISHED'}:
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
