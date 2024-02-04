import bpy
from bpy.props import (
    BoolProperty,
    StringProperty,

)

from ..prop import drag_import_prop


class drag_import_vrm_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()


    extract_textures_into_folder: BoolProperty(
        name='extract textures into folder',
        description='',
        default=False
    )
    make_new_texture_folder: BoolProperty(
        name='make new texture folder',
        description='',
        default=True
    )
    set_shading_type_to_material_on_import: BoolProperty(
        name='set shading type to material on import',
        description='',
        default=True
    )
    set_view_transform_to_standard_on_import: BoolProperty(
        name='set view transform to standard on import',
        description='',
        default=True
    )
    set_armature_display_to_wire: BoolProperty(
        name='set armature display to wire',
        description='',
        default=True
    )
    set_armature_display_to_show_in_front: BoolProperty(
        name='set armature display to show in front',
        description='',
        default=True
    )
    set_armature_bone_shape_to_default: BoolProperty(
        name='set armature bone shape to default',
        description='',
        default=True
    )
class Drag_import_vrma(bpy.types.Operator,drag_import_prop):
    """Load a vrma file"""
    bl_idname = 'drag_import.vrma'
    bl_label = 'Import vrma'
    bl_options = {'REGISTER', 'PRESET','UNDO'}
    def execute(self, context):
        keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        for f in self.files:
            bpy.ops.import_scene.vrma(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret
class Drag_import_vrm(bpy.types.Operator, drag_import_vrm_prop,drag_import_prop):
    """Load a vrm file"""
    bl_idname = 'drag_import.vrm'
    bl_label = 'Import vrm'
    bl_options = {'REGISTER', 'PRESET','UNDO'}
    def draw(self, context):
        #包括
        layout = self.layout.box()
        prop = context.scene.drag_import_vrm_prop
        layout.prop(prop, "extract_textures_into_folder")
        layout.prop(prop, "make_new_texture_folder")
        layout.prop(prop, "set_shading_type_to_material_on_import")
        layout.prop(prop, "set_view_transform_to_standard_on_import")
        layout.prop(prop, "set_armature_display_to_wire")
        layout.prop(prop, "set_armature_display_to_show_in_front")
        layout.prop(prop, "set_armature_bone_shape_to_default")


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
            bpy.ops.import_scene.vrm(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret


    def set_parameter(self, context):
        prop = context.scene.drag_import_vrm_prop
        self.extract_textures_into_folder = prop.extract_textures_into_folder
        self.make_new_texture_folder = prop.make_new_texture_folder
        self.set_shading_type_to_material_on_import = prop.set_shading_type_to_material_on_import
        self.set_view_transform_to_standard_on_import = prop.set_view_transform_to_standard_on_import
        self.set_armature_display_to_wire = prop.set_armature_display_to_wire
        self.set_armature_display_to_show_in_front = prop.set_armature_display_to_show_in_front
        self.set_armature_bone_shape_to_default = prop.set_armature_bone_shape_to_default


def register():
    bpy.utils.register_class(drag_import_vrm_prop)
    bpy.types.Scene.drag_import_vrm_prop = bpy.props.PointerProperty(type=drag_import_vrm_prop)
    bpy.utils.register_class(Drag_import_vrm)
    bpy.utils.register_class(Drag_import_vrma)


def unregister():
    bpy.utils.unregister_class(Drag_import_vrm)
    bpy.utils.unregister_class(Drag_import_vrma)
    del bpy.types.Scene.drag_import_vrm_prop
    bpy.utils.unregister_class(drag_import_vrm_prop)
