import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)
from  ..prop import drag_import_prop

class drag_import_stl_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()

    global_scale: FloatProperty(
        name='Scale',
        description='',
        default=1.0
    )

    use_scene_unit: BoolProperty(
        name='Scene Unit',
        description="Apply current scene's unit (as defined by unit scale) to imported data",
        default=False
    )
    axis_forward: EnumProperty(
        name='Forward Axis',
        items=(
            ("X", "X", "Positive X axis"),
            ("Y", "Y", "Positive Y axis"),
            ("Z", "Z", "Positive Z axis"),
            ("-X", "-X", "Negative X axis"),
            ("-Y", "-Y", "Negative Y axis"),
            ("-Z", "-Z", "Negative Z axis"),
        ),
        description='',
        default="Y"
    )
    axis_up: EnumProperty(
        name='Up Axis',
        items=(
            ("X", "X", "Positive X axis"),
            ("Y", "Y", "Positive Y axis"),
            ("Z", "Z", "Positive Z axis"),
            ("-X", "-X", "Negative X axis"),
            ("-Y", "-Y", "Negative Y axis"),
            ("-Z", "-Z", "Negative Z axis"),
        ),
        description='',
        default="Z"
    )
    use_facet_normal: BoolProperty(
        name='Facet Normals',
        description="Use (import) facet normals (note that this will still give flat shading)",
        default=False,
    )

class Drag_import_stl(bpy.types.Operator, drag_import_stl_prop,drag_import_prop):
    """Load a stl file"""
    bl_idname = 'drag_import.stl'
    bl_label = 'Import stl'
    bl_options = {'REGISTER','PRESET','UNDO'}
    def draw(self, context):

        prop = context.scene.drag_import_stl_prop
        trans = self.layout.box()
        trans.label(text='Transform')
        trans.prop(prop, "global_scale")
        trans.prop(prop, "use_scene_unit")
        trans.prop(prop, "axis_forward")
        trans.prop(prop, "axis_up")
        geom = self.layout.box()
        geom.label(text='Geometry')
        geom.prop(prop, "use_facet_normal")

    def invoke(self, context, event):
        if self.pop_menu:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def execute(self, context):
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath','pop_menu','files',))
        for f in self.files:
            bpy.ops.import_mesh.stl(filepath=f.name, **keywords)
        ret = {'FINISHED'}
        return ret


    def set_parameter(self, context):
        prop = context.scene.drag_import_stl_prop
        self.global_scale = prop.global_scale
        self.use_scene_unit = prop.use_scene_unit
        self.axis_forward = prop.axis_forward
        self.axis_up = prop.axis_up
        self.use_facet_normal = prop.use_facet_normal


def register():
    bpy.utils.register_class(drag_import_stl_prop)
    bpy.types.Scene.drag_import_stl_prop = bpy.props.PointerProperty(type=drag_import_stl_prop)
    # bpy.utils.register_class(Drag_import_stl_panel)
    bpy.utils.register_class(Drag_import_stl)


def unregister():
    # bpy.utils.unregister_class(Drag_import_stl_panel)
    bpy.utils.unregister_class(Drag_import_stl)
    del bpy.types.Scene.drag_import_stl_prop
    bpy.utils.unregister_class(drag_import_stl_prop)
