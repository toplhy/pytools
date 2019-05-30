import os
import sys
import time
import win32api
import win32gui

import win32con

everything_dir = r'C:\Program Files\Everything\Everything.exe'
idea_dir = r'C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.5\bin\idea64.exe'
wechat_dir = r'C:\Program Files (x86)\Tencent\WeChat\WeChat.exe'
tim_dir = r'C:\Program Files (x86)\Tencent\TIM\Bin\QQScLauncher.exe'


# 测试网络联通
def test_network():
    network = 1
    index = 0
    while network != 0 and index < 10:
        time.sleep(1)
        index += 1
        network = os.system("ping www.baidu.com")
        print("第%s次，结果是：%s"%(index, network))
    return True if(network == 0) else False


# 启动Everything后最小化
def open_everything():
    os.startfile(everything_dir)
    everything_handle = 0
    # 找到窗口句柄
    while everything_handle == 0:
        time.sleep(1)
        everything_handle = win32gui.FindWindow("EVERYTHING", "Everything")
    # 将窗口最小化
    win32gui.CloseWindow(everything_handle)


# 启动微信并点击“登录”
def open_wechat():
    if test_network():
        os.startfile(wechat_dir)
        wechat_handle = 0
        # 找到窗口句柄
        while wechat_handle == 0:
            time.sleep(1)
            wechat_handle = win32gui.FindWindow("WeChatLoginWndForPC", "登录")
        # 获取窗口位置
        left, top, right, bottom = win32gui.GetWindowRect(wechat_handle)
        # 鼠标定位到"登录"按钮
        win32api.SetCursorPos([int((right - left) / 2 + left), int(((bottom - top) / 3) * 2 + top)])
        # 鼠标点击
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


# 启动Tim并点击“扫码登录”
def open_tim():
    if test_network():
        os.startfile(tim_dir)
        tim_handle = 0
        # 找到窗口句柄
        while tim_handle == 0:
            time.sleep(1)
            tim_handle = win32gui.FindWindow("TXGuiFoundation", "TIM")
        # 获取窗口位置521,197,1015,667
        left, top, right, bottom = win32gui.GetWindowRect(tim_handle)
        # 鼠标定位到"扫码登录"图标
        win32api.SetCursorPos([int(right - 50), int(bottom - 100)])
        # 鼠标点击
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


# 启动IDEA
def open_idea():
    os.startfile(idea_dir)


if __name__ == "__main__":
    open_everything()
    open_idea()
    open_wechat()
    open_tim()
    sys.exit()
