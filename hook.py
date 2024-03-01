import os
import sys

import bpy
from pathlib import Path
from ctypes import windll, POINTER, CDLL, c_uint, c_char_p, c_int64, c_longlong, c_wchar_p, c_uint64, cdll, cast, \
    c_void_p, c_int, c_float, \
    c_bool, c_wchar_p

from time import sleep
from .timer import Timer

'''函数定义（set_hook, set_wheel_status等）:

这些函数与加载的DLL进行交互，用于控制和查询钩子和鼠标滚轮状态，以及获取拖动文件的路径。'''


class MyDLLWrapper:
    def __init__(self, dll_path):
        # 加载 DLL
        self.dll = CDLL(dll_path)
        self.set_paragram()

    def set_paragram(self):
        # 设置函数的参数类型和返回类型
        self.dll.set_hook.argtypes = [c_int]  # set_hook函数的参数类型是整数
        self.dll.set_hook.restype = None  # set_hook函数的返回类型是无
        self.dll.get_dragfiles.restype = c_void_p  # get_dragfiles函数的返回类型是指针
        self.dll.get_num.restype = c_uint  # get_dragfiles函数的返回类型是指针
        self.dll.get_globalFileList.restype = POINTER(POINTER(c_wchar_p))  # get_globalFileList函数的返回类型是指针

    def set_hook(self, action):  # 定义设置钩子状态的函数
        if action:  # 如果action为真（激活钩子）
            self.dll.set_hook(1)  # 调用DLL的set_hook函数，传递1作为参数
        else:  # 如果action为假（禁用钩子）
            self.dll.set_hook(0)  # 调用DLL的set_hook函数，传递0作为参数

    def get_dragfiles(self):  # 定义获取拖拽文件的函数
        p = self.dll.get_dragfiles()  # 调用DLL的get_dragfiles函数
        return cast(p, c_wchar_p).value  # 将返回的指针转换成宽字符字符串并返回

    def get_num(self):  # 定义获取拖拽文件的函数
        p = self.dll.get_num()  # 调用DLL的get_dragfiles函数
        return p  # 将返回的指针转换成宽字符字符串并返回

    def get_globalFileList(self):  # 定义获取拖拽文件的函数
        p = self.dll.get_globalFileList()
        num = self.get_num()
        list = []
        for i in range(num):
            print(i, '    ', cast(p[i], c_wchar_p).value)
            print(i, '    ', p[i])
            list.append(cast(p[i], c_wchar_p).value)
        return list

    def clear_dragfiles(self):  # 定义清除拖拽文件记录的函数
        self.dll.clear_dragfiles()  # 调用DLL的clear_dragfiles函数

    def clearFileList(self):
        self.dll.clearFileList()

    def __del__(self):
        # 释放 DLL
        windll.kernel32.FreeLibrary(self.dll._handle)


def folder_files(drag_file):
    files_list = []
    for root, dirs, files in os.walk(drag_file):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            files_list.append(file_path)
    return files_list



def is_support():
    return sys.platform == "win32"


import shutil


def copy_and_create_folder(source_file, folder_name):
    dll_path = source_file.joinpath('dll', ).as_posix()
    files_list = []
    for root, dirs, files in os.walk(dll_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            files_list.append(file_path)
    grandparent_directory = source_file.parent
    new_folder_path = grandparent_directory / folder_name
    if not new_folder_path.exists():
        # 如果不存在，则创建新文件夹
        new_folder_path.mkdir()
        # print(f"新文件夹已创建在: {new_folder_path}")

    try:
        for file in files_list:
            file_path = Path(file)
            if file_path.exists() and file_path.is_file():
                destination = new_folder_path / file_path.name
                shutil.copy(file_path, destination)
                # print(f"文件已复制到: {destination}")

    except Exception as e:
        print(f"dll被占用,开启了多个blender")

cur_path = Path(__file__).parent
# 它检查系统的平台并相应地加载动态链接库（DLL），这个库假设用于处理拖放事件的低级别钩子。
copy_and_create_folder(cur_path, 'drag_import_dll')
if is_support():  # 如果支持当前操作系统
    # 获取当前文件的父目录
    dll_path = cur_path.parent.joinpath('drag_import_dll', 'hook.dll').as_posix()
    # print(cur_path)
    # print(dll_path)
    my_dll_wrapper = MyDLLWrapper(dll_path)
    my_dll_wrapper.set_hook(1)

def track():  # 定义一个名为track的函数
    while True:  # 创建一个无限循环
        sleep(1 / 30)  # 每次循环暂停约1/30秒
        drag_file = my_dll_wrapper.get_dragfiles()  # 获取当前拖拽的文件

        if not drag_file:  # 如果没有拖拽文件，则继续下一次循环
            continue

        def file_open():
            files = my_dll_wrapper.get_globalFileList()
            print('files', files)
            for f in files:
                if os.path.isdir(f):
                    folder_fs = folder_files(f)
                    bpy.context.scene.drag_import_prop.files_string.extend(folder_fs)
                    continue
                bpy.context.scene.drag_import_prop.files_string.append(f)
            print('drag_import_prop', bpy.context.scene.drag_import_prop.files)

            bpy.ops.drag_import.files('INVOKE_DEFAULT')

        Timer.put(file_open)
        Timer.put2(my_dll_wrapper.clearFileList)
        print('put')
        my_dll_wrapper.clear_dragfiles()  # 清除拖拽文件记录

# 创建并启动一个守护线程运行track函数
