from utils.calculated import Calculated
from pynput import keyboard
import time
import os
import orjson
base = Calculated()
# 游戏初始化设置
base.get_hwnd()
base.set_windowsize()
base.active_window()
# 可记录的按键列表
key_list = ['w','a','s','d']
# 记录按键按下的时间
key_down_time = {}
# 记录按键顺序及时间
key_event_list = []
# 保存文件名字
save_name = "map_X-X_X"
# 每次水平移动视角距离数值px
mouse_move_value = 100
# 记录最终水平移动视角距离数据
last_move_value = 0

# 按下触发事件
def on_press(key):
    # 记录当前时间
    current_time = time.perf_counter()
    try:
        if key.char in key_list and key.char not in key_down_time:
            key_down_time[key.char] = current_time
            print("按键按下:",key.char,current_time)
    except AttributeError:
        pass

# 释放触发事件
def on_release(key):
    global last_move_value
    # 记录当前时间
    current_time = time.perf_counter()

    # 水平移动视角mouse_move映射|loc_angle映射
    if key == keyboard.Key.left:
        last_move_value = last_move_value - mouse_move_value
        base.mouse_move(mouse_move_value*-1)
        print(f"当前记录水平移动距离:{last_move_value}")
    elif key == keyboard.Key.right:
        last_move_value = last_move_value + mouse_move_value
        base.mouse_move(mouse_move_value)
        print(f"当前记录水平移动距离:{last_move_value}")
    # loc_angle映射
    elif key == keyboard.Key.f7:
        angle = base.get_loc_angle()
        key_event_list.append({"loc_angle":angle})
        print(f"已记录最终位置角度loc_angle:{angle}")
        last_move_value = 0
    elif last_move_value != 0:
        key_event_list.append({"mouse_move":last_move_value})
        print(f"已记录最终水平移动距离mouse_move:{last_move_value}")
        last_move_value = 0
    # 可记录按键(非特殊)映射
    try:
        if key.char in key_list and key.char in key_down_time:
            key_time = current_time-key_down_time[key.char]
            print(f"{key.char}按下了{key_time}秒")
            key_event_list.append({key.char:key_time})
            print(key_event_list)
            del key_down_time[key.char]
    except AttributeError:
        pass
    if key == keyboard.Key.f9:
        save_json()
        return False

# 保存录制文件
def save_json():
    global save_name
    save_dict = {
        "name": "地图-编号",
        "author": "作者",
        "start": [],
        "map": []
    }
    save_dict["map"] = key_event_list
    if not os.path.exists("maps/save"):
        os.makedirs("maps/save")
    with open(f'maps/save/{save_name}.json', 'wb') as f:
        f.write(orjson.dumps(save_dict, option=orjson.OPT_INDENT_2))

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:  # 创建按键监听线程
    listener.join()  # 等待按键监听线程结束
