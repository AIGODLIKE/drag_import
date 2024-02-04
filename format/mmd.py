import bpy
from bpy.props import (
    BoolProperty,
    StringProperty,

)

from ..prop import drag_import_prop

# try:
#     try:
#         from cats.extern_tools.mmd_tools_local import DictionaryEnum
#     except:
#         print('如果有cats插件请将cats文件夹改名为cats!')
#     from mmd_tools.translations import DictionaryEnum
# except:
#     print('如果有mmd插件请将mmd文件夹改为mmd!')
def _update_types(cls, prop):
    types = cls.types.copy()

    if 'PHYSICS' in types:
        types.add('ARMATURE')
    if 'DISPLAY' in types:
        types.add('ARMATURE')
    if 'MORPHS' in types:
        types.add('ARMATURE')
        types.add('MESH')

    if types != cls.types:
        cls.types = types # trigger update

LOG_LEVEL_ITEMS = [
    ('DEBUG', '4. DEBUG', '', 1),
    ('INFO', '3. INFO', '', 2),
    ('WARNING', '2. WARNING', '', 3),
    ('ERROR', '1. ERROR', '', 4),
]

class drag_import_pmx_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()
    ik_loop_factor: bpy.props.IntProperty(
        name='IK Loop Factor',
        description='Scaling factor of MMD IK loop',
        min=1,
        soft_max=10, max=100,
        default=5,
    )

    types: bpy.props.EnumProperty(
        name='Types',
        description='Select which parts will be imported',
        options={'ENUM_FLAG'},
        items = [
            ('MESH', 'Mesh', 'Mesh', 1),
            ('ARMATURE', 'Armature', 'Armature', 2),
            ('PHYSICS', 'Physics', 'Rigidbodies and joints (include Armature)', 4),
            ('DISPLAY', 'Display', 'Display frames (include Armature)', 8),
            ('MORPHS', 'Morphs', 'Morphs (include Armature and Mesh)', 16),
        ],
        default={'MESH', 'ARMATURE', 'PHYSICS', 'DISPLAY', 'MORPHS',},
        update=_update_types,
    )
    scale: bpy.props.FloatProperty(
        name='Scale',
        description='Scaling factor for importing the model',
        default=0.08,
    )
    clean_model: bpy.props.BoolProperty(
        name='Clean Model',
        description='Remove unused vertices and duplicated/invalid faces',
        default=True,
    )
    remove_doubles: bpy.props.BoolProperty(
        name='Remove Doubles',
        description='Merge duplicated vertices and faces',
        default=False,
    )
    fix_IK_links: bpy.props.BoolProperty(
        name='Fix IK Links',
        description='Fix IK links to be blender suitable',
        default=False,
    )

    apply_bone_fixed_axis: bpy.props.BoolProperty(
        name='Apply Bone Fixed Axis',
        description="Apply bone's fixed axis to be blender suitable",
        default=False,
    )
    rename_bones: bpy.props.BoolProperty(
        name='Rename Bones - L / R Suffix',
        description='Use Blender naming conventions for Left / Right paired bones',
        default=True,
    )
    use_underscore: bpy.props.BoolProperty(
        name="Rename Bones - Use Underscore",
        description='Will not use dot, e.g. if renaming bones, will use _R instead of .R',
        default=False,
    )
    use_mipmap: bpy.props.BoolProperty(
        name='use MIP maps for UV textures',
        description='Specify if mipmaps will be generated',
        default=True,
    )
    dictionary: bpy.props.EnumProperty(
        name='Rename Bones To English',
        items=(
            ('DISABLED', 'Disabled',''),
            ('INTERNAL', 'Internal Dictionary', ''),
        ),
        # items=DictionaryEnum.get_dictionary_items,
        description='Translate bone names from Japanese to English using selected dictionary',
    )
    sph_blend_factor: bpy.props.FloatProperty(
        name='influence of .sph textures',
        description='The diffuse color factor of texture slot for .sph textures',
        default=1.0,
    )
    spa_blend_factor: bpy.props.FloatProperty(
        name='influence of .spa textures',
        description='The diffuse color factor of texture slot for .spa textures',
        default=1.0,
    )
    log_level: bpy.props.EnumProperty(
        name='Log level',
        description='Select log level',
        items=LOG_LEVEL_ITEMS,
        default='INFO',
    )
    save_log: bpy.props.BoolProperty(
        name='Create a log file',
        description='Create a log file',
        default=False,
    )
