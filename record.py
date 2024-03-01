'''
author: Souloco
modify: Klamist
2024-3-1 18:30:11
StarRail-FastRun的map.json录制脚本，保存在map/save
不要同时按多个键，疾跑先按住shift或鼠标右键再赶路（转弯时注意衔接不要掉速）
鼠标操作请使用攻击键、转向键（绝对转向时可先用鼠标瞄准）
交互键按下之前，请先超快短按补一个wasd位移，录入蹭的方向（例如先w再f最终记为f:w）
主控键：
    F8保存+重录，F9保存+退出，F10闪退
赶路键：
    W A S D E F R，移动、交互、秘技
等待键：
    Q，根据按住的时间添加delay，用于原地等待
鼠标操作：
    攻击键：X打怪，V打罐子
    转向键：<和>键(M键右边俩)让角色转向，可多次点按叠加直到转向目标
    绝对转向：手动转到目标方向，然后按F7键，通过小地图箭头记录视角(get_loc_angle)
    视角转正：方向键↑↓←→，视角转朝小地图对应方向(loc_angle)
'''

import time 
import os
from datetime import datetime
from utils.calculated import Calculated
from pynput import keyboard
import orjson
from win32 import win32api
import ctypes
import pyuac
# 以管理员身份启动
if __name__ == '__main__':
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()

calcu = Calculated()
# 游戏初始化设置
calcu.get_hwnd()
calcu.set_windowsize()
calcu.active_window()
ctypes.windll.user32.SetProcessDPIAware()
scale = ctypes.windll.user32.GetDpiForSystem() / 96.0
# 可记录的按键列表
key_list = ['w','a','s','d','e','f','r','x','v','q']
# 使用键秘技键分别是啥
use_key = "f"
skill_key = "e"
# 记录按键按下的时间
key_down_time = {}
# 记录按键顺序及时间
key_event_list = []
# 保存文件名字
save_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
# 每次水平移动视角距离数值px
mouse_move_value = 100
# 记录最终水平移动视角距离数据
last_move_value = 0

print("开始录制")

# 鼠标位移
def mouse_move(value:int):
    # log.info(f"视角转向{value}")
    win32api.mouse_event(1,int(value*scale),0)

# 按下触发事件
def on_press(key):
    # 记录当前时间
    current_time = time.perf_counter()
    try:
        if key.char in key_list and key.char not in key_down_time:
            key_down_time[key.char] = current_time
            # print("按键按下:",key.char,current_time)
    except AttributeError:
        pass

# 释放触发事件
def on_release(key):
    global last_move_value, key_event_list
    # 记录当前时间
    current_time = time.perf_counter()

    # 记录：赶路键、攻击键、转向键
    try:
        if key.char in key_list and key.char in key_down_time:
            key_time = current_time - key_down_time[key.char]
            if last_move_value != 0:
                key_event_list.append({"mouse_move":last_move_value})
                print(f"最终视角平移mouse_move:{last_move_value}")
                last_move_value = 0
            if key.char == use_key:  # 交互键参数使用上一步位移的方向
                last_way, = key_event_list[-1]
                last_time, = key_event_list[-1].values()
                if last_time < 0.15 and last_way in ['w','a','s','d']:  # 若提前超短位移，就替换为蹭f
                    del key_event_list[-1]
                    key_event_list.append({"f": last_way})
                    print(f"f 朝{last_way}方向蹭交互")
                else:
                    print("f 未提供方向")
            elif key.char == skill_key:
                key_event_list.append({"e": 1.2})
                print("e 使用秘技")
            elif key.char == 'q':
                key_event_list.append({"delay": key_time})
                print(f"在此停顿{key_time}秒")
            elif key.char == 'r':
                key_event_list.append({"r": 1.0})
                print("r 放泡泡")
            elif key.char == 'x':
                key_event_list.append({"fighting": 1})
                print("x 打怪入战")
                win32api.mouse_event(2 | 4,0,0)
            elif key.char == 'v':
                key_event_list.append({"fighting": 2})
                print("v 打罐子")
                win32api.mouse_event(2 | 4,0,0)
            elif key_time > 0.01:  # 忽略loc_angle导致的超短位移输入
                key_event_list.append({key.char:key_time})
                print(f"{key.char} 跑路{key_time}秒")
            del key_down_time[key.char]
        # 水平移动视角mouse_move映射
        elif key.char == ',':
            last_move_value = last_move_value - mouse_move_value
            mouse_move(mouse_move_value*-1)
            # print(f"当前记录水平移动距离:{last_move_value}")
        elif key.char == '.':
            last_move_value = last_move_value + mouse_move_value
            mouse_move(mouse_move_value)
            # print(f"当前记录水平移动距离:{last_move_value}")
    except AttributeError:
        pass
    # loc_angle定位
    if key == keyboard.Key.f7:
        angle = calcu.get_loc_angle()
        key_event_list.append({"loc_angle":angle})
        print(f"当前视角朝向loc_angle:{angle}")
        last_move_value = 0
    # 方向键定向转到小地图的正上下左右
    elif key == keyboard.Key.left:
        calcu.correct_loc_angle(180)
        key_event_list.append({"loc_angle": 180})
        print("视角转正loc_angle: 180")
    elif key == keyboard.Key.right:
        calcu.correct_loc_angle(0)
        key_event_list.append({"loc_angle": 0})
        print("视角转正loc_angle: 0")
    elif key == keyboard.Key.up:
        calcu.correct_loc_angle(90)
        key_event_list.append({"loc_angle": 90})
        print("视角转正loc_angle: 90")
    elif key == keyboard.Key.down:
        calcu.correct_loc_angle(270)
        key_event_list.append({"loc_angle": 270})
        print("视角转正loc_angle: 270")
    # F10直接闪退
    if key == keyboard.Key.f10:
        return False
    # F9键保存之前的内容，并退出程序
    if key == keyboard.Key.f9:
        print(key_event_list)
        save_json()
        print("保存")
        return False
    # F8键保存之前的内容，并清空列表，继续录新的
    elif key == keyboard.Key.f8:
        save_json()
        print("保存")
        key_event_list = []
        save_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# 保存录制文件
def save_json():
    global save_name, key_event_list
    save_dict = {
        "name": "地图",
        "author": "作者",
        "start": [],
        "map": []
    }
    save_dict["map"] = key_event_list
    if not os.path.exists("maps/save"):
        os.makedirs("maps/save")
    with open(f'maps/save/{save_name}.json', 'wb') as f:
        f.write(orjson.dumps(save_dict, option=orjson.OPT_INDENT_2))

# 创建监听线程并等待结束
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
