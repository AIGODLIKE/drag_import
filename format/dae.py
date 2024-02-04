import bpy
from bpy.props import (
    BoolProperty,

    IntProperty,
    StringProperty,

)
from  ..prop import drag_import_prop

class drag_import_dae_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    min_chain_length: IntProperty(
        name='Minimum Chain Length',
        description="When searching Bone Chains disregard chains of length below this value")

    import_units: BoolProperty(
        name='Import Units',
        description="If disabled match import to Blender's current Unit settings otherwise use the settings from the Imported scene",
        default=False
    )
    custom_normals: BoolProperty(
        name='Custom Normals',
        description='Import custom normals, if available (otherwise Blender will recompute them)',
        default=True
    )
    fix_orientation: BoolProperty(
        name='Fix Leaf Bones',
        description='Fix Orientation of Leaf Bones (Collada does only support Joints)',
        default=False
    )
    find_chains: BoolProperty(
        name='Find Bone Chains',
        description='Find best matching Bone Chains and ensure bones in chain are connected',
        default=False
    )
    auto_connect: BoolProperty(
        name='Auto Connect',
        description='Set use_connect for parent bones which have exactly one child bone',
        default=False
    )
    keep_bind_info: BoolProperty(
        name='Keep Bind Info',
        description='Store Bindpose information in custom bone properties for later use during Collada export',
        default=False
    )



class Drag_import_dae(bpy.types.Operator,drag_import_dae_prop,drag_import_prop):
    """Load a dae file"""
    bl_idname = 'drag_import.dae'
    bl_label = 'Import dae'
    bl_options = {'REGISTER','PRESET','UNDO'}

    def draw(self, context):
        prop = context.scene.drag_import_dae_prop
        layout = self.layout.box()
        layout.label(text='Import Data Options')
        layout.prop(prop, "import_units")
        layout.prop(prop, "custom_normals")
        arma=self.layout.box()
        arma.label(text='Armature Options')
        arma.prop(prop, "fix_orientation")
        arma.prop(prop, "find_chains")
        arma.prop(prop, "auto_connect")
        arma.prop(prop, "min_chain_length")
        sub=self.layout.box()
        sub.prop(prop, "keep_bind_info")
    def invoke(self, context, event):
        # 弹出菜单
        # return context.window_manager.invoke_props_dialog(self)
        # print('tanchucaidan',self.pop_menu and not self.pop_once)
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        # ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        for f in self.files:
            bpy.ops.wm.collada_import(filepath=f.name, **keywords)
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
    # bpy.utils.register_class(Drag_import_dae_panel)
    bpy.utils.register_class(Drag_import_dae)


def unregister():
    # bpy.utils.unregister_class(Drag_import_dae_panel)
    bpy.utils.unregister_class(Drag_import_dae)
    del bpy.types.Scene.drag_import_dae_prop
    bpy.utils.unregister_class(drag_import_dae_prop)
