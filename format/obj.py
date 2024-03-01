import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)

from ..prop import drag_import_prop



class drag_import_obj_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    global_scale: FloatProperty(
        name='Scale',
        description="min chain length",
        default=1.0)

    clamp_size: FloatProperty(
        name='clamp size',
        description='',
        default=0.0
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
        default="NEGATIVE_Z"
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
        default="Y"
    )

    use_split_objects: BoolProperty(
        name='use split objects',
        description='',
        default=True
    )
    use_split_groups: BoolProperty(
        name='use split groups',
        description='',
        default=False
    )
    import_vertex_groups: BoolProperty(
        name='import vertex groups',
        description='',
        default=False
    )
    validate_meshes: BoolProperty(
        name='Validate Meshes',
        description='',
        default=False
    )



class Drag_import_obj(bpy.types.Operator, drag_import_obj_prop,drag_import_prop):
    """Load a obj file"""
    bl_idname = 'drag_import.obj'
    bl_label = 'Import obj'
    bl_options = {'REGISTER', 'PRESET','UNDO'}
    def draw(self, context):
        #包括
        layout = self.layout.box()
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        layout.label(text='Transform')
        # sfile = context.space_data
        # operator = sfile.active_operator
        prop = context.scene.drag_import_obj_prop
        layout.prop(prop, "global_scale")
        layout.prop(prop, "clamp_size")
        layout.prop(prop, "forward_axis")
        layout.prop(prop, "up_axis")
        sub = self.layout.box()
        sub.use_property_split = True
        sub.use_property_decorate = False  # No animation.
        sub.label(text='Options')
        sub.prop(prop, "use_split_objects")
        sub.prop(prop, "use_split_groups")
        sub.prop(prop, "import_vertex_groups")
        sub.prop(prop, "validate_meshes")

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
            bpy.ops.wm.obj_import(filepath=f.name, **keywords)
        # if bpy.ops.wm.obj_import(filepath=self.filepath, **keywords) == {'FINISHED'}:
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
    # bpy.utils.register_class(Drag_import_obj_panel)
    bpy.utils.register_class(Drag_import_obj)


def unregister():
    # bpy.utils.unregister_class(Drag_import_obj_panel)
    bpy.utils.unregister_class(Drag_import_obj)
    del bpy.types.Scene.drag_import_obj_prop
    bpy.utils.unregister_class(drag_import_obj_prop)
