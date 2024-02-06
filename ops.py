import bpy,os
from bpy.props import (
    CollectionProperty,
    BoolProperty,
    StringProperty,

)
from .prop import drag_import_prop
from pathlib import Path

class Drag_import_files(bpy.types.Operator):
    """Load a FBX file"""
    bl_idname = "drag_import.files"
    bl_label = "Import FBX"
    bl_options = {'UNDO','REGISTER'}

    pop_menu:BoolProperty(
        name="Pop-up menu",
        description="Pop-up Import Settings Window",
        default=False
    )
    single_fbx=0

    def invoke(self, context, event):
        if event.ctrl:
            self.pop_menu=True

        print('pop:',self.pop_menu)
        return self.execute(context)
    def execute(self,context):
        print('pop',self.pop_menu)
        # if i== '.fbx':
        # files=[{'name':f} for f in bpy.context.scene.drag_import_prop.files_string]
        files_types=[]
        files={}
        for f in bpy.context.scene.drag_import_prop.files_string:
            extension=Path(f).suffix.lower()
            if extension not in files.keys():
                files.setdefault(f'{extension}',[])
            files[f'{extension}'].append({'name':f})
            files_types.append(extension)
        files_types=set(files_types)
        print('文件类型:',files_types)
        print('文件列表:',files)
        file_filter=['.bvh','.gltf','.pmd','.pmx','.vmd','.vpd','.svg','usd','.x3d','.ply','.wrl','.glb','.vrm','.vrma']
        for o in bpy.context.scene.objects:
            if hasattr(o.data, 'name'):

                name=o.data.name
                # print('文件名:',name)
                if o.type=='EMPTY' and (o.data is None or o.data.name[-4:] in file_filter):
                    # try:
                    bpy.data.objects.remove(o)
                    bpy.data.images.remove(bpy.data.images[name])

                    # except:
                    #     pass
        for i in files_types:
            if i=='.fbx':
                bpy.ops.drag_import.fbx('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i== '.obj':
                bpy.ops.drag_import.obj('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i in ['.glb','.gltf']:
                bpy.ops.drag_import.gltf('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i =='.dae':
                bpy.ops.drag_import.dae('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i =='.abc':
                bpy.ops.drag_import.abc('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i in ['.usd','.usdc']:
                bpy.ops.drag_import.usd('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i =='.svg':
                bpy.ops.drag_import.svg('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i =='.ply':
                bpy.ops.drag_import.ply('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i =='.stl':
                bpy.ops.drag_import.stl('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i =='.bvh':
                bpy.ops.drag_import.bvh('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
            elif i =='.vrm':
                try:
                    bpy.ops.drag_import.vrm('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
                except:
                    self.report({'INFO'},'启用最新版vrm导入插件')
                    # return {'CANCELLED'}
            elif i =='.vrma':
                try:
                    bpy.ops.drag_import.vrma('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
                except:
                    self.report({'INFO'},'启用最新版vrm导入插件')
                    # return {'CANCELLED'}
            elif i in ['.pmx','.pmd']:
                try:
                    try:
                        bpy.ops.drag_import.pmx2102('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)

                    except:
                        bpy.ops.drag_import.pmx0190('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
                except:
                    self.report({'INFO'},'启用最新版pmx或cats导入插件')
                    # return {'CANCELLED'}
            elif i =='.vmd':
                try:
                    try:
                        bpy.ops.drag_import.vmd2102('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)

                    except:
                        bpy.ops.drag_import.vmd0190('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
                except:
                    self.report({'INFO'},'启用最新版pmx或cats导入插件')
                    # return {'CANCELLED'}
            elif i =='.vpd':
                try:
                    try:
                        bpy.ops.drag_import.vpd2102('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)

                    except:
                        bpy.ops.drag_import.vpd0190('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)
                except:
                    self.report({'INFO'},'启用最新版pmx或cats导入插件')
                    # return {'CANCELLED'}
            elif i in ['.x3d','.wrl']:
                try:
                    for o in bpy.context.scene.objects:
                        name=o.data.name
                        if o.type=='EMPTY' and (o.data is None or o.data.name==os.path.basename(f)):
                            bpy.data.objects.remove(o)
                            bpy.data.images.remove(bpy.data.images[name])

                except:
                    pass
                bpy.ops.drag_import.x3d('INVOKE_DEFAULT',files=files[i],pop_menu=self.pop_menu)

        self.pop_menu=False
        self.single_fbx=0
        print('清除前',bpy.context.scene.drag_import_prop.files_string)
        bpy.context.scene.drag_import_prop.files_string.clear()
        print('清除后',bpy.context.scene.drag_import_prop.files_string)
        return {'FINISHED'}
def register():
    # bpy.utils.register_class(FilePathPropertyGroup)
    bpy.utils.register_class(Drag_import_files)



def unregister():
    # bpy.utils.unregister_class(FilePathPropertyGroup)
    bpy.utils.unregister_class(Drag_import_files)

