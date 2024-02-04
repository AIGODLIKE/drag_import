import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    IntProperty,
    StringProperty,
    CollectionProperty
)
from  ..prop import drag_import_prop

class Drag_import_gltf_prop(bpy.types.PropertyGroup):
    filter_glob: StringProperty(default="*.glb;*.gltf", options={'HIDDEN'})

    filepath: StringProperty()

    loglevel: IntProperty(
        name='Log Level',
        description="Log Level")

    import_pack_images: BoolProperty(
        name='Pack Images',
        description='Pack all images into .blend file',
        default=True
    )
    export_import_convert_lighting_mode: EnumProperty(
        name='Lighting Mode',
        items=(
            ('SPEC', 'Standard', 'Physically-based glTF lighting units (cd, lx, nt)'),
            ('COMPAT', 'Unitless', 'Non-physical, unitless lighting. Useful when exposure controls are not available'),
            ('RAW', 'Raw (Deprecated)', 'Blender lighting strengths with no conversion'),
        ),
        description='Optional backwards compatibility for non-standard render engines. Applies to lights',# TODO: and emissive materials',
        default='SPEC'
    )
    merge_vertices: BoolProperty(
        name='Merge Vertices',
        description=(
            'The glTF format requires discontinuous normals, UVs, and other vertex attributes to be stored as separate vertices,as required for rendering on typical graphics hardware.This option attempts to combine co-located vertices where possible.Currently cannot combine verts with different normals'
        ),
        default=False,
    )

    import_shading: EnumProperty(
        name="Shading",
        items=(("NORMALS", "Use Normal Data", ""),
               ("FLAT", "Flat Shading", ""),
               ("SMOOTH", "Smooth Shading", "")),
        description="How normals are computed during import",
        default="NORMALS")

    bone_heuristic: EnumProperty(
        name="Bone Dir",
        items=(
            ("BLENDER", "Blender (best for import/export round trip)",
             "Good for re-importing glTFs exported from Blender, and re-exporting glTFs to glTFs after Blender editing.Bone tips are placed on their local +Y axis (in glTF space)"),
            ("TEMPERANCE", "Temperance (average)",
             "Decent all-around strategy. A bone with one child has its tip placed on the local axis closest to its child"),
            ("FORTUNE", "Fortune (may look better, less accurate)",
             "Might look better than Temperance, but also might have errors. A bone with one child has its tip placed at its child's root.Non-uniform scalings may get messed up though, so beware"),
        ),
        description="Heuristic for placing bones. Tries to make bones pretty",
        default="BLENDER",
    )

    guess_original_bind_pose: BoolProperty(
        name='Guess Original Bind Pose',
        description=(
            'Try to guess the original bind pose for skinned meshes from the inverse bind matrices.When off, use default/rest pose as bind pose'
        ),
        default=True,
    )

    import_webp_texture: BoolProperty(
        name='Import WebP textures',
        description=(
            "If a texture exists in WebP format,loads the WebP texture instead of the fallback PNG/JPEG one"
        ),
        default=False,
    )


class Drag_import_gltf(bpy.types.Operator,Drag_import_gltf_prop,drag_import_prop):
    """Load a glTF 2.0 file"""
    bl_idname = 'drag_import.gltf'
    bl_label = 'Import glTF 2.0'
    bl_options = {'REGISTER','PRESET','UNDO'}

    def draw(self, context):

        prop = context.scene.drag_import_gltf_prop
        option=self.layout.box()
        option.prop(prop, "import_pack_images")
        option.prop(prop, "merge_vertices")
        option.prop(prop, "import_shading")
        option.prop(prop, "guess_original_bind_pose")
        option.prop(prop, "bone_heuristic")
        option.prop(prop, "export_import_convert_lighting_mode")
        if bpy.app.version>=(4,0,0):
            option.prop(prop, "import_webp_texture")

    def invoke(self, context, event):
        # 弹出菜单
        # return context.window_manager.invoke_props_dialog(self)
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def set_parameter(self, context):
        prop = context.scene.drag_import_gltf_prop
        self.import_pack_images = prop.import_pack_images
        self.merge_vertices = prop.merge_vertices
        self.import_shading = prop.import_shading
        self.guess_original_bind_pose = prop.guess_original_bind_pose
        self.bone_heuristic = prop.bone_heuristic
        self.export_import_convert_lighting_mode = prop.export_import_convert_lighting_mode
        self.import_webp_texture = prop.import_webp_texture
    def execute(self, context):
        # ret = {'CANCELLED'}
        self.set_parameter(context)
        if bpy.app.version>=(4,0,0):
            keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        else:
            keywords = self.as_keywords(ignore=('filepath','files','pop_menu','import_webp_texture'))
        for f in self.files:
            bpy.ops.import_scene.gltf(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret





def register():
    bpy.utils.register_class(Drag_import_gltf_prop)
    bpy.types.Scene.drag_import_gltf_prop = bpy.props.PointerProperty(type=Drag_import_gltf_prop)
    # bpy.utils.register_class(Drag_import_gltf_panel)
    bpy.utils.register_class(Drag_import_gltf)


def unregister():
    # bpy.utils.unregister_class(Drag_import_gltf_panel)
    bpy.utils.unregister_class(Drag_import_gltf)
    del bpy.types.Scene.drag_import_gltf_prop
    bpy.utils.unregister_class(Drag_import_gltf_prop)
