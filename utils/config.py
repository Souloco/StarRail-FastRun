import json
import os
import cv2 as cv
import sys
# 路径
if getattr(sys, 'frozen', False):
    root_dir = os.path.dirname(sys.executable)
elif __file__:
    root_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
# picture路径
picture_dir = os.path.join(root_dir,"picture")
# model路径
model_dir = os.path.join(root_dir,"model")
# dungeon路径
dungeon_dir = os.path.join(root_dir,"dungeon")
# 配置文件名字
CONFIG_FILE_NAME = "config.json"
def read_map(map_type="map"):
    """
    说明：
        读取地图文件
    """
    map_list = os.listdir(os.path.join(root_dir,f"maps\\{map_type}"))
    return map_list

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

def read_maplist_name(map_type="map"):
    """
    说明：
        读取map列表的info字段信息，返回列表
    参数：
        map：地图json名字
        info:信息字段
    """
    map_list = read_map(map_type)
    map_name_list = []
    for map in map_list:
        with open(os.path.join(root_dir,f"maps\\{map_type}\\{map}"),encoding='utf-8') as f:
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
    fontsize = 10
    fontfamily = "Microsoft YaHei UI"
    skill = False
    skill_food = False
    auto_map_hide = True
    map_type = "map"
    proxy = "https://gh-proxy.com/"
    配置1 = []
    配置2 = []
    配置3 = []
    配置4 = []
    配置5 = []
    dungeon_time = ["配置1","配置1","配置1","配置1","配置1","配置1","配置1"]
    dungeon_time_flag = False
    universe_bonus = 0
    universe_nums = 34
    auto_universe = False
def check_config():
    with open(os.path.join(root_dir,CONFIG_FILE_NAME),"r",encoding='utf-8') as f:
        data = json.load(f)
    for key,item in Config.__dict__.items():
        if '__' not in key and key not in data:
            set_config(key,item)
    return True
def message(msg:str):
    with open(os.path.join(root_dir,"logs","message.txt"),"w",encoding='utf-8') as f:
        f.write(f"{msg}")
    return True
