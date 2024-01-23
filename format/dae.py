import bpy
from bpy.props import (
    BoolProperty,

    IntProperty,
    StringProperty,

)


class drag_import_dae_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    min_chain_length: IntProperty(
        name='min chain length',
        description="min chain length")

    import_units: BoolProperty(
        name='import_units',
        description='',
        default=False
    )
    custom_normals: BoolProperty(
        name='custom_normals',
        description='',
        default=True
    )
    fix_orientation: BoolProperty(
        name='fix_orientation',
        description='',
        default=False
    )
    find_chains: BoolProperty(
        name='find_chains',
        description='',
        default=False
    )
    auto_connect: BoolProperty(
        name='auto_connect',
        description='',
        default=False
    )
    keep_bind_info: BoolProperty(
        name='keep_bind_info',
        description='',
        default=False
    )


class Drag_import_dae_panel(bpy.types.Panel):
    """创建一个面板在 N面板中"""
    bl_label = "dae_panel"
    bl_idname = "OBJECT_PT_import_dae"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Drag_import'  # N面板的标签

    def draw(self, context):
        layout = self.layout
        drag_import_dae_prop = context.scene.drag_import_dae_prop

        layout.prop(drag_import_dae_prop, "import_units")
        layout.prop(drag_import_dae_prop, "custom_normals")
        layout.prop(drag_import_dae_prop, "fix_orientation")
        layout.prop(drag_import_dae_prop, "find_chains")
        layout.prop(drag_import_dae_prop, "auto_connect")
        layout.prop(drag_import_dae_prop, "min_chain_length")
        layout.prop(drag_import_dae_prop, "keep_bind_info")


class Drag_import_dae(bpy.types.Operator,drag_import_dae_prop):
    """Load a dae file"""
    bl_idname = 'drag_import.dae'
    bl_label = 'Import dae'
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath',))

        if bpy.ops.wm.collada_import(filepath=self.filepath, **keywords) == {'FINISHED'}:
            ret = {'FINISHED'}
        return ret

        # return self.import_dae(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_dae_prop
        self.min_chain_length = prop.min_chain_length
        self.import_units = prop.import_units
        self.custom_normals = prop.custom_normals
        self.fix_orientation = prop.fix_orientation
        self.find_chains = prop.find_chains
        self.auto_connect = prop.auto_connect
        self.keep_bind_info = prop.keep_bind_info


def register():
    bpy.utils.register_class(drag_import_dae_prop)
    bpy.types.Scene.drag_import_dae_prop = bpy.props.PointerProperty(type=drag_import_dae_prop)
    bpy.utils.register_class(Drag_import_dae_panel)
    bpy.utils.register_class(Drag_import_dae)


def unregister():
    bpy.utils.unregister_class(Drag_import_dae_panel)
    bpy.utils.unregister_class(Drag_import_dae)
    del bpy.types.Scene.drag_import_dae_prop
    bpy.utils.unregister_class(drag_import_dae_prop)
