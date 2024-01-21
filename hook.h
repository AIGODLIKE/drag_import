/*在这段代码中：

使用#include包含了标准输入输出流、向量和字符串类。
通过预处理器指令定义了XLIB宏，该宏用于在Windows上标记函数为导出函数。
使用了条件编译来包含不同平台（Windows）特有的头文件。
定义了GetMsgProc函数，这是一个低级别的鼠标事件处理函数，用于处理全局鼠标事件，特别是鼠标滚轮的消息。
这段代码主要涉及底层Windows消息处理和DLL导出函数的定义，通常用于创建可以被其他语言或程序调用的库。例如，你可能会在Python中使用ctypes或其他类似库来加载这个DLL并调用其函数。在实际应用中，这样的DLL可以用来实现鼠标事件的监听、处理和响应，或者用于其他需要在底层和操作系统交互的情况。

*/
// 包含必要的头文件
#include <iostream>
#include <vector>
//#include <xstring>

// 定义XLIB宏，用于导出函数
#ifndef XLIB
  #ifdef _WIN32
  #define XLIB extern "C" __declspec(dllexport)
  #else
  #define XLIB extern "C"
  #endif
#endif

// 如果是Windows平台，包含Windows.h
#ifdef _WIN32
#include <Windows.h>
#endif

// 使用extern "C"确保函数名在编译后不会被C++编译器改变（即保持C语言链接方式）
#ifdef __cplusplus
extern "C" {
#endif

// 声明要导出的函数
XLIB void set_debug(bool);
XLIB void set_hook(bool set);
XLIB void set_wheel_status(int s);
XLIB int get_wheel_status();
XLIB WCHAR* get_dragfiles();
XLIB void clear_dragfiles();
XLIB void run_forever();
void msg_run();
bool hook_exec();

// 定义GetMsgProc回调函数，用于捕捉和处理消息，如鼠标滚轮消息
LRESULT CALLBACK GetMsgProc(int nCode, WPARAM wParam, LPARAM lParam)
{
    // 标准的hook处理模式
    if (nCode < 0)
    {
        return CallNextHookEx(NULL, nCode, wParam, lParam);
    }

    // 获取消息并处理
    LPMSG lpmsg = (LPMSG)lParam;
    UINT msg = LOWORD(lpmsg->message);

    switch (msg)
    {
    case WM_MOUSEWHEEL:
        // 当检测到鼠标滚轮事件时，在控制台输出
        std::cout << "\n WM_MOUSEWHEEL from GetMsgProc \n" <<std::endl;
        // 获取滚轮的滚动数据并输出
        MSLLHOOKSTRUCT *pMouseStruct = (MSLLHOOKSTRUCT *)lParam; // WH_MOUSE_LL struct
        int status = GET_WHEEL_DELTA_WPARAM(pMouseStruct->mouseData);
        int status2 = GET_WHEEL_DELTA_WPARAM(wParam);
        std::cout << status << " " << status2 << " " << pMouseStruct->mouseData << std::endl;
        break;
    }

    // 调用下一个hook
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

#ifdef __cplusplus
}
#endif
