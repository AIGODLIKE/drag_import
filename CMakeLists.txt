cmake_minimum_required(VERSION 3.20)

project(hook)

# 设置C++标准
set(CMAKE_CXX_STANDARD 20)
# 添加您的项目源文件
add_library(hook SHARED hook.cpp hook.h)
find_package(PolyHook_2 CONFIG REQUIRED)
target_link_libraries(hook PUBLIC PolyHook_2::PolyHook_2)
#vs needed
#set(CMAKE_PREFIX_PATH
#    "G:\\work\\002code\\vcpkg\\packages\\polyhook2_x64-windows\\share\\PolyHook_2\\"
#    "G:\\work\\002code\\vcpkg\\packages\\zydis_x64-windows\\share\\zydis\\"
#    "G:\\work\\002code\\vcpkg\\packages\\zycore_x64-windows\\share\\zycore\\"
#    "G:\\work\\002code\\vcpkg\\packages\\asmjit_x64-windows\\share\\asmjit\\"
#    "G:\\work\\002code\\vcpkg\\packages\\asmtk_x64-windows\\share\\asmtk\\")
#target_include_directories(hook PUBLIC "G:\\work\\002code\\vcpkg\\packages\\asmjit_x64-windows\\include\\")