class drag_import_vpd_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()


    scale: bpy.props.FloatProperty(
        name='Scale',
        description='Scaling factor for importing the pose',
        default=0.08,
    )
    bone_mapper: bpy.props.EnumProperty(
        name='Bone Mapper',
        description='Select bone mapper',
        items=[
            ('BLENDER', 'Blender', 'Use blender bone name', 0),
            ('PMX', 'PMX', 'Use japanese name of MMD bone', 1),
            ('RENAMED_BONES', 'Renamed bones', 'Rename the bone of pose data to be blender suitable', 2),
        ],
        default='PMX',
    )
    rename_bones: bpy.props.BoolProperty(
        name='Rename Bones - L / R Suffix',
        description='Use Blender naming conventions for Left / Right paired bones',
        default=True,
    )
    use_underscore: bpy.props.BoolProperty(
        name="Rename Bones - Use Underscore",
        description='Will not use dot, e.g. if renaming bones, will use _R instead of .R',
        default=False,
    )
    dictionary: bpy.props.EnumProperty(
        name='Dictionary',
        items=(
            ('DISABLED', 'Disabled',''),
            ('INTERNAL', 'Internal Dictionary', ''),
        ),
        # items=DictionaryEnum.get_dictionary_items,
        description='Translate bone names from Japanese to English using selected dictionary',
    )
    use_pose_mode: bpy.props.BoolProperty(
        name='Treat Current Pose as Rest Pose',
        description='You can pose the model to fit the original pose of a pose data, such as T-Pose or A-Pose',
        default=False,
        options={'SKIP_SAVE'},
    )
class drag_import_vmd_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()


    scale: bpy.props.FloatProperty(
        name='Scale',
        description='Scaling factor for importing the motion',
        default=0.08,
    )
    margin: bpy.props.IntProperty(
        name='Margin',
        description='How many frames added before motion starting',
        min=0,
        default=5,
    )
    bone_mapper: bpy.props.EnumProperty(
        name='Bone Mapper',
        description='Select bone mapper',
        items=[
            ('BLENDER', 'Blender', 'Use blender bone name', 0),
            ('PMX', 'PMX', 'Use japanese name of MMD bone', 1),
            ('RENAMED_BONES', 'Renamed bones', 'Rename the bone of motion data to be blender suitable', 2),
        ],
        default='PMX',
    )
    rename_bones: bpy.props.BoolProperty(
        name='Rename Bones - L / R Suffix',
        description='Use Blender naming conventions for Left / Right paired bones',
        default=True,
    )
    use_underscore: bpy.props.BoolProperty(
        name="Rename Bones - Use Underscore",
        description='Will not use dot, e.g. if renaming bones, will use _R instead of .R',
        default=False,
    )
    dictionary: bpy.props.EnumProperty(
        name='Rename Bones To English',
        items=(
            ('DISABLED', 'Disabled',''),
            ('INTERNAL', 'Internal Dictionary', ''),
        ),
        # items=DictionaryEnum.get_dictionary_items,
        description='Translate bone names from Japanese to English using selected dictionary',
    )
    use_pose_mode: bpy.props.BoolProperty(
        name='Treat Current Pose as Rest Pose',
        description='You can pose the model to fit the original pose of a motion data, such as T-Pose or A-Pose',
        default=False,
        options={'SKIP_SAVE'},
    )
    use_mirror: bpy.props.BoolProperty(
        name='Mirror Motion',
        description='Import the motion by using X-Axis mirror',
        default=False,
    )
    update_scene_settings: bpy.props.BoolProperty(
        name='Update scene settings',
        description='Update frame range and frame rate (30 fps)',
        default=True,
    )
