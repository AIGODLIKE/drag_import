import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)
from  ..prop import drag_import_prop

class drag_import_3ds_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    constrain_size: FloatProperty(
        name="Constrain Size",
        description="Scale the model by 10 until it reaches the "
                    "size constraint (0 to disable)",
        min=0.0, max=1000.0,
        soft_min=0.0, soft_max=1000.0,
        default=10.0,
    )
    use_scene_unit: BoolProperty(
        name="Scene Unit",
        description="Convert to scene unit length settings",
        default=False,
    )
    use_center_pivot: BoolProperty(
        name="Pivot Origin",
        description="Move all geometry to pivot origin",
        default=False,
    )
    use_image_search: BoolProperty(
        name="Image Search",
        description="Search subdirectories for any associated images "
                    "(Warning, may be slow)",
        default=True,
    )
    object_filter: EnumProperty(
        name="Object Filter", options={'ENUM_FLAG'},
        items=(('WORLD', "World".rjust(11), "", 'WORLD_DATA', 0x1),
               ('MESH', "Mesh".rjust(11), "", 'MESH_DATA', 0x2),
               ('LIGHT', "Light".rjust(12), "", 'LIGHT_DATA', 0x4),
               ('CAMERA', "Camera".rjust(11), "", 'CAMERA_DATA', 0x8),
               ('EMPTY', "Empty".rjust(11), "", 'EMPTY_AXIS', 0x10),
               ),
        description="Object types to import",
        default={'WORLD', 'MESH', 'LIGHT', 'CAMERA', 'EMPTY'},
    )
    use_apply_transform: BoolProperty(
        name="Apply Transform",
        description="Workaround for object transformations "
                    "importing incorrectly",
        default=True,
    )
    use_keyframes: BoolProperty(
        name="Animation",
        description="Read the keyframe data",
        default=True,
    )
    use_world_matrix: BoolProperty(
        name="World Space",
        description="Transform to matrix world",
        default=False,
    )
    use_cursor: BoolProperty(
        name="Cursor Origin",
        description="Read the 3D cursor location",
        default=False,
    )



class Drag_import_3ds(bpy.types.Operator, drag_import_3ds_prop,drag_import_prop):
    """Load a 3ds file"""
    bl_idname = 'drag_import.max3ds'
    bl_label = 'Import 3ds'
    bl_options = {'REGISTER','PRESET','UNDO'}
    def draw(self, context):
        layout = self.layout.box()
        prop = context.scene.drag_import_3ds_prop
        layout.label(text='Transform')
        row=layout.row(align=True)
        row.prop(prop, "use_image_search")
        row.label(text="", icon='OUTLINER_OB_IMAGE' if prop.use_image_search else 'IMAGE_DATA')
        layout.column().prop(prop, "object_filter")
        row = layout.row(align=True)
        row.prop(prop, "use_keyframes")
        row.label(text="", icon='ANIM' if prop.use_keyframes else 'DECORATE_DRIVER')
        row = layout.row(align=True)
        row.prop(prop, "use_cursor")
        row.label(text="", icon='PIVOT_CURSOR' if prop.use_cursor else 'CURSOR')

        trans = self.layout.box()
        trans.label(text='Transform')
        transrow=trans.row(align=True)
        transrow.prop(prop, "constrain_size")
        transrow = trans.row(align=True)
        transrow.prop(prop, "use_scene_unit")
        transrow.label(text="", icon='EMPTY_ARROWS' if prop.use_scene_unit else 'EMPTY_DATA')
        transrow = trans.row(align=True)
        transrow.prop(prop, "use_center_pivot")
        transrow.label(text="", icon='OVERLAY' if prop.use_center_pivot else 'PIVOT_ACTIVE')
        transrow = trans.row(align=True)
        transrow.prop(prop, "use_apply_transform")
        transrow.label(text="", icon='MESH_CUBE' if prop.use_apply_transform else 'MOD_SOLIDIFY')
        transrow = trans.row(align=True)
        transrow.prop(prop, "use_world_matrix")
        transrow.label(text="", icon='WORLD' if prop.use_world_matrix else 'META_BALL')
        trans.prop(prop, "axis_forward")
        trans.prop(prop, "axis_up")

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
            bpy.ops.import_scene.max3ds(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret

        # return self.import_3ds(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_3ds_prop

        self.constrain_size = prop.constrain_size
        self.use_scene_unit = prop.use_scene_unit
        self.use_center_pivot = prop.use_center_pivot
        self.use_image_search = prop.use_image_search
        self.object_filter = prop.object_filter
        self.use_apply_transform = prop.use_apply_transform
        self.use_keyframes = prop.use_keyframes
        self.use_world_matrix = prop.use_world_matrix
        self.use_cursor = prop.use_cursor



def register():
    bpy.utils.register_class(drag_import_3ds_prop)
    bpy.types.Scene.drag_import_3ds_prop = bpy.props.PointerProperty(type=drag_import_3ds_prop)
    # bpy.utils.register_class(Drag_import_3ds_panel)
    bpy.utils.register_class(Drag_import_3ds)


def unregister():
    # bpy.utils.unregister_class(Drag_import_3ds_panel)
    bpy.utils.unregister_class(Drag_import_3ds)
    del bpy.types.Scene.drag_import_3ds_prop
    bpy.utils.unregister_class(drag_import_3ds_prop)
