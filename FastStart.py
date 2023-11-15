from utils.config import get_config,read_json_info
from utils.map import Map
from utils.dungeon import Dungeon
from utils.log import log
import time
import os
import pyuac
if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()
# 实例化
auto_map = Map()
auto_dungeon = Dungeon()
# 读取配置
map_list_data = get_config("map_list_data")
auto_map_list_data = get_config("auto_map_list_data")
gamepath = get_config("gamepath")
if get_config("dungeon_time_flag"):
    today_id = int(time.strftime("%w", time.localtime()))
    dungeon_time = get_config("dungeon_time")
    dungeon_config = dungeon_time[today_id]
else:
    dungeon_config = get_config("配置1")
# 配置启用
auto_map.calculated.img_log_value = get_config("img_log")
auto_map.team_change = get_config("team_change")
auto_map.teamid = get_config("team_id")
auto_map.id = get_config("character_id")
auto_map.commission = get_config("commission")
auto_map.close_game = get_config("close_game")
auto_map.nums = get_config("auto_map_nums")
auto_dungeon.team_change = get_config("team_change")
auto_dungeon.teamid = get_config("dungeon_team_id")
auto_dungeon.id = get_config("dungeon_character_id")
# 启动游戏
os.startfile(gamepath)
time.sleep(10)
# 游戏执行
auto_map.calculated.get_hwnd()
auto_dungeon.calculated.get_hwnd()
if auto_map.calculated.hwnd == 0:
    log.warning("未检测到游戏运行,请启动游戏")
else:
    auto_map.calculated.set_windowsize()
    # 登录
    auto_map.calculated.login()
    # 清体力
    auto_dungeon.start(dungeon_config)
    # 锄大地
    auto_map.start(map_list_data,auto_map_list_data)
time.sleep(5)
