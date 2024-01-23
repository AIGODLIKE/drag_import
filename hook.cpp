/*
这段代码是用C++语言编写的，用于实现一个Windows下的钩子（hook）库。它主要功能包括捕获鼠标滚轮事件、键盘按键事件、拖拽文件事件等，并提供了一系列导出函数以供外部调用*/
#include "hook.h"
// #include "dragdrop.h"
//#include "logger.h"
//#include <algorithm>
//#include "ole2.h"
#include "polyhook2/Detour/NatDetour.hpp"
#include "polyhook2/IHook.hpp"
//#include "spdlog/logger.h"

// 定义GH宏，用于创建钩子
#define GH(f) PLH::NatDetour((uint64_t)&f, (uint64_t)h##f, &h##f##Tramp)
/*GH 是宏的名称，当你在代码中写 GH(someFunction) 时，它会被展开成 PLH::NatDetour 的调用。
f 是宏的参数，代表你想要设置钩子的函数。
PLH::NatDetour 是PolyHook 2库中的一个类，它提供了函数的钩子（detouring）功能。Detouring是一种修改程序执行流程的技术，它通常用于改变函数调用或者插入额外的代码执行。
(uint64_t)&f 是将函数f的地址转换成uint64_t类型，即它的地址。
h##f 和 &h##f##Tramp 是使用宏的连接操作符##构造的标识符。
如果f是PeekMessageW，那么h##f就会变成hPeekMessageW，&h##f##Tramp就会变成&hPeekMessageWTramp。
这些通常是与f相关联的另外两个函数，一个是你提供的hook处理函数，另一个是用于存储原始函数地址的变量。
这行代码的目的是为了使设置函数钩子更加简洁和直观。
在使用时，你只需要提供想要钩子的函数名称，宏就会扩展成一个完整的PLH::NatDetour调用，
从而设置钩子。这种技术在底层系统编程、游戏开发、安全研究等领域经常被使用，用于改变或扩展现有的功能。
在实际开发中，使用这种高级技术需要对系统编程、内存管理和相关工具有深入的理解。*/

using namespace std;

// 定义静态变量，用于存储全局状态
//static int wheel_status = 0;  // 鼠标滚轮状态
static WCHAR dragfiles[512];  // 拖拽文件路径
static UINT fileCount;
static bool is_msg_run = false;  // 消息循环运行标志
static WCHAR** globalFileList = nullptr;
void allocateFileList(UINT numberOfFiles) {
    // 先清理之前的列表
    clearFileList();

    // 为指针数组分配内存
    globalFileList = new WCHAR*[numberOfFiles];

    // 为每个文件路径分配内存
    for (UINT i = 0; i < numberOfFiles; ++i) {
        globalFileList[i] = new WCHAR[512];
    }
}
XLIB void clearFileList() {
    if (globalFileList != nullptr) {
        // 释放每个文件路径的内存
        for (UINT i = 0; i < fileCount && globalFileList[i] != nullptr; ++i) {
            delete[] globalFileList[i];
            globalFileList[i] = nullptr;
        }

        // 释放指针数组的内存
        delete[] globalFileList;
        globalFileList = nullptr;
    }
}





// 定义变量用于存储原始PeekMessageW函数的地址
//uint64_t hPeekMessageWTramp = NULL;
//
//// 定义hook后的PeekMessageW函数
//BOOL hPeekMessageW(LPMSG lpMsg, HWND hWnd, UINT wMsgFilterMin,
//                   UINT wMsgFilterMax, UINT wRemoveMsg) {
//  // 调用原始的PeekMessageW函数，并将结果存储在res中
//  BOOL res = PLH::FnCast(hPeekMessageWTramp, &PeekMessageW)(
//      lpMsg, hWnd, wMsgFilterMin, wMsgFilterMax, wRemoveMsg);
//  // 调用msgProc函数处理消息
////  msgProc(lpMsg, hWnd, wMsgFilterMin, wMsgFilterMax, "PMSGW");
//  return res;  // 返回原始函数的结果
//}
/*在这段代码中：

hPeekMessageW 是一个hook版本的 PeekMessageW 函数。PeekMessageW 是Windows API中的一个函数，
用于从应用程序的消息队列中获取消息。hook这个函数允许程序在消息被处理之前捕获并处理它们。
hDragQueryFileW 是一个hook版本的 DragQueryFileW 函数。DragQueryFileW 是Windows API中的一个函数，
用于从拖拽操作中检索文件信息。hook这个函数允许程序在文件被拖拽到应用程序中时捕获并处理文件路径。
两个函数都使用了PolyHook 2（PLH::FnCast），这是一个C++库，用于hook函数。
通过将原始函数的地址和新函数的地址传递给这个库，可以实现在调用原始函数时自动跳转到新函数的功能。*/
// 定义变量用于存储原始DragQueryFileW函数的地址
/*
这段代码定义了两个函数，hPeekMessageW 和 hDragQueryFileW，
这两个函数都是用于hook系统函数，以便在系统调用这些函数时执行一些额外的操作*/
uint64_t hDragQueryFileWTramp = NULL;

