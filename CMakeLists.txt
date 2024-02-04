cmake_minimum_required(VERSION 3.20)

project(hook)

# 设置C++标准
set(CMAKE_CXX_STANDARD 20)
# 添加您的项目源文件
add_library(hook SHARED hook.cpp hook.h
)
#set(CMAKE_PREFIX_PATH
#    "G:\\work\\002code\\vcpkg\\packages\\polyhook2_x64-windows\\share\\PolyHook_2\\",
#    "G:\\work\\002code\\vcpkg\\packages\\zydis_x64-windows\\share\\zydis\\",
#    "G:\\work\\002code\\vcpkg\\packages\\zycore_x64-windows\\share\\zycore\\",
#    "G:\\work\\002code\\vcpkg\\packages\\asmjit_x64-windows\\share\\asmjit\\",
#    "G:\\work\\002code\\vcpkg\\packages\\asmtk_x64-windows\\share\\asmtk\\")
#set(PolyHook_2_DIR "G:\\work\\002code\\vcpkg\\packages\\polyhook2_x64-windows\\share\\PolyHook_2",
#"G:\\work\\002code\\vcpkg\\packages\\zydis_x64-windows\\share\\zydis\\",
#    "G:\\work\\002code\\vcpkg\\packages\\zycore_x64-windows\\share\\zycore\\",
#    "G:\\work\\002code\\vcpkg\\packages\\asmjit_x64-windows\\share\\asmjit\\",
#    "G:\\work\\002code\\vcpkg\\packages\\asmtk_x64-windows\\share\\asmtk\\",
#
#)

set(Boost_USE_STATIC_LIBS ON)
target_include_directories(hook PRIVATE "G:\\work\\002code\\vcpkg\\packages\\asmjit_x64-windows\\include\\")
find_package(PolyHook_2 CONFIG REQUIRED)
target_link_libraries(hook PRIVATE PolyHook_2::PolyHook_2)
#vs needed
# 假设这是生成 DLL 的命令


# 定义目标文件夹
set(TARGET_DIR "${CMAKE_SOURCE_DIR}/dll")

# 创建目标文件夹（如果它还不存在）
file(MAKE_DIRECTORY ${TARGET_DIR})

# 添加自定义命令，在构建后移动 DLL 文件
add_custom_command(TARGET hook POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:hook>
        ${TARGET_DIR}/$<TARGET_FILE_NAME:hook>)



