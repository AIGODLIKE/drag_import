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


@orientation_helper(axis_forward='-Z', axis_up='Y')
class Drag_import_fbx(bpy.types.Operator):
    """Load a FBX file"""
    bl_idname = "drag_imort.fbx"
    bl_label = "Import FBX"
    bl_options = {'UNDO', 'PRESET'}

    directory: StringProperty()

    filename_ext = ".fbx"
    filter_glob: StringProperty(default="*.fbx", options={'HIDDEN'})

    filepath: StringProperty(
            name="File Path",
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
    global_scale: FloatProperty(
            name="Scale",
            min=0.001, max=1000.0,
            default=1.0,
            )
    bake_space_transform: BoolProperty(
            name="Apply Transform",
            description="Bake space transform into object data, avoids getting unwanted rotations to objects when "
                        "target space is not aligned with Blender's space "
                        "(WARNING! experimental option, use at own risk, known to be broken with armatures/animations)",
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
            description="Force connection of children bones to their parent, even if their computed head/tail "
                        "positions do not match (can be useful with pure-joints-type armatures)",
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

    def draw(self, context):
        pass

    def execute(self, context):
        keywords = self.as_keywords(ignore=("filter_glob", "directory", "ui_tab", "filepath",))

        # from . import import_fbx
        import os
        print('path',self.filepath)
        if self.filepath:
            ret = {'CANCELLED'}
            # dirname = os.path.dirname(self.filepath)
            # for file in self.filepath:
                # path = os.path.join(dirname, file.name)
                # if import_fbx.load(self, context, filepath=path, **keywords) == {'FINISHED'}:
            if bpy.ops.import_scene.fbx(filepath=self.filepath, **keywords) == {'FINISHED'}:
                    ret = {'FINISHED'}
            return ret



class FBX_PT_import_include(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Include"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "IMPORT_SCENE_OT_fbx"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, "use_custom_normals")
        layout.prop(operator, "use_subsurf")
        layout.prop(operator, "use_custom_props")
        sub = layout.row()
        sub.enabled = operator.use_custom_props
        sub.prop(operator, "use_custom_props_enum_as_string")
        layout.prop(operator, "use_image_search")
        layout.prop(operator, "colors_type")


class FBX_PT_import_transform(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Transform"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "IMPORT_SCENE_OT_fbx"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        # sfile = context.space_data
        # operator = sfile.active_operator
        operator = bpy.ops.import_scene.fbx

        layout.prop(operator, "global_scale")
        layout.prop(operator, "decal_offset")
        row = layout.row()
        row.prop(operator, "bake_space_transform")
        row.label(text="", icon='ERROR')
        layout.prop(operator, "use_prepost_rot")


class FBX_PT_import_transform_manual_orientation(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Manual Orientation"
    bl_parent_id = "FBX_PT_import_transform"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "IMPORT_SCENE_OT_fbx"

    def draw_header(self, context):
        sfile = context.space_data
        operator = sfile.active_operator

        self.layout.prop(operator, "use_manual_orientation", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.enabled = operator.use_manual_orientation

        layout.prop(operator, "axis_forward")
        layout.prop(operator, "axis_up")


class FBX_PT_import_animation(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Animation"
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "IMPORT_SCENE_OT_fbx"

    def draw_header(self, context):
        sfile = context.space_data
        operator = sfile.active_operator

        self.layout.prop(operator, "use_anim", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.enabled = operator.use_anim

        layout.prop(operator, "anim_offset")


class FBX_PT_import_armature(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Armature"
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "IMPORT_SCENE_OT_fbx"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, "ignore_leaf_bones")
        layout.prop(operator, "force_connect_children"),
        layout.prop(operator, "automatic_bone_orientation"),
        sub = layout.column()
        sub.enabled = not operator.automatic_bone_orientation
        sub.prop(operator, "primary_bone_axis")
        sub.prop(operator, "secondary_bone_axis")
classes=[
    Drag_import_fbx,
]
def register():

    from bpy.utils import register_class
    for c in classes:
        register_class(c)
    pass



def unregister():

    from bpy.utils import unregister_class
    for c in classes:
        unregister_class(c)
    pass
