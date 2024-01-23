import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)


class drag_import_obj_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    global_scale: FloatProperty(
        name='global_scale',
        description="min chain length",
        default=1.0)

    clamp_size: FloatProperty(
        name='clamp_size',
        description='',
        default=0.0
    )
    forward_axis: EnumProperty(
        name='forward_axis',
        items=(
            ("X", "X", "Positive X axis"),
            ("Y", "Y", "Positive Y axis"),
            ("Z", "Z", "Positive Z axis"),
            ("NEGATIVE_X", "-X", "Negative X axis"),
            ("NEGATIVE_Y", "-Y", "Negative Y axis"),
            ("NEGATIVE_Z", "-Z", "Negative Z axis"),
        ),
        description='',
        default="NEGATIVE_Z"
    )
    up_axis: EnumProperty(
        name='up_axis',
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
    use_split_objects: BoolProperty(
        name='use_split_objects',
        description='',
        default=True
    )
    use_split_groups: BoolProperty(
        name='use_split_groups',
        description='',
        default=False
    )
    import_vertex_groups: BoolProperty(
        name='import_vertex_groups',
        description='',
        default=False
    )
    validate_meshes: BoolProperty(
        name='validate_meshes',
        description='',
        default=False
    )


class Drag_import_obj_panel(bpy.types.Panel):
    """创建一个面板在 N面板中"""
    bl_label = "obj_panel"
    bl_idname = "OBJECT_PT_import_obj"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Drag_import'  # N面板的标签

    def draw(self, context):
        layout = self.layout
        drag_import_obj_prop = context.scene.drag_import_obj_prop

        layout.prop(drag_import_obj_prop, "global_scale")
        layout.prop(drag_import_obj_prop, "clamp_size")
        layout.prop(drag_import_obj_prop, "forward_axis")
        layout.prop(drag_import_obj_prop, "up_axis")
        layout.prop(drag_import_obj_prop, "use_split_objects")
        layout.prop(drag_import_obj_prop, "use_split_groups")
        layout.prop(drag_import_obj_prop, "import_vertex_groups")
        layout.prop(drag_import_obj_prop, "validate_meshes")


class Drag_import_obj(bpy.types.Operator, drag_import_obj_prop):
    """Load a obj file"""
    bl_idname = 'drag_import.obj'
    bl_label = 'Import obj'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath',))

        if bpy.ops.wm.obj_import(filepath=self.filepath, **keywords) == {'FINISHED'}:
            ret = {'FINISHED'}
        return ret

        # return self.import_obj(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_obj_prop
        self.global_scale = prop.global_scale
        self.clamp_size = prop.clamp_size
        self.forward_axis = prop.forward_axis
        self.up_axis = prop.up_axis
        self.use_split_objects = prop.use_split_objects
        self.use_split_groups = prop.use_split_groups
        self.import_vertex_groups = prop.import_vertex_groups
        self.validate_meshes = prop.validate_meshes


def register():
    bpy.utils.register_class(drag_import_obj_prop)
    bpy.types.Scene.drag_import_obj_prop = bpy.props.PointerProperty(type=drag_import_obj_prop)
    bpy.utils.register_class(Drag_import_obj_panel)
    bpy.utils.register_class(Drag_import_obj)


def unregister():
    bpy.utils.unregister_class(Drag_import_obj_panel)
    bpy.utils.unregister_class(Drag_import_obj)
    del bpy.types.Scene.drag_import_obj_prop
    bpy.utils.unregister_class(drag_import_obj_prop)
