import bpy
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty,
    StringProperty,

)


class drag_import_bvh_prop(bpy.types.PropertyGroup):
    filepath: StringProperty()
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
    target: EnumProperty(
        items=(
            ('ARMATURE', "Armature", ""),
            ('OBJECT', "Object", ""),
        ),
        name="Target",
        description="Import target type",
        default='ARMATURE',
    )
    global_scale: FloatProperty(
        name="Scale",
        description="Scale the BVH by this value",
        min=0.0001, max=1000000.0,
        soft_min=0.001, soft_max=100.0,
        default=1.0,
    )
    frame_start: IntProperty(
        name="Start Frame",
        description="Starting frame for the animation",
        default=1,
    )
    use_fps_scale: BoolProperty(
        name="Scale FPS",
        description=(
            "Scale the framerate from the BVH to the current scenes, "
            "otherwise each BVH frame maps directly to a Blender frame"
        ),
        default=False,
    )
    update_scene_fps: BoolProperty(
        name="Update Scene FPS",
        description=(
            "Set the scene framerate to that of the BVH file (note that this "
            "nullifies the 'Scale FPS' option, as the scale will be 1:1)"
        ),
        default=False,
    )
    update_scene_duration: BoolProperty(
        name="Update Scene Duration",
        description="Extend the scene's duration to the BVH duration (never shortens the scene)",
        default=False,
    )
    use_cyclic: BoolProperty(
        name="Loop",
        description="Loop the animation playback",
        default=False,
    )
    rotate_mode: EnumProperty(
        name="Rotation",
        description="Rotation conversion",
        items=(
            ('QUATERNION', "Quaternion",
             "Convert rotations to quaternions"),
            ('NATIVE', "Euler (Native)",
             "Use the rotation order defined in the BVH file"),
            ('XYZ', "Euler (XYZ)", "Convert rotations to euler XYZ"),
            ('XZY', "Euler (XZY)", "Convert rotations to euler XZY"),
            ('YXZ', "Euler (YXZ)", "Convert rotations to euler YXZ"),
            ('YZX', "Euler (YZX)", "Convert rotations to euler YZX"),
            ('ZXY', "Euler (ZXY)", "Convert rotations to euler ZXY"),
            ('ZYX', "Euler (ZYX)", "Convert rotations to euler ZYX"),
        ),
        default='NATIVE',
    )



# class Drag_import_bvh_panel(bpy.types.Panel):
#     """创建一个面板在 N面板中"""
#     bl_label = "bvh_panel"
#     bl_idname = "bvhECT_PT_import_bvh"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Drag_import'  # N面板的标签
#
#     def draw(self, context):
#         layout = self.layout
#         drag_import_bvh_prop = context.scene.drag_import_bvh_prop
#
#         layout.prop(drag_import_bvh_prop, "global_scale")
#         layout.prop(drag_import_bvh_prop, "clamp_size")
#         layout.prop(drag_import_bvh_prop, "forward_axis")
#         layout.prop(drag_import_bvh_prop, "up_axis")
#         layout.prop(drag_import_bvh_prop, "use_split_bvhects")
#         layout.prop(drag_import_bvh_prop, "use_split_groups")
#         layout.prop(drag_import_bvh_prop, "import_vertex_groups")
#         layout.prop(drag_import_bvh_prop, "validate_meshes")


class Drag_import_bvh(bpy.types.Operator, drag_import_bvh_prop):
    """Load a bvh file"""
    bl_idname = 'drag_import.bvh'
    bl_label = 'Import bvh'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ret = {'CANCELLED'}
        self.set_parameter(context)
        keywords = self.as_keywords(ignore=('filepath',))

        if bpy.ops.import_anim.bvh(filepath=self.filepath, **keywords) == {'FINISHED'}:
            ret = {'FINISHED'}
        return ret

        # return self.import_bvh(context)

    def set_parameter(self, context):
        prop = context.scene.drag_import_bvh_prop
        self.axis_forward = prop.axis_forward
        self.axis_up = prop.axis_up
        self.target = prop.target
        self.global_scale = prop.global_scale
        self.rotate_mode = prop.rotate_mode
        self.frame_start = prop.frame_start
        self.use_fps_scale = prop.use_fps_scale
        self.use_cyclic = prop.use_cyclic
        self.update_scene_fps = prop.update_scene_fps
        self.update_scene_duration = prop.update_scene_duration


def register():
    bpy.utils.register_class(drag_import_bvh_prop)
    bpy.types.Scene.drag_import_bvh_prop = bpy.props.PointerProperty(type=drag_import_bvh_prop)
    # bpy.utils.register_class(Drag_import_bvh_panel)
    bpy.utils.register_class(Drag_import_bvh)


def unregister():
    # bpy.utils.unregister_class(Drag_import_bvh_panel)
    bpy.utils.unregister_class(Drag_import_bvh)
    del bpy.types.Scene.drag_import_bvh_prop
    bpy.utils.unregister_class(drag_import_bvh_prop)
