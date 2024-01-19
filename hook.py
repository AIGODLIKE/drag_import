import os
import sys
from queue import Queue
import threading
import bpy
from functools import partial
from pathlib import Path
from ctypes import RTLD_GLOBAL, POINTER, CDLL, c_int64, c_longlong, c_uint64, cdll, cast, c_void_p, c_int, c_float, \
    c_bool, c_wchar_p
from array import array as Array
from threading import Thread
from time import sleep
from .timer import Timer

# from .utils import _T

# 导入:

# 导入了各种Python和特定于Blender的模块，用于处理文件、线程、ctypes用于与C库接口等。
'''函数定义（set_hook, set_wheel_status等）:

这些函数与加载的DLL进行交互，用于控制和查询钩子和鼠标滚轮状态，以及获取拖动文件的路径。'''


def set_hook(action):
    ...


def set_wheel_status(s):
    ...


def get_wheel_status():
    return 0


def clear_dragfiles():
    ...


def get_dragfiles():
    return ""


def is_support():
    return sys.platform == "win32"


# 它检查系统的平台并相应地加载动态链接库（DLL），这个库假设用于处理拖放事件的低级别钩子。

if is_support():  # 如果支持当前操作系统
    cur_path = Path(__file__).parent  # 获取当前文件的父目录
    if sys.platform == "darwin":  # 如果是macOS系统
        dll_path = cur_path.joinpath("hook.dylib").as_posix()  # 构建.dylib库文件的路径
        dll = cdll.LoadLibrary(dll_path)  # 加载.dylib库文件
    elif sys.platform == "win32":  # 如果是Windows系统
        from ctypes import WinDLL  # 导入WinDLL类

        dll_path = cur_path.joinpath("hook.dll").as_posix()  # 构建.dll库文件的路径
        if sys.version_info >= (3, 9, 0):  # 如果Python版本大于等于3.9
            os.add_dll_directory(cur_path.as_posix())  # 将当前路径添加到DLL搜索路径
            try:
                dll = WinDLL(dll_path, winmode=RTLD_GLOBAL)  # 尝试加载全局模式的.dll库文件
            except BaseException:  # 如果尝试失败
                dll = CDLL(dll_path, winmode=RTLD_GLOBAL)  # 加载全局模式的.dll库文件
        else:  # 如果Python版本小于3.9
            dll = cdll.LoadLibrary(dll_path)  # 直接加载.dll库文件

    # 设置函数的参数类型和返回类型
    dll.set_hook.argtypes = [c_int]  # set_hook函数的参数类型是整数
    dll.set_hook.restype = None  # set_hook函数的返回类型是无
    dll.set_wheel_status.argtypes = [c_int]  # set_wheel_status函数的参数类型是整数
    dll.get_wheel_status.restype = c_int  # get_wheel_status函数的返回类型是整数
    dll.get_dragfiles.restype = c_void_p  # get_dragfiles函数的返回类型是指针


    def set_hook(action):  # 定义设置钩子状态的函数
        if action:  # 如果action为真（激活钩子）
            dll.set_hook(1)  # 调用DLL的set_hook函数，传递1作为参数
        else:  # 如果action为假（禁用钩子）
            dll.set_hook(0)  # 调用DLL的set_hook函数，传递0作为参数


    def set_wheel_status(s):  # 定义设置鼠标滚轮状态的函数
        dll.set_wheel_status(s)  # 调用DLL的set_wheel_status函数，传递s作为参数


    def get_wheel_status():  # 定义获取鼠标滚轮状态的函数
        return dll.get_wheel_status()  # 调用DLL的get_wheel_status函数并返回其结果


    def get_dragfiles():  # 定义获取拖拽文件的函数
        p = dll.get_dragfiles()  # 调用DLL的get_dragfiles函数
        return cast(p, c_wchar_p).value  # 将返回的指针转换成宽字符字符串并返回


    def clear_dragfiles():  # 定义清除拖拽文件记录的函数
        dll.clear_dragfiles()  # 调用DLL的clear_dragfiles函数


    set_hook(1)  # 激活钩子
    # dll.set_debug(True)  #（未启用）设置调试模式

CACHED_DPFILES: list[Path] = []  # 声明一个名为CACHED_DPFILES的变量，它是一个Path对象的列表，并初始化为一个空列表