class drag_import_vpd2102(bpy.types.Operator, drag_import_vpd_prop,drag_import_prop):
    """Load a vpd file"""
    bl_idname = 'drag_import.vpd2102'
    bl_label = 'Import vmd'
    bl_options = {'REGISTER', 'PRESET','UNDO'}



    def draw(self, context):
        prop = context.scene.drag_import_vpd_prop
        layout = self.layout
        layout.prop(prop, 'scale')

        layout.prop(prop, 'bone_mapper')
        if prop.bone_mapper == 'RENAMED_BONES':
            layout.prop(prop, 'rename_bones')
            layout.prop(prop, 'use_underscore')
            layout.prop(prop, 'dictionary')
        layout.prop(prop, 'use_pose_mode')


    def invoke(self, context, event):
        # 弹出菜单
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        for f in self.files:
            bpy.ops.mmd_tools.import_vpd(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret


    def set_parameter(self, context):
        prop = context.scene.drag_import_pmx_prop
        self.scale = prop.scale
        self.bone_mapper = prop.bone_mapper
        self.rename_bones = prop.rename_bones
        self.use_underscore = prop.use_underscore
        self.dictionary = prop.dictionary
        self.use_pose_mode = prop.use_pose_mode
        # self.update_scene_settings = prop.update_scene_settings
class drag_import_vpd0190(bpy.types.Operator, drag_import_vpd_prop,drag_import_prop):
    """Load a vpd file"""
    bl_idname = 'drag_import.vpd0190'
    bl_label = 'Import vmd'
    bl_options = {'REGISTER', 'PRESET','UNDO'}


    def draw(self, context):
        prop = context.scene.drag_import_vpd_prop
        layout = self.layout
        layout.prop(prop, 'scale')

        layout.prop(prop, 'bone_mapper')
        if prop.bone_mapper == 'RENAMED_BONES':
            layout.prop(prop, 'rename_bones')
            layout.prop(prop, 'use_underscore')
            layout.prop(prop, 'dictionary')
        layout.prop(prop, 'use_pose_mode')


    def invoke(self, context, event):
        # 弹出菜单
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        for f in self.files:
            bpy.ops.mmd_tools.import_vpd(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret


    def set_parameter(self, context):
        prop = context.scene.drag_import_pmx_prop
        self.scale = prop.scale
        self.bone_mapper = prop.bone_mapper
        self.rename_bones = prop.rename_bones
        self.use_underscore = prop.use_underscore
        self.dictionary = prop.dictionary
        self.use_pose_mode = prop.use_pose_mode
class drag_import_vmd2102(bpy.types.Operator, drag_import_vmd_prop,drag_import_prop):
    """Load a vmd file"""
    bl_idname = 'drag_import.vmd2102'
    bl_label = 'Import vmd'
    bl_options = {'REGISTER', 'PRESET','UNDO'}
    use_NLA: bpy.props.BoolProperty(
        name='Use NLA',
        description='Import the motion as NLA strips',
        default=False,
    )

    def draw(self, context):
        prop = context.scene.drag_import_pmx_prop
        layout = self.layout.box()
        layout.prop(prop, 'scale')
        layout.prop(prop, 'margin')
        layout.prop(self, 'use_NLA')

        layout.prop(prop, 'bone_mapper')
        if prop.bone_mapper == 'RENAMED_BONES':
            layout.prop(prop, 'rename_bones')
            layout.prop(prop, 'use_underscore')
            layout.prop(prop, 'dictionary')
        layout.prop(prop, 'use_pose_mode')
        layout.prop(prop, 'use_mirror')

        layout.prop(prop, 'update_scene_settings')


    def invoke(self, context, event):
        # 弹出菜单
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        for f in self.files:
            bpy.ops.mmd_tools.import_vmd(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret


    def set_parameter(self, context):
        prop = context.scene.drag_import_pmx_prop
        self.margin = prop.margin
        self.scale = prop.scale
        self.bone_mapper = prop.bone_mapper
        self.rename_bones = prop.rename_bones
        self.use_underscore = prop.use_underscore
        self.dictionary = prop.dictionary
        self.use_pose_mode = prop.use_pose_mode
        self.use_mirror = prop.use_mirror
        self.update_scene_settings = prop.update_scene_settings
class drag_import_vmd0190(bpy.types.Operator, drag_import_vmd_prop,drag_import_prop):
    """Load a vmd file"""
    bl_idname = 'drag_import.vmd0190'
    bl_label = 'Import vmd'
    bl_options = {'REGISTER', 'PRESET','UNDO'}


    def draw(self, context):
        prop = context.scene.drag_import_pmx_prop
        layout = self.layout.box()
        layout.prop(prop, 'scale')
        layout.prop(prop, 'margin')
        layout.prop(prop, 'bone_mapper')
        if prop.bone_mapper == 'RENAMED_BONES':
            layout.prop(prop, 'rename_bones')
            layout.prop(prop, 'use_underscore')
            layout.prop(prop, 'dictionary')
        layout.prop(prop, 'use_pose_mode')
        layout.prop(prop, 'use_mirror')

        layout.prop(prop, 'update_scene_settings')


    def invoke(self, context, event):
        # 弹出菜单
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        for f in self.files:
            bpy.ops.mmd_tools.import_vmd(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret


    def set_parameter(self, context):
        prop = context.scene.drag_import_pmx_prop
        self.margin = prop.margin
        self.scale = prop.scale
        self.bone_mapper = prop.bone_mapper
        self.rename_bones = prop.rename_bones
        self.use_underscore = prop.use_underscore
        self.dictionary = prop.dictionary
        self.use_pose_mode = prop.use_pose_mode
        self.use_mirror = prop.use_mirror
        self.update_scene_settings = prop.update_scene_settings
class drag_import_pmx2102(bpy.types.Operator, drag_import_pmx_prop,drag_import_prop):
    """Load a pmx file"""
    bl_idname = 'drag_import.pmx2102'
    bl_label = 'Import pmx'
    bl_options = {'REGISTER', 'PRESET','UNDO'}

    def draw(self, context):
        #包括
        layout = self.layout.box()
        prop = context.scene.drag_import_pmx_prop
        layout.prop(prop, "types")
        layout.prop(prop, "scale")
        layout.prop(prop, "clean_model")
        layout.prop(prop, "remove_doubles")
        layout.prop(prop, "fix_IK_links")

        layout.prop(prop, "ik_loop_factor")

        layout.prop(prop, "apply_bone_fixed_axis")
        layout.prop(prop, "rename_bones")
        layout.prop(prop, "use_underscore")
        layout.prop(prop, "dictionary")

        layout.prop(prop, "use_mipmap")
        layout.prop(prop, "sph_blend_factor")
        layout.prop(prop, "spa_blend_factor")
        layout.prop(prop, "log_level")
        layout.prop(prop, "save_log")


    def invoke(self, context, event):
        # 弹出菜单
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        for f in self.files:
            bpy.ops.mmd_tools.import_model(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret


    def set_parameter(self, context):
        prop = context.scene.drag_import_pmx_prop
        self.types = prop.types
        self.scale = prop.scale
        self.clean_model = prop.clean_model
        self.remove_doubles = prop.remove_doubles
        self.fix_IK_links = prop.fix_IK_links
        self.apply_bone_fixed_axis = prop.apply_bone_fixed_axis
        self.rename_bones = prop.rename_bones
        self.use_underscore = prop.use_underscore
        self.use_mipmap = prop.use_mipmap
        self.dictionary = prop.dictionary
        self.sph_blend_factor = prop.sph_blend_factor
        self.spa_blend_factor = prop.spa_blend_factor
        self.log_level = prop.log_level
        self.save_log = prop.save_log
        self.ik_loop_factor = prop.ik_loop_factor
class drag_import_pmx0190(bpy.types.Operator, drag_import_pmx_prop,drag_import_prop):
    """Load a pmx file"""
    bl_idname = 'drag_import.pmx0190'
    bl_label = 'Import pmx'
    bl_options = {'REGISTER', 'PRESET','UNDO'}
    def draw(self, context):
        #包括
        layout = self.layout.box()
        prop = context.scene.drag_import_pmx_prop
        layout.prop(prop, "types")
        layout.prop(prop, "scale")
        layout.prop(prop, "clean_model")
        layout.prop(prop, "remove_doubles")
        layout.prop(prop, "fix_IK_links")

        # layout.prop(prop, "ik_loop_factor")

        layout.prop(prop, "apply_bone_fixed_axis")
        layout.prop(prop, "rename_bones")
        layout.prop(prop, "use_underscore")
        layout.prop(prop, "dictionary")

        layout.prop(prop, "use_mipmap")
        layout.prop(prop, "sph_blend_factor")
        layout.prop(prop, "spa_blend_factor")
        layout.prop(prop, "log_level")
        layout.prop(prop, "save_log")


    def invoke(self, context, event):
        # 弹出菜单
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu','ik_loop_factor'))
        for f in self.files:
            bpy.ops.mmd_tools.import_model(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret


    def set_parameter(self, context):
        prop = context.scene.drag_import_pmx_prop
        self.types = prop.types
        self.scale = prop.scale
        self.clean_model = prop.clean_model
        self.remove_doubles = prop.remove_doubles
        self.fix_IK_links = prop.fix_IK_links
        # self.ik_loop_factor = prop.ik_loop_factor
        self.apply_bone_fixed_axis = prop.apply_bone_fixed_axis
        self.rename_bones = prop.rename_bones
        self.use_underscore = prop.use_underscore
        self.use_mipmap = prop.use_mipmap
        self.dictionary = prop.dictionary
        self.sph_blend_factor = prop.sph_blend_factor
        self.spa_blend_factor = prop.spa_blend_factor
        self.log_level = prop.log_level
        self.save_log = prop.save_log


def register():
    bpy.utils.register_class(drag_import_pmx_prop)
    bpy.utils.register_class(drag_import_vmd_prop)
    bpy.utils.register_class(drag_import_vpd_prop)
    bpy.types.Scene.drag_import_pmx_prop = bpy.props.PointerProperty(type=drag_import_pmx_prop)
    bpy.types.Scene.drag_import_vmd_prop = bpy.props.PointerProperty(type=drag_import_vmd_prop)
    bpy.types.Scene.drag_import_vpd_prop = bpy.props.PointerProperty(type=drag_import_vpd_prop)
    bpy.utils.register_class(drag_import_vpd2102)
    bpy.utils.register_class(drag_import_vmd2102)
    bpy.utils.register_class(drag_import_pmx2102)
    bpy.utils.register_class(drag_import_vpd0190)
    bpy.utils.register_class(drag_import_vmd0190)
    bpy.utils.register_class(drag_import_pmx0190)
    # bpy.utils.register_class(Drag_import_vrma)


def unregister():
    bpy.utils.unregister_class(drag_import_vpd2102)
    bpy.utils.unregister_class(drag_import_vmd2102)
    bpy.utils.unregister_class(drag_import_pmx2102)
    bpy.utils.unregister_class(drag_import_vmd0190)
    bpy.utils.unregister_class(drag_import_vpd0190)
    bpy.utils.unregister_class(drag_import_pmx0190)
    # bpy.utils.unregister_class(Drag_import_vrma)
    del bpy.types.Scene.drag_import_pmx_prop
    del bpy.types.Scene.drag_import_vmd_prop
    del bpy.types.Scene.drag_import_vpd_prop
    bpy.utils.unregister_class(drag_import_pmx_prop)
    bpy.utils.unregister_class(drag_import_vmd_prop)
    bpy.utils.unregister_class(drag_import_vpd_prop)
