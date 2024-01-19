# import bpy
# import threading
# import queue
# import time
#
# # 创建一个队列用于线程间通信
# file_path_queue = queue.Queue()
#
# # 线程函数，模拟异步获取文件路径并将其放入队列
# def thread_function():
#     # 示例：假设5秒后获取到文件路径
#     time.sleep(5)
#     file_path_queue.put("F:\\nbwork\\20240116dragimport\\untitled.obj")
#
#
# # 操作符用于在主线程中导入OBJ文件
# class ImportOBJOperator(bpy.types.Operator):
#     bl_idname = "imp.obj_operator"
#     bl_label = "Import OBJ Operator"
#
#     def execute(self, context):
#         if not file_path_queue.empty():
#             file_path = file_path_queue.get()
#             if bpy.path.exists(file_path):
#                 bpy.ops.import_scene.obj(filepath=file_path)
#                 return {'FINISHED'}
#         return {'CANCELLED'}
#
# # 定时器每秒检查一次队列
# def timer_callback():
#     if not file_path_queue.empty():
#         bpy.ops.imp.obj_operator()  # 如果队列中有文件路径，触发操作符导入OBJ文件
#     return 0.33
#
# def register():
#     bpy.utils.register_class(ImportOBJOperator)
#     bpy.app.timers.register(timer_callback)
#
# def unregister():
#     bpy.utils.unregister_class(ImportOBJOperator)
#     bpy.app.timers.unregister(timer_callback)
#
# if __name__ == "__main__":
#     register()
#
#     # 启动线程
#     thread = threading.Thread(target=thread_function)
#     thread.start()
