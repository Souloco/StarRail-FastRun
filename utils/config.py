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

# 配置文件名字
CONFIG_FILE_NAME = "config.json"
def compare_map(item:str):
    planet_id = item[item.index('_') + 1:item.index('-')].zfill(2)
    map_id = item[item.index('-') + 1:item.index('_',5)].zfill(2)
    index_id = item[item.index('_',5) + 1:item.index('.')].zfill(2)
    return planet_id + map_id + index_id
def read_map(map_type="map"):
    """
    说明：
        读取地图文件
    """
    map_list = os.listdir(os.path.join(root_dir,f"maps\\{map_type}"))
    map_list.sort(key=compare_map)
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
    json_path = os.path.join(root_dir,prepath,path)
    try:
        with open(json_path,encoding='utf-8') as f:
            data = json.load(f)
            info_list = data[info]
        return info_list
    except Exception:
        print(json_path + f"读取{info}字段信息失败")
        raise

def set_json_info(path,info:str,value,prepath=""):
    json_path = os.path.join(root_dir,prepath,path)
    with open(json_path,"r",encoding='utf-8') as f:
        data = json.load(f)
        data[info] = value
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)

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
def read_picture(imgname,prepath="picture"):
    """
    说明：
        读取图片
    参数：
        imgpath：图片名
        prepath: 修补目录
    """
    imgpath = os.path.join(root_dir,prepath,imgname)
    try:
        if os.path.exists(imgpath):
            img = cv.imread(imgpath)
            return img
        else:
            print(f"{imgpath}图片路径不存在")
            return False
    except Exception:
        print(f"{imgpath}图片读取失败")
        return False

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
    character_id = 4
    dungeon_character_id = 1
    close_game = 0
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
    skill_make = False
    skill_buy = False
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
    universe_rewards = False
    auto_map = False
    auto_dungeon = False
    run_change = False
    fight_time = 900
    task_commission = False
    task_supportrewards = False
    task_rewards = False
    task_dailytask = False
    food = False
    functional_sequence = ["commisson","supportrewards","dungeon","skill_buy","skill_make","map","Universe","dailytask","rewards"]
    compare_maps = False
    rotation = 1.0


def check_config():
    config_path = os.path.join(root_dir,CONFIG_FILE_NAME)
    # 如果不存在先创建空白json
    if not os.path.exists(config_path):
        with open(config_path,"w",encoding='utf-8') as f:
            json.dump({},f)
            f.close()
    # 缺少配置补充默认值
    with open(config_path,"r",encoding='utf-8') as f:
        data = json.load(f)
        for key,item in Config.__dict__.items():
            if '__' not in key and key not in data:
                set_config(key,item)
    return True

def check_map_config():
    config_path = os.path.join(root_dir,'maps',CONFIG_FILE_NAME)
    # 如果不存在先创建空白json
    if not os.path.exists(config_path):
        with open(config_path,"w",encoding='utf-8') as f:
            json.dump({},f)
            f.close()
    # 获取路线种类
    map_types = get_map_types()
    # 缺少配置补充默认值
    with open(config_path,"r",encoding='utf-8') as f:
        data = json.load(f)
        for type in map_types:
            info = type + '_sequence'
            if info not in data:
                set_json_info(CONFIG_FILE_NAME,info,[],"maps")

def get_map_types():
    map_types = os.listdir(os.path.join(root_dir,'maps'))
    map_types = [item for item in map_types if os.path.isdir(os.path.join(root_dir,'maps',item))]
    map_types.remove('save')
    map_types.remove('special')
    return map_types

def message(msg:str):
    with open(os.path.join(root_dir,"logs","message.txt"),"w",encoding='utf-8') as f:
        f.write(f"{msg}")
    return True
