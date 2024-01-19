cmake_minimum_required(VERSION 3.0)

project(YourProjectName)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)

# 设置输出目录
set(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR}/bin)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

# 导入spdlog库
find_package(spdlog REQUIRED)

# 导入PolyHook2库（这里假设PolyHook2是一个CMake可用的库）
# 使用ExternalProject模块可以自动下载和构建库
include(ExternalProject)
ExternalProject_Add(
        PolyHook2
        PREFIX ${CMAKE_BINARY_DIR}/deps
        GIT_REPOSITORY https://github.com/stevemk14ebr/PolyHook_2_0
        CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
)

# 添加您的项目源文件
add_executable(YourProjectName main.cpp)

# 链接spdlog库
target_link_libraries(YourProjectName PRIVATE spdlog::spdlog)

# 链接PolyHook2库
# 使用ExternalProject_Add生成的库的路径
target_link_libraries(YourProjectName PRIVATE ${CMAKE_BINARY_DIR}/deps/src/PolyHook2-build/your_lib_name)

# 添加PolyHook2库的头文件路径
target_include_directories(YourProjectName PRIVATE ${CMAKE_BINARY_DIR}/deps/src/PolyHook2/src)

# 将PolyHook2库的构建目标添加到依赖项中
add_dependencies(YourProjectName PolyHook2)
