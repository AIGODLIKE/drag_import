import bpy
from bpy.props import (
        StringProperty,
        BoolProperty,
        FloatProperty,
        EnumProperty,
        CollectionProperty,
        )
from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        orientation_helper,
        axis_conversion,
        )
from ..prop import drag_import_prop
class drag_import_fbx_prop(bpy.types.PropertyGroup):
    filter_glob: StringProperty(default="*.fbx", options={'HIDDEN'})

    filepath: StringProperty(
        name="File Path",
    )
    global_scale: FloatProperty(
        name="Scale",
        min=0.001, max=1000.0,
        default=1.0,
    )
    ui_tab: EnumProperty(
        items=(('MAIN', "Main", "Main basic settings"),
               ('ARMATURE', "Armatures", "Armature-related settings"),
               ),
        name="ui_tab",
        description="Import options categories",
    )

    use_manual_orientation: BoolProperty(
        name="Manual Orientation",
        description="Specify orientation and scale, instead of using embedded data in FBX file",
        default=False,
    )
    axis_forward: EnumProperty(
        name="Forward Axis",
        items=(('X', "X Axis", ""),
               ('Y', "Y Axis", ""),
               ('Z', "Z Axis", ""),
               ('-X', "-X Axis", ""),
               ('-Y', "-Y Axis", ""),
               ('-Z', "-Z Axis", ""),
               ),
        default='-Z',
    )
    axis_up: EnumProperty(
        name="Up Axis",
        items=(('X', "X Axis", ""),
               ('Y', "Y Axis", ""),
               ('Z', "Z Axis", ""),
               ('-X', "-X Axis", ""),
               ('-Y', "-Y Axis", ""),
               ('-Z', "-Z Axis", ""),
               ),
        default='Y',
    )
    bake_space_transform: BoolProperty(
        name="Apply Transform",
        description="Bake space transform into object data, avoids getting unwanted rotations to objects when target space is not aligned with Blender's space (WARNING! experimental option, use at own risk, known to be broken with armatures/animations)",
        default=False,
    )

    use_custom_normals: BoolProperty(
        name="Custom Normals",
        description="Import custom normals, if available (otherwise Blender will recompute them)",
        default=True,
    )
    colors_type: EnumProperty(
        name="Vertex Colors",
        items=(('NONE', "None", "Do not import color attributes"),
               ('SRGB', "sRGB", "Expect file colors in sRGB color space"),
               ('LINEAR', "Linear", "Expect file colors in linear color space"),
               ),
        description="Import vertex color attributes",
        default='SRGB',
    )

    use_image_search: BoolProperty(
        name="Image Search",
        description="Search subdirs for any associated images (WARNING: may be slow)",
        default=True,
    )

    use_alpha_decals: BoolProperty(
        name="Alpha Decals",
        description="Treat materials with alpha as decals (no shadow casting)",
        default=False,
    )
    decal_offset: FloatProperty(
        name="Decal Offset",
        description="Displace geometry of alpha meshes",
        min=0.0, max=1.0,
        default=0.0,
    )

    use_anim: BoolProperty(
        name="Import Animation",
        description="Import FBX animation",
        default=True,
    )
    anim_offset: FloatProperty(
        name="Animation Offset",
        description="Offset to apply to animation during import, in frames",
        default=1.0,
    )

    use_subsurf: BoolProperty(
        name="Subdivision Data",
        description="Import FBX subdivision information as subdivision surface modifiers",
        default=False,
    )

    use_custom_props: BoolProperty(
        name="Custom Properties",
        description="Import user properties as custom properties",
        default=True,
    )
    use_custom_props_enum_as_string: BoolProperty(
        name="Import Enums As Strings",
        description="Store enumeration values as strings",
        default=True,
    )

    ignore_leaf_bones: BoolProperty(
        name="Ignore Leaf Bones",
        description="Ignore the last bone at the end of each chain (used to mark the length of the previous bone)",
        default=False,
    )
    force_connect_children: BoolProperty(
        name="Force Connect Children",
        description="Force connection of children bones to their parent, even if their computed head/tail positions do not match (can be useful with pure-joints-type armatures)",
        default=False,
    )
    automatic_bone_orientation: BoolProperty(
        name="Automatic Bone Orientation",
        description="Try to align the major bone axis with the bone children",
        default=False,
    )
    primary_bone_axis: EnumProperty(
        name="Primary Bone Axis",
        items=(('X', "X Axis", ""),
               ('Y', "Y Axis", ""),
               ('Z', "Z Axis", ""),
               ('-X', "-X Axis", ""),
               ('-Y', "-Y Axis", ""),
               ('-Z', "-Z Axis", ""),
               ),
        default='Y',
    )
    secondary_bone_axis: EnumProperty(
        name="Secondary Bone Axis",
        items=(('X', "X Axis", ""),
               ('Y', "Y Axis", ""),
               ('Z', "Z Axis", ""),
               ('-X', "-X Axis", ""),
               ('-Y', "-Y Axis", ""),
               ('-Z', "-Z Axis", ""),
               ),
        default='X',
    )

    use_prepost_rot: BoolProperty(
        name="Use Pre/Post Rotation",
        description="Use pre/post rotation from FBX transform (you may have to disable that in some cases)",
        default=True,
    )