// 定义hook后的DragQueryFileW函数
UINT hDragQueryFileW(HDROP hDrop, UINT iFile, LPWSTR lpszFile, UINT cch) {

  // 调用原始的DragQueryFileW函数，并将结果存储在res中
  UINT res = PLH::FnCast(hDragQueryFileWTramp, &DragQueryFileW)(hDrop, iFile,
                                                                lpszFile, cch);
  /*-------------------------------------------------*/

/*单个字符串*/
  // 如果提供了文件路径lpszFile
  if (lpszFile) {
    // 计算文件路径的长度，并限制最大长度为512
    int len = min(wcslen(lpszFile) + 1, 512);
      // 将文件路径复制到dragfiles变量中
    wcscpy_s(dragfiles, len, lpszFile);
    //文件数量
//    fileCount = DragQueryFileW(hDrop, 0xFFFFFFFF, nullptr, 0);
    fileCount = PLH::FnCast(hDragQueryFileWTramp, &DragQueryFileW)(hDrop, 0xFFFFFFFF,
                                                                   nullptr, 0);
    fileCount = min(fileCount, 1024);  // 确保不超过最大文件数量
    allocateFileList(fileCount);
    // 循环处理每个文件
    for (UINT i = 0; i < fileCount; ++i) {
        // 将每个文件的路径存储到全局列表中
        UINT temp = PLH::FnCast(hDragQueryFileWTramp, &DragQueryFileW)(hDrop, i,
                                                                       globalFileList[i], cch);
//        DragQueryFileW(hDrop, i, globalFileList[i], cch);
//        int len = min(wcslen(globalFileList[i]) + 1, 512);
//        wcscpy_s(dragfiles, len, globalFileList[i]);
    }
  }




   /*-------------------------------------*/
    return res;  // 返回原始函数的结果
}
/*在这段代码中：

clear_dragfiles 用于清空当前记录的拖拽文件路径。
get_dragfiles 用于获取当前记录的拖拽文件路径。
set_hook 用于根据传入的布尔值启用或禁用特定的系统钩子。
这通常用于拦截和修改系统级事件，如消息循环中的消息或拖拽文件事件。*/
/*
这段代码定义了一系列函数，主要用于操作和获取拖拽文件路径、鼠标滚轮状态以及设置钩子*/
// 定义清除拖拽文件路径的函数
XLIB void clear_dragfiles() {
  dragfiles[0] = '\0';  // 将dragfiles字符串的第一个字符设置为null字符，从而清空字符串
  // dragfiles.clear();  // 这行代码被注释掉了，但它的目的是清空dragfiles列表
}

// 定义获取拖拽文件路径的函数
XLIB WCHAR *get_dragfiles() { 
  return dragfiles;  // 返回dragfiles字符串，即拖拽文件的路径
}
XLIB UINT get_num() {
    return fileCount;  // 返回dragfiles字符串，即拖拽文件的路径
}
XLIB WCHAR **get_globalFileList() {
    return globalFileList;  // 返回dragfiles字符串，即拖拽文件的路径
}

// 定义设置钩子的函数
XLIB void set_hook(bool set) {
  // 使用GH宏创建PeekMessageW和DragQueryFileW函数的hook
//  static auto pmsgwdetour = GH(PeekMessageW);
  static auto dqfwhook = GH(DragQueryFileW);

  // 根据set参数的值，安装或卸载钩子
  if (set) {
//    pmsgwdetour.hook();  // 安装PeekMessageW钩子
    dqfwhook.hook();     // 安装DragQueryFileW钩子
  } else {
//    pmsgwdetour.unHook();  // 卸载PeekMessageW钩子
    dqfwhook.unHook();     // 卸载DragQueryFileW钩子
  }
}

