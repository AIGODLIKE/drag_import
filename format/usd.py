import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)
from  ..prop import drag_import_prop

class drag_import_usd_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    import_cameras: BoolProperty(
        name='Cameras',
        description='',
        default=True
    )
    import_curves: BoolProperty(
        name='Curves',
        description='',
        default=True
    )
    import_lights: BoolProperty(
        name='Lights',
        description='',
        default=True
    )
    import_materials: BoolProperty(
        name='Materials',
        description='',
        default=True
    )
    import_meshes: BoolProperty(
        name='Meshes',
        description='',
        default=True
    )
    import_volumes: BoolProperty(
        name='Volumes',
        description='',
        default=True
    )
    import_shapes: BoolProperty(
        name='Shapes',
        description='',
        default=True
    )
    import_skeletons: BoolProperty(
        name='Skeletons',
        description='',
        default=True
    )
    import_blendshapes: BoolProperty(
        name='Blend Shapes',
        description='',
        default=True
    )

    prim_path_mask: StringProperty(
        name='Path Mask',
        description='Import only the primitive at the given path and its descendants.Multiple paths may be specified in a list delimited by commas or semicolons',
    )
    scale: FloatProperty(
        name='Scale',
        description="Value by which to enlarge or shrink the objects with respect to the world's origin",
        default=1.0
    )
    read_mesh_uvs: BoolProperty(
        name='UV Coordinates',
        description='Read mesh UV coordinates',
        default=True
    )
    read_mesh_colors: BoolProperty(
        name='Color Attributes',
        description='Read mesh color attributes',
        default=True
    )
    read_mesh_attributes: BoolProperty(
        name='Mesh Attributes',
        description='Read USD Primvars as mesh attributes',
        default=True
    )
    import_subdiv: BoolProperty(
        name='Import Subdivision Scheme',
        description='Create subdivision surface modifiers based on the USD SubdivisionScheme attribute',
        default=False
    )
    import_instance_proxies: BoolProperty(
        name='Import Instance Proxies',
        description='Create unique Blender objects for USD instances',
        default=True
    )
    import_visible_only: BoolProperty(
        name='Visible Primitives Only',
        description="Do not import invisible USD primitives.Only applies to primitives with a non-animated visibility attribute.Primitives with animated visibility will always be imported",
        default=True
    )
    import_guide: BoolProperty(
        name='Guide',
        description='Import guide geometry',
        default=False
    )
    import_proxy: BoolProperty(
        name='Proxy',
        description='Import proxy geometry',
        default=True
    )
    import_render: BoolProperty(
        name='Render',
        description='Import final render geometry',
        default=True
    )
    set_frame_range: BoolProperty(
        name='set frame range',
        description="Update the scene's start and end frame to match those of the USD archive",
        default=True
    )
    relative_path: BoolProperty(
        name='relative path',
        description="Select the file relative to the blend file",
        default=True
    )
    create_collection: BoolProperty(
        name='Create Collection',
        description='Add all imported objects to a new collection',
        default=False
    )
    light_intensity_scale: FloatProperty(
        name='Light Intensity Scale',
        description='Scale for the intensity of imported lights',
        default=1.0
    )

    import_all_materials: BoolProperty(
        name='Import All Materials',
        description="Also import materials that are not used by any geometry.Note that when this option is false, materials referenced by geometry will still be imported",
        default=False
    )
    import_usd_preview: BoolProperty(
        name='Import USD Preview',
        description='Convert UsdPreviewSurface shaders to Principled BSDF shader networks',
        default=True
    )
    set_material_blend: BoolProperty(
        name='Set Material Blend',
        description="If the Import USD Preview option is enabled,the material blend method will automatically be set based on the shader's opacity and opacityThreshold inputs",
        default=True
    )
    mtl_name_collision_mode: EnumProperty(
        name='Material Name Collision',
        items=(
            ("MAKE_UNIQUE", "Make Unique", "Import each USD material as a unique Blender material"),

            ("REFERENCE_EXISTING", "Reference Existing",
             "If a material with the same name already exists, reference that instead of importing"),
        ),
        description='Behavior when the name of an imported material conflicts with an existing material',
        default="MAKE_UNIQUE"
    )
    import_textures_mode: EnumProperty(
        name='Import Textures',
        items=(
            ("IMPORT_NONE","None", "Don't import textures"),
            ("IMPORT_PACK","Packed", "Import textures as packed data"),
            ("IMPORT_COPY","Copy", "Copy files to textures directory"),
        ),
        description='Behavior when importing textures from a USDZ archive',
        default="IMPORT_PACK"
    )
    import_textures_dir: StringProperty(name='Textures Directory',
                                        description='Path to the directory where imported textures will be copied',
                                        default='//textures/')
    tex_name_collision_mode: EnumProperty(
        name='File Name Collision',
        items=(
            ("USE_EXISTING", "Use Existing", "If a file with the same name already exists, use that instead of copying"),
            ("OVERWRITE", "Overwrite", "Overwrite existing files"),
        ),
        description='Behavior when the name of an imported texture file conflicts with an existing file',
        default="USE_EXISTING"
    )



