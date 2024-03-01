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
        name='Scale',
        description="Value by which to enlarge or shrink the objects with respect to the world's origin",
        default=1.0
    )

    relative_path: BoolProperty(
        name='Relative Path',
        description='',
        default=True
    )
    set_frame_range: BoolProperty(
        name='Set Frame Range',
        description="Update the scene's start and end frame to match those of the abc archive",
        default=True
    )
    is_sequence: BoolProperty(
        name='Is Sequence',
        description='',
        default=False
    )
    validate_meshes: BoolProperty(
        name='Validate Meshes',
        description='',
        default=False
    )
    always_add_cache_reader: BoolProperty(
        name='Always Add Cache Reader',
        description='Add cache modifiers and constraints to imported objects even if they are not animated so that '
                    'they can be updated when reloading the Alembic archive',
        default=False
    )



from ..prop import drag_import_prop
class Drag_import_abc(bpy.types.Operator, drag_import_abc_prop,drag_import_prop):
    """Load a abc file"""
    bl_idname = 'drag_import.abc'
    bl_label = 'Import abc'
    bl_options = {'REGISTER', 'UNDO'}
    def draw(self, context):
        layout = self.layout.box()
        prop = context.scene.drag_import_abc_prop
        layout.label(text='Manual Transform')
        layout.prop(prop, "scale")
        option=self.layout.box()
        option.label(text='Options')
        option.prop(prop, "relative_path")
        option.prop(prop, "set_frame_range")
        option.prop(prop, "is_sequence")
        option.prop(prop, "validate_meshes")
        option.prop(prop, "always_add_cache_reader")

    def invoke(self, context, event):
        # 弹出菜单
        # return context.window_manager.invoke_props_dialog(self)
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        ret = {'CANCELLED'}
        # self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','pop_menu','files'))
        for f in self.files:
            bpy.ops.wm.alembic_import(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret

        # return self.import_abc(context)

    # def set_parameter(self, context):
    #     prop = context.scene.prop
    #     self.scale = prop.scale
    #     self.relative_path = prop.relative_path
    #     self.set_frame_range = prop.set_frame_range
    #     self.is_sequence = prop.is_sequence
    #     self.validate_meshes = prop.validate_meshes
    #     self.always_add_cache_reader = prop.always_add_cache_reader


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