@orientation_helper(axis_forward='-Z', axis_up='Y')
class Drag_import_fbx(bpy.types.Operator,drag_import_fbx_prop,drag_import_prop):
    """Load a FBX file"""
    bl_idname = "drag_import.fbx"
    bl_label = "Import FBX"
    bl_options = {'UNDO', 'PRESET','REGISTER'}


    def draw(self, context):
        #包括
        layout = self.layout.box()
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        layout.label(text='Include')
        # sfile = context.space_data
        # operator = sfile.active_operator
        prop = context.scene.drag_import_fbx_prop
        layout.prop(prop, "use_custom_normals")
        layout.prop(prop, "use_subsurf")
        layout.prop(prop, "use_custom_props")
        sub = layout.row()
        sub.enabled = prop.use_custom_props
        sub.prop(prop, "use_custom_props_enum_as_string")
        layout.prop(prop, "use_image_search")
        layout.prop(prop, "colors_type")

        #变换
        trans= self.layout.box()
        trans.label(text='Transform')
        trans.prop(prop, "global_scale")
        trans.prop(prop, "decal_offset")
        row = trans.row()
        row.prop(prop, "bake_space_transform")
        row.label(text="", icon='ERROR')
        trans.prop(prop, "use_prepost_rot")
        trans.prop(prop, "use_manual_orientation")

        manual_orientation=trans.column()

        manual_orientation.prop(prop, "axis_forward")
        manual_orientation.prop(prop, "axis_up")
        manual_orientation.enabled = prop.use_manual_orientation
        anim=self.layout.box()
        anim.label(text='Animation')
        anim.prop(prop, "use_anim",)
        anim_sub=anim.row()
        anim_sub.prop(prop, "anim_offset")
        anim_sub.enabled = prop.use_anim
        arm=self.layout.box()
        arm.label(text='Armature')
        arm.prop(prop, "ignore_leaf_bones")
        arm.prop(prop, "force_connect_children"),
        arm.prop(prop, "automatic_bone_orientation"),
        sub = arm.column()
        sub.enabled = not prop.automatic_bone_orientation
        sub.prop(prop, "primary_bone_axis")
        sub.prop(prop, "secondary_bone_axis")
    def invoke(self, context, event):
        # 弹出菜单
        # return context.window_manager.invoke_props_dialog(self)
        # print('tanchucaidan',self.pop_menu and not self.pop_once)
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def set_parameter(self, context):
        # self.files=bpy.context.scene.drag_import_prop.files
        from pprint import pprint
        print('scene prop')
        pprint(bpy.context.scene.drag_import_prop.files)
        print('fbx ops')
        pprint(self.files)
        prop = context.scene.drag_import_fbx_prop
        self.ui_tab = prop.ui_tab
        self.use_manual_orientation = prop.use_manual_orientation
        self.axis_forward = prop.axis_forward
        self.axis_up = prop.axis_up
        self.global_scale = prop.global_scale
        self.bake_space_transform = prop.bake_space_transform
        self.use_custom_normals = prop.use_custom_normals
        self.colors_type = prop.colors_type
        self.use_image_search = prop.use_image_search
        self.use_alpha_decals = prop.use_alpha_decals
        self.decal_offset = prop.decal_offset
        self.use_anim = prop.use_anim
        self.anim_offset = prop.anim_offset
        self.use_subsurf = prop.use_subsurf
        self.use_custom_props = prop.use_custom_props
        self.use_custom_props_enum_as_string = prop.use_custom_props_enum_as_string
        self.ignore_leaf_bones = prop.ignore_leaf_bones
        self.force_connect_children = prop.force_connect_children
        self.automatic_bone_orientation = prop.automatic_bone_orientation
        self.primary_bone_axis = prop.primary_bone_axis
        self.secondary_bone_axis = prop.secondary_bone_axis
        self.use_prepost_rot = prop.use_prepost_rot
    def execute(self, context):

        self.set_parameter(context)
        keywords = self.as_keywords(ignore=("filter_glob", "directory", "ui_tab", "filepath","pop_menu",'files'))
        print('files_fbx:',self.files)
        for f in self.files:
            print(f)
        print('path',self.filepath)

        ret = {'CANCELLED'}

        from io_scene_fbx import import_fbx
        for file in self.files:
            if import_fbx.load(self,context,filepath=file.name, **keywords) == {'FINISHED'}:
                ret = {'FINISHED'}
        return ret


#
# classes=[
#     Drag_import_fbx,
# ]
def register():
    bpy.utils.register_class(drag_import_fbx_prop)
    bpy.types.Scene.drag_import_fbx_prop = bpy.props.PointerProperty(type=drag_import_fbx_prop)
    # bpy.utils.register_class(Drag_import_fbx_panel)
    bpy.utils.register_class(Drag_import_fbx)


def unregister():
    # bpy.utils.unregister_class(Drag_import_fbx_panel)
    bpy.utils.unregister_class(Drag_import_fbx)
    del bpy.types.Scene.drag_import_fbx_prop
    bpy.utils.unregister_class(drag_import_fbx_prop)