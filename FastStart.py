from utils.config import get_config
from utils.StarRail import StarRail
from utils.log import log
import time
import pyuac
import subprocess
if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()
# 实例化
sra = StarRail()
# 读取配置
gamepath = get_config("gamepath")
# 配置启用
# 锄大地配置
sra.map.img_logs = get_config("img_log")
sra.map.compare_maps = get_config("compare_maps")
sra.map.team_change = get_config("team_change")
sra.map.teamid = get_config("team_id")
sra.map.id = get_config("character_id")
sra.map.skill = get_config("skill")
sra.map.run_change = get_config("run_change")
sra.map.mappath = "maps\\" + get_config("map_type")
sra.map.map_list = get_config("map_list_data")
sra.calculated.fight_time = get_config("fight_time")
sra.calculated.health_food = get_config("food")
sra.calculated.reborn_food = get_config("food")
sra.calculated.skill_food = get_config("skill_food")
# 清体力配置
sra.dungeon.team_change = get_config("team_change")
sra.dungeon.teamid = get_config("dungeon_team_id")
sra.dungeon.id = get_config("dungeon_character_id")
# 清任务配置启用
sra.task.commission_flag = get_config("task_commission")
sra.task.supportrewards_flag = get_config("task_supportrewards")
sra.task.dailytask_flag = get_config("task_rewards")
sra.task.rewards_flag = get_config("task_dailytask")
if get_config("dungeon_time_flag"):
    today_id = int(time.strftime("%w", time.localtime()))
    dungeon_time = get_config("dungeon_time")
    sra.dungeon.dungeon_list = dungeon_time[today_id]
else:
    sra.dungeon.dungeon_list = get_config("配置1")
# 单项功能是否执行
sra.map_flag = get_config("auto_map")
sra.dungeon_flag = get_config("auto_dungeon")
sra.universe_flag = get_config("auto_universe")
# 功能序列配置
sra.functional_sequence = get_config("functional_sequence")
# 自动关机配置
sra.close_game = get_config("close_game")
# 启动游戏
subprocess.Popen([gamepath],shell=True)
time.sleep(10)
# 游戏执行
sra.calculated.get_hwnd()
if sra.calculated.hwnd == 0:
    log.warning("未检测到游戏运行,请启动游戏")
else:
    sra.calculated.set_windowsize()
    # 登录
    sra.calculated.login()
    # 启动多功能执行
    sra.allfunction()
time.sleep(5)