# def pop_menu(self, context):  # 定义一个名为pop_menu的函数
#     layout: bpy.types.UILayout = self.layout  # 获取当前UI布局
#     for file in CACHED_DPFILES:  # 遍历之前缓存的所有拖拽文件路径
#         name = file.name  # 获取文件名
#         itype = ""  # 初始化文件类型变量
#         if file.suffix.lower() == ".csv":  # 如果文件后缀是.csv
#             itype = _T("BatchTaskTable")  # 设置文件类型为BatchTaskTable
#         else:  # 如果文件后缀不是.csv
#             itype = _T("NodeTree")  # 设置文件类型为NodeTree
#         info = _T("Import [{}] as {}?").format(name, itype)  # 格式化显示的信息，询问用户是否导入
#         op = layout.operator("sdn.popup_load", text=info, icon="IMPORT")  # 创建一个操作按钮
#         op.filepath = file.as_posix()  # 设置操作的文件路径

'''跟踪线程:

一个线程（t）在后台持续运行track函数。这个函数似乎在间隔时间检查拖拽的文件并更新一个缓存文件列表（CACHED_DPFILES）。当检测到新文件时，它准备在Blender节点编辑器中显示一个弹出菜单以导入文件。'''


def track():  # 定义一个名为track的函数
    while True:  # 创建一个无限循环
        sleep(1 / 30)  # 每次循环暂停约1/30秒
        drag_file = get_dragfiles()  # 获取当前拖拽的文件
        if not drag_file:  # 如果没有拖拽文件，则继续下一次循环
            continue
        drag_file = Path(drag_file)  # 将拖拽的文件路径转换为Path对象
        print(os.path.isdir(drag_file))
        if not(drag_file.suffix.lower() in {".fbx", ".obj"} or os.path.isdir(drag_file)):  # 如果文件类型不在指定列表中，则继续下一次循环
            continue
        CACHED_DPFILES.clear()  # 清空之前缓存的文件列表
        CACHED_DPFILES.append(Path(drag_file))  # 将当前拖拽的文件添加到缓存列表
        print('CACHED_DPFILES:', CACHED_DPFILES)
        print('CACHED_DPFILES:', drag_file)

        def file_open():
            print('f')
            current_thread = threading.current_thread()
            # 打印当前线程的名称
            print(f"Function is running in thread: {current_thread.name}")
            # bpy.ops.import_scene.fbx(filepath=str(drag_file))
            # bpy.ops.wm.obj_import(filepath=str(drag_file))
            if drag_file.suffix.lower()== '.fbx':
                bpy.ops.import_scene.fbx(filepath=str(drag_file), directory="", filter_glob="*.fbx", files=[], ui_tab='MAIN',
                                         use_manual_orientation=False, global_scale=1, bake_space_transform=False,
                                         use_custom_normals=True, colors_type='SRGB', use_image_search=True,
                                         use_alpha_decals=False, decal_offset=0, use_anim=True, anim_offset=1,
                                         use_subsurf=False, use_custom_props=True, use_custom_props_enum_as_string=True,
                                         ignore_leaf_bones=False, force_connect_children=False,
                                         automatic_bone_orientation=False, primary_bone_axis='Y', secondary_bone_axis='X',
                                         use_prepost_rot=True, axis_forward='-Z', axis_up='Y')
            elif drag_file.suffix.lower()== '.obj':
                bpy.ops.wm.obj_import(filepath=str(drag_file))
            elif os.path.isdir(drag_file):
                print(f"{drag_file} 是一个文件夹")
                for root, dirs, files in os.walk(drag_file):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        file_extension = os.path.splitext(file_name)[1].lower()

                        # 添加您想要导入的文件格式，例如'.obj', '.fbx', '.blend'等
                        if file_extension == '.fbx':
                            bpy.ops.import_scene.fbx(filepath=str(file_path), directory="", filter_glob="*.fbx",
                                                     files=[], ui_tab='MAIN',
                                                     use_manual_orientation=False, global_scale=1,
                                                     bake_space_transform=False,
                                                     use_custom_normals=True, colors_type='SRGB', use_image_search=True,
                                                     use_alpha_decals=False, decal_offset=0, use_anim=True,
                                                     anim_offset=1,
                                                     use_subsurf=False, use_custom_props=True,
                                                     use_custom_props_enum_as_string=True,
                                                     ignore_leaf_bones=False, force_connect_children=False,
                                                     automatic_bone_orientation=False, primary_bone_axis='Y',
                                                     secondary_bone_axis='X',
                                                     use_prepost_rot=True, axis_forward='-Z', axis_up='Y')
                        elif file_extension == '.obj':
                            bpy.ops.wm.obj_import(filepath=str(file_path))
                def draw(cls,context):
                    layout=cls.layout
                    layout.label(text='aa')

                bpy.context.window_manager.popup_menu(draw,title="")
        Timer.put(file_open)
        print('put')
        clear_dragfiles()  # 清除拖拽文件记录

# 创建并启动一个守护线程运行track函数
