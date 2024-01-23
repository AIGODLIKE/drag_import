import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)


class drag_import_svg_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    resolution: IntProperty(
        name="Resolution",
        description="Resolution of the generated strokes",
        min=1, max=30,
        soft_min=1, soft_max=20,
        default=10,
    )
    scale: FloatProperty(
        name="Scale",
        description="Scale of the final strokes",
        min=0.001, max=100.0,
        soft_min=0.001, soft_max=100.0,
        default=10.0,
    )



# class Drag_import_svg_panel(bpy.types.Panel):
#     """创建一个面板在 N面板中"""
#     bl_label = "svg_panel"
#     bl_idname = "svgECT_PT_import_svg"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Drag_import'  # N面板的标签
#
#     def draw(self, context):
#         layout = self.layout
#         drag_import_svg_prop = context.scene.drag_import_svg_prop
#
#         layout.prop(drag_import_svg_prop, "global_scale")
#         layout.prop(drag_import_svg_prop, "clamp_size")
#         layout.prop(drag_import_svg_prop, "forward_axis")
#         layout.prop(drag_import_svg_prop, "up_axis")
#         layout.prop(drag_import_svg_prop, "use_split_svgects")
#         layout.prop(drag_import_svg_prop, "use_split_groups")
#         layout.prop(drag_import_svg_prop, "import_vertex_groups")
#         layout.prop(drag_import_svg_prop, "validate_meshes")


class Drag_import_svg(bpy.types.Operator, drag_import_svg_prop):
    """Load a svg file"""
    bl_idname = 'drag_import.svg'
    bl_label = 'Import svg'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','resolution','scale'))

        if bpy.ops.import_curve.svg(filepath=self.filepath, **keywords) == {'FINISHED'}:
            ret = {'FINISHED'}
        return ret

        # return self.import_svg(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_svg_prop
        self.resolution = prop.resolution
        self.scale = prop.scale



def register():
    bpy.utils.register_class(drag_import_svg_prop)
    bpy.types.Scene.drag_import_svg_prop = bpy.props.PointerProperty(type=drag_import_svg_prop)
    # bpy.utils.register_class(Drag_import_svg_panel)
    bpy.utils.register_class(Drag_import_svg)


def unregister():
    # bpy.utils.unregister_class(Drag_import_svg_panel)
    bpy.utils.unregister_class(Drag_import_svg)
    del bpy.types.Scene.drag_import_svg_prop
    bpy.utils.unregister_class(drag_import_svg_prop)
