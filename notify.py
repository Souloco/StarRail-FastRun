import pystray
from PIL import Image
import os
import threading
import time
import win32console
import win32gui
CMD = win32console.GetConsoleWindow()
win32gui.ShowWindow(CMD, 0)  # 隐藏命令行窗口
# 退出
def on_exit(icon, item):
    icon.stop()
# 通知
def notify(msg:str):
    icon.notify(title="StarRail-FastRun", message=f"{msg}")

# 创建菜单项
menu = (
    pystray.MenuItem(text='退出', action=on_exit),                           # 最后一个菜单项
)

# 创建图标对象
image = Image.open("favicon.ico")                                                # 打开并读取图片文件
icon = pystray.Icon("StarRail-FastRun", image, "StarRail-FastRun", menu)     # 创建图标对象并绑定菜单项

# 循环监测
def listen():
    file_path = "./logs/message.txt"
    if not os.path.exists(file_path):
        with open(file_path,'w',encoding='utf-8') as file:
            file.write("初始化")
    starttime = os.path.getmtime(file_path)
    while True:
        if starttime != os.path.getmtime(file_path):
            starttime = os.path.getmtime(file_path)
            with open(file_path,'r',encoding='utf-8') as file:
                content = file.read()
            notify(content)
        time.sleep(60)
t = threading.Thread(name='notify',target=listen,daemon=True)
t.start()
icon.run()
