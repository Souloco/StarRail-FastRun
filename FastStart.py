from utils.config import get_config,read_json_info
from utils.map import Map
from utils.dungeon import Dungeon
from utils.log import log
import time
import os
import pyuac
if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()
# 读取配置
map_list_data = get_config("map_list_data")
auto_map_list_data = get_config("auto_map_list_data")
auto_map_nums = get_config("auto_map_nums")
commission = get_config("commission")
team_change = get_config("team_change")
team_id = get_config("team_id")
character_id = get_config("character_id")
img_log = get_config("img_log")
close_game = get_config("close_game")
gamepath = get_config("gamepath")
dungeon_team_id = get_config("dungeon_team_id")
dungeon_character_id = get_config("dungeon_character_id")
dungeon_config = read_json_info("dungeon.json","配置1",prepath="dungeon")
# 启动游戏
os.startfile(gamepath)
# 实例化
auto_map = Map()
auto_dungeon = Dungeon()
time.sleep(10)
# 游戏执行
auto_map.calculated.get_hwnd()
auto_dungeon.calculated.get_hwnd()
if auto_map.calculated.hwnd == 0:
    log.warning("未检测到游戏运行,请启动游戏")
else:
    auto_map.calculated.set_windowsize()
    # 截图记录
    auto_map.calculated.img_log_value = img_log
    # 登录
    auto_map.calculated.login()
    # 委托
    if commission:
        auto_map.calculated.commission()
    # 清体力队伍切换
    auto_dungeon.calculated.set_windowsize()
    if team_change:
        auto_dungeon.calculated.change_team(teamid=dungeon_team_id,id=dungeon_character_id)
    # 清体力
    auto_dungeon.enter_dungeon_list(dungeon_config)
    # 锄大地队伍切换
    if team_change:
        auto_map.calculated.change_team(teamid=team_id,id=character_id)
    # 锄大地
    auto_map.map_init()
    auto_map.Enter_map_all(map_list_data,auto_map_list_data,close_game,auto_map_nums)
time.sleep(5)