class Drag_import_usd(bpy.types.Operator, drag_import_usd_prop,drag_import_prop):
    """Load a usd file"""
    bl_idname = 'drag_import.usd'
    bl_label = 'Import usd'
    bl_options = {'REGISTER','PRESET','UNDO'}
    def draw(self, context):
        types = self.layout.box()
        prop = context.scene.drag_import_usd_prop
        types.prop(prop, "import_cameras")
        types.prop(prop, "import_curves")
        types.prop(prop, "import_lights")
        types.prop(prop, "import_materials")
        types.prop(prop, "import_meshes")
        types.prop(prop, "import_volumes")
        types.prop(prop, "import_shapes")
        if bpy.app.version>=(4,0,0):
            types.prop(prop, "import_skeletons")
            types.prop(prop, "import_blendshapes")
        types.prop(prop, "prim_path_mask")
        types.prop(prop, "scale")
        mesh=self.layout.box()
        mesh.prop(prop, "read_mesh_uvs")
        mesh.prop(prop, "read_mesh_colors")
        if bpy.app.version>=(4,0,0):
            mesh.prop(prop, "read_mesh_attributes")
        mesh.prop(prop, "import_subdiv")
        mesh.prop(prop, "import_instance_proxies")
        mesh.prop(prop, "import_visible_only")
        mesh.prop(prop, "import_guide")
        mesh.prop(prop, "import_proxy")
        mesh.prop(prop, "import_render")
        mesh.prop(prop, "set_frame_range")
        mesh.prop(prop, "relative_path")
        mesh.prop(prop, "create_collection")
        mesh.prop(prop, "light_intensity_scale")
        mat=self.layout.box()
        mat.prop(prop, "import_all_materials")
        mat.prop(prop, "import_usd_preview")
        mat.prop(prop, "set_material_blend")
        mat.prop(prop, "mtl_name_collision_mode")
        textures=self.layout.box()
        textures.prop(prop, "import_textures_mode")
        textures.prop(prop, "import_textures_dir")
        textures.prop(prop, "tex_name_collision_mode")
    def invoke(self, context, event):
        # 弹出菜单
        # return context.window_manager.invoke_props_dialog(self)
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        self.set_parameter(context)
        if bpy.app.version>=(4,0,0):
            keywords = self.as_keywords(ignore=('filepath','files','pop_menu'))
        else:
            keywords = self.as_keywords(ignore=('filepath','files','pop_menu','import_skeletons','import_blendshapes','read_mesh_attributes'))
        for f in self.files:
            bpy.ops.wm.usd_import(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret

        # return self.import_usd(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_usd_prop
        self.import_cameras = prop.import_cameras
        self.import_curves = prop.import_curves
        self.import_lights = prop.import_lights
        self.import_materials = prop.import_materials
        self.import_meshes = prop.import_meshes
        self.import_volumes = prop.import_volumes
        self.import_shapes = prop.import_shapes
        self.import_blendshapes = prop.import_blendshapes
        self.prim_path_mask = prop.prim_path_mask
        self.scale = prop.scale
        self.read_mesh_uvs = prop.read_mesh_uvs
        self.read_mesh_colors = prop.read_mesh_colors
        self.read_mesh_attributes = prop.read_mesh_attributes
        self.import_subdiv = prop.import_subdiv
        self.import_instance_proxies = prop.import_instance_proxies
        self.import_visible_only = prop.import_visible_only
        self.import_guide = prop.import_guide
        self.import_proxy = prop.import_proxy
        self.import_render = prop.import_render
        self.set_frame_range = prop.set_frame_range
        self.relative_path = prop.relative_path
        self.create_collection = prop.create_collection
        self.light_intensity_scale = prop.light_intensity_scale
        self.import_all_materials = prop.import_all_materials
        self.import_usd_preview = prop.import_usd_preview
        self.set_material_blend = prop.set_material_blend
        self.mtl_name_collision_mode = prop.mtl_name_collision_mode
        self.import_textures_mode = prop.import_textures_mode
        self.import_textures_dir = prop.import_textures_dir
        self.tex_name_collision_mode = prop.tex_name_collision_mode


def register():
    bpy.utils.register_class(drag_import_usd_prop)
    bpy.types.Scene.drag_import_usd_prop = bpy.props.PointerProperty(type=drag_import_usd_prop)
    # bpy.utils.register_class(Drag_import_usd_panel)
    bpy.utils.register_class(Drag_import_usd)


def unregister():
    # bpy.utils.unregister_class(Drag_import_usd_panel)
    bpy.utils.unregister_class(Drag_import_usd)
    del bpy.types.Scene.drag_import_usd_prop
    bpy.utils.unregister_class(drag_import_usd_prop)
