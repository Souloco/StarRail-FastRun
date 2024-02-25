from utils.calculated import Calculated
from pynput import keyboard
import time
import os
import orjson
base = Calculated()
# 可记录的按键列表
key_list = ['w','a','s','d']
# 记录按键按下的时间
key_down_time = {}
# 记录按键顺序及时间
key_event_list = []
# 保存文件名字
save_name = "map_X-X_X"

# 按下触发事件
def on_press(key):
    # 记录当前时间
    current_time = time.perf_counter()
    try:
        if key.char in key_list and key.char not in key_down_time:
            key_down_time[key.char] = current_time
            print("按键按下:",key.char,current_time)
    except AttributeError:
        # print('特殊键： {} 被按下'.format(key))
        pass

# 释放触发事件
def on_release(key):
    # 记录当前时间
    current_time = time.perf_counter()
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