/*run_exit 函数用于停止消息处理循环。它通过将is_msg_run标志设置为false来实现。
run_forever 函数用于开始一个无限的消息处理循环。
它首先检查is_msg_run标志以确保循环不会被重复启动，然后设置标志为true并调用msg_run进入循环。
msg_run 是实际的消息处理循环，它持续调用hook_exec函数，直到is_msg_run变为false。
hook_exec 函数不断从消息队列中获取消息并进行处理。它使用了PeekMessage函数来检查队列，
如果有消息就使用TranslateMessage和DispatchMessage进行处理。特别地，如果收到了退出消息WM_QUIT，则会跳出循环。*/
// 这些函数通常用于创建和管理一个自定义的消息循环，可以用于应用程序需要特别响应或处理系统消息时
// 定义退出消息处理循环的函数
/*这段代码定义了几个函数，用于控制消息处理循环的开始和结束，以及在循环中处理系统消息*/
void run_exit() { 
  is_msg_run = false;  // 设置标志，使消息处理循环停止
}

// 定义启动无限消息处理循环的函数
void run_forever() {
  if (is_msg_run)  // 如果消息处理循环已经在运行，则直接返回
    return;
  is_msg_run = true;  // 设置标志，开始消息处理循环
  msg_run();  // 调用msg_run函数进入循环
}

// 定义消息处理循环
void msg_run() {
  while (is_msg_run && hook_exec()) {
    // 这里没有内容，意味着它会持续运行hook_exec，直到is_msg_run变为false
  }
}

// 定义执行钩子和消息处理的函数
bool hook_exec() {
  static MSG msg;  // 定义一个MSG结构体，用于存储消息
  while (1) {
    // 不断尝试从消息队列中获取消息
    if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
      if (msg.message == WM_QUIT) {
        // 如果是退出消息，则退出循环
        break;
      }
      // 转换并分派消息给窗口过程函数
      TranslateMessage(&msg);
      DispatchMessage(&msg);
    }
  }
  return true;  // 返回true，表示函数执行完成
}

/*EnumProc 是一个典型的Windows回调函数，通常用于窗口枚举任务，如获取窗口的类名、标题等信息。
它可以作为参数传递给 EnumWindows、EnumChildWindows、EnumThreadWindows 等API函数。
RegDragDropCb 是一个注释掉的示例函数，展示了如何使用 EnumProc 函数来枚举窗口并注册拖拽回调。
虽然代码被注释掉了，但它提供了一个实现拖拽和放下操作的示例框架。*/
// 定义一个静态变量用于存储窗口句柄
static HWND p;
/*
这段代码定义了一个名为 EnumProc 的函数，它是一个回调函数，用于枚举窗口并执行某些操作，比如获取窗口的类名。*/
// 定义一个回调函数EnumProc，用于枚举窗口
BOOL CALLBACK EnumProc(HWND hWnd, LPARAM lParam) {
  char classname[256];  // 定义一个字符数组用于存储类名
  GetClassName(hWnd, classname, sizeof(classname));  // 获取窗口的类名并存储在classname中

  // 以下是一些示例类名，通常输出在日志或控制台中以便于调试或信息展示
  /*
  EnumProc: Static
  EnumProc: GHOST_WindowClass
  EnumProc: VNDDSKIN_SERVICES
  EnumProc: MSCTFIME UI
  EnumProc: IME
  */

//  logger->info("EnumProc: {}", classname);  // 使用日志记录类名
  if (strcmp(classname, "GHOST_WindowClass") != 0) {
    p = hWnd;  // 如果类名不是"GHOST_WindowClass"，则存储当前窗口的句柄到p
  }
  return TRUE;  // 继续枚举下一个窗口
}

// 注释掉的代码示例展示了如何注册拖拽回调
// void RegDragDropCb()
// {
//     EnumThreadWindows(GetCurrentThreadId(), EnumProc, NULL);  // 枚举当前线程的所有窗口
//     static DropTargetWin32 *droptarget = new DropTargetWin32();  // 创建一个DropTargetWin32对象
//     droptarget->m_hWnd = p;  // 设置拖拽目标窗口
//     HWND pp = GetForegroundWindow();  // 获取当前前台窗口
//     ::RevokeDragDrop(pp);  // 注销之前的拖拽处理
//     ::RegisterDragDrop(pp, droptarget);  // 注册新的拖拽处理
// }

