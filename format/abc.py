import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)


class drag_import_abc_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    scale: FloatProperty(
        name='scale',
        description='',
        default=1.0
    )

    relative_path: BoolProperty(
        name='relative_path',
        description='',
        default=True
    )
    set_frame_range: BoolProperty(
        name='set_frame_range',
        description='',
        default=True
    )
    is_sequence: BoolProperty(
        name='is_sequence',
        description='',
        default=False
    )
    validate_meshes: BoolProperty(
        name='validate_meshes',
        description='',
        default=False
    )
    always_add_cache_reader: BoolProperty(
        name='always_add_cache_reader',
        description='',
        default=False
    )


# class Drag_import_abc_panel(bpy.types.Panel):
#     """创建一个面板在 N面板中"""
#     bl_label = "abc_panel"
#     bl_idname = "abcECT_PT_import_abc"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Drag_import'  # N面板的标签
#
#     def draw(self, context):
#         layout = self.layout
#         drag_import_abc_prop = context.scene.drag_import_abc_prop
#
#         layout.prop(drag_import_abc_prop, "global_scale")
#         layout.prop(drag_import_abc_prop, "clamp_size")
#         layout.prop(drag_import_abc_prop, "forward_axis")
#         layout.prop(drag_import_abc_prop, "up_axis")
#         layout.prop(drag_import_abc_prop, "use_split_abcects")
#         layout.prop(drag_import_abc_prop, "use_split_groups")
#         layout.prop(drag_import_abc_prop, "import_vertex_groups")
#         layout.prop(drag_import_abc_prop, "validate_meshes")


class Drag_import_abc(bpy.types.Operator, drag_import_abc_prop):
    """Load a abc file"""
    bl_idname = 'drag_import.abc'
    bl_label = 'Import abc'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath',))

        if bpy.ops.wm.alembic_import(filepath=self.filepath, **keywords) == {'FINISHED'}:
            ret = {'FINISHED'}
        return ret

        # return self.import_abc(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_abc_prop
        self.scale = prop.scale
        self.relative_path = prop.relative_path
        self.set_frame_range = prop.set_frame_range
        self.is_sequence = prop.is_sequence
        self.validate_meshes = prop.validate_meshes
        self.always_add_cache_reader = prop.always_add_cache_reader


def register():
    bpy.utils.register_class(drag_import_abc_prop)
    bpy.types.Scene.drag_import_abc_prop = bpy.props.PointerProperty(type=drag_import_abc_prop)
    # bpy.utils.register_class(Drag_import_abc_panel)
    bpy.utils.register_class(Drag_import_abc)


def unregister():
    # bpy.utils.unregister_class(Drag_import_abc_panel)
    bpy.utils.unregister_class(Drag_import_abc)
    del bpy.types.Scene.drag_import_abc_prop
    bpy.utils.unregister_class(drag_import_abc_prop)
