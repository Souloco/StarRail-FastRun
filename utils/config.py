import json
import os
import cv2 as cv
import sys
# 路径
if getattr(sys, 'frozen', False):
    root_dir = os.path.dirname(sys.executable)
elif __file__:
    root_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
# map路径
map_dir = os.path.join(root_dir,"map")
# picture路径
picture_dir = os.path.join(root_dir,"picture")
# model路径
model_dir = os.path.join(root_dir,"model")
# dungeon路径
dungeon_dir = os.path.join(root_dir,"dungeon")
# 配置文件名字
CONFIG_FILE_NAME = "config.json"
def set_dir(root_path):
    """
    说明：
        刷新路径
    参数：
        root_path：替换后的根路径
    """
    global root_dir
    global picture_dir
    global map_dir
    global model_dir
    root_dir = root_path
    map_dir = os.path.join(root_path,"map")
    picture_dir = os.path.join(root_path,"picture")
    model_dir = os.path.join(root_path,"model")
def read_map():
    """
    说明：
        读取地图文件
    """
    map_list = os.listdir(map_dir)
    return map_list
def read_map_name():
    """
    说明：
        读取地图文件名字，返回列表
    """
    map_list = read_map()
    map_name_list = []
    map_planet_list = []
    for map in map_list:
        planet_id = int(map[map.index('_') + 1:map.index('-')])
        with open(os.path.join(map_dir,map),encoding='utf-8') as f:
            data = json.load(f)
            map_name = data["name"]
            if len(map_name_list) < planet_id:
                map_name_list.append([])
                map_planet_list.append([])
            map_name_list[planet_id-1].append(map_name)
            map_planet_list[planet_id-1].append(map)
    return map_name_list,map_planet_list
def read_json_info(path,info,prepath=""):
    """
    说明：
        读取单个json的info字段信息
    参数：
        path：json名字
        info:信息字段
        prepath:修补目录
    """
    with open(os.path.join(root_dir,prepath,path),encoding='utf-8') as f:
        data = json.load(f)
        info_list = data[info]
    return info_list

def save_dungeon_info(dungeon,info,value):
    """
    说明：
        保存单个dungeon的info字段信息
    参数：
        dungeon：地图json
        info:信息字段
    """
    with open(os.path.join(dungeon_dir,dungeon),"r",encoding='utf-8') as f:
        data = json.load(f)
        data[info] = value
    with open(os.path.join(dungeon_dir,dungeon), "w", encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)

def read_maplist_name():
    """
    说明：
        读取map列表的info字段信息，返回列表
    参数：
        map：地图json名字
        info:信息字段
    """
    map_list = read_map()
    map_name_list = []
    for map in map_list:
        with open(os.path.join(map_dir,map),encoding='utf-8') as f:
            data = json.load(f)
            map_name = data["name"]
        map_name_list.append(map_name)
    return map_name_list
def read_picture(imgpath):
    """
    说明：
        读取图片
    参数：
        imgpath：图片名
    """
    img = cv.imread(os.path.join(picture_dir,imgpath))
    return img

def set_config(info:str,value):
    with open(os.path.join(root_dir,CONFIG_FILE_NAME),"r",encoding='utf-8') as f:
        data = json.load(f)
        data[info] = value
    with open(os.path.join(root_dir,CONFIG_FILE_NAME), "w", encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)

def get_config(info:str):
    with open(os.path.join(root_dir,CONFIG_FILE_NAME),"r",encoding='utf-8') as f:
        data = json.load(f)
        info_list = data[info]
        return info_list
class Config():
    auto_map_list_data = []
    auto_map_nums = 0
    character_id = 4
    dungeon_character_id = 1
    close_game = False
    img_log = False
    map_list_data = []
    team_change = False
    team_id = 1
    dungeon_team_id = 1
    commission = False
    gamepath = ""
