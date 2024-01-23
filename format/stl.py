import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)


class drag_import_stl_prop(bpy.types.PropertyGroup):
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
        default="Y"
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
        default="Z"
    )
    use_facet_normal: BoolProperty(
        name='Facet Normals',
        description="Use (import) facet normals (note that this will still give flat shading)",
        default=False,
    )



# class Drag_import_stl_panel(bpy.types.Panel):
#     """创建一个面板在 N面板中"""
#     bl_label = "stl_panel"
#     bl_idname = "stlECT_PT_import_stl"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Drag_import'  # N面板的标签
#
#     def draw(self, context):
#         layout = self.layout
#         drag_import_stl_prop = context.scene.drag_import_stl_prop
#
#         layout.prop(drag_import_stl_prop, "global_scale")
#         layout.prop(drag_import_stl_prop, "clamp_size")
#         layout.prop(drag_import_stl_prop, "forward_axis")
#         layout.prop(drag_import_stl_prop, "up_axis")
#         layout.prop(drag_import_stl_prop, "use_split_stlects")
#         layout.prop(drag_import_stl_prop, "use_split_groups")
#         layout.prop(drag_import_stl_prop, "import_vertex_groups")
#         layout.prop(drag_import_stl_prop, "validate_meshes")


class Drag_import_stl(bpy.types.Operator, drag_import_stl_prop):
    """Load a stl file"""
    bl_idname = 'drag_import.stl'
    bl_label = 'Import stl'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath',))

        if bpy.ops.import_mesh.stl(filepath=self.filepath, **keywords) == {'FINISHED'}:
            ret = {'FINISHED'}
        return ret

        # return self.import_stl(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_stl_prop
        self.global_scale = prop.global_scale
        self.use_scene_unit = prop.use_scene_unit
        self.axis_forward = prop.axis_forward
        self.axis_up = prop.axis_up
        self.use_facet_normal = prop.use_facet_normal


def register():
    bpy.utils.register_class(drag_import_stl_prop)
    bpy.types.Scene.drag_import_stl_prop = bpy.props.PointerProperty(type=drag_import_stl_prop)
    # bpy.utils.register_class(Drag_import_stl_panel)
    bpy.utils.register_class(Drag_import_stl)


def unregister():
    # bpy.utils.unregister_class(Drag_import_stl_panel)
    bpy.utils.unregister_class(Drag_import_stl)
    del bpy.types.Scene.drag_import_stl_prop
    bpy.utils.unregister_class(drag_import_stl_prop)
