import time
from .calculated import Calculated
from .config import read_json_info,message
from .log import log
from pynput import mouse
from pyautogui import drag
from pynput.keyboard import Key
class Dungeon:
    def __init__(self,base:Calculated = Calculated()):
        self.calculated = base
        self.team_change = False
        self.teamid = 1
        self.id = 1
        self.index_find_nums,self.dungeon_find_nums = self.dungeon_find_init()
        self.dungeon_list = []

    def dungeon_find_init(self):
        """
        说明:
            配置的副本数量搜寻次数初始化
        """
        dungeon_indexlist = read_json_info("dungeon.json","indexname",prepath="dungeon")
        index_find_nums = len(dungeon_indexlist) // 2
        dungeon_find_nums = 0
        for name in dungeon_indexlist:
            dungeon_list = read_json_info("dungeon.json",name,prepath="dungeon")
            nums = len(dungeon_list) // 2
            if dungeon_find_nums < nums:
                dungeon_find_nums = nums
        return index_find_nums,dungeon_find_nums

    def open_dungeon(self):
        self.calculated.check_main_interface()
        starttime = time.time()
        maxtime = 100
        while not self.calculated.img_check("universe.jpg",overtime=1) and time.time() - starttime < maxtime:
            self.calculated.Keyboard.press(Key.f4)
            time.sleep(0.05)
            self.calculated.Keyboard.release(Key.f4)
            self.calculated.img_click("dungeon_main.png",overtime=2)

    def enter_dungeon(self,dungeonpath:str,nums=1):
        self.open_dungeon()
        dungeon_id = dungeonpath[dungeonpath.index("_")+1:dungeonpath.index("-")]
        dungeon_name_dir = dungeonpath[0:dungeonpath.index("-")] + ".jpg"
        # 向下滚动寻找
        for i in range(self.index_find_nums):
            if not self.calculated.img_check(dungeon_name_dir,(0,0,0,0),1):
                self.calculated.Mouse.position = self.calculated.mouse_pos((450,400))
                drag(0,-150, 1,button='left')
        time.sleep(0.7)
        self.calculated.img_click(dungeon_name_dir)
        # 向下滚动寻找
        for i in range(self.dungeon_find_nums):
            if not self.calculated.img_check(dungeonpath,(0,0,0,0),1):
                self.calculated.Mouse.position = self.calculated.mouse_pos((1200,900))
                drag(0,-300, 1,button='left')
            else:
                break
        time.sleep(1.2)
        self.calculated.dungeon_img_click(dungeonpath)
        time.sleep(2)
        while not self.calculated.img_check("dungeon_fight1.jpg",overtime=1.0):
            time.sleep(1)
        if self.calculated.has_red((1250,950,1300,1000)):
            log.info("退出副本")
            self.calculated.img_click("exit.jpg")
            time.sleep(0.5)
            return True
        log.info("进入副本")
        self.calculated.img_click("dungeon_fight1.jpg")
        if self.calculated.img_check("dungeon_fight2.jpg",overtime=2):
            self.calculated.img_click("dungeon_fight2.jpg")
            self.calculated.img_click("sure.jpg",(1118,650,1225,693))
        else:
            self.calculated.img_click("exit3.jpg")
            self.calculated.img_click("exit.jpg")
            time.sleep(0.5)
            return True
        # 凝滞虚影主动打怪
        if dungeon_id == '3':
            self.calculated.wait_main_interface()
            self.calculated.fighting(2)
        while nums > 1:
            while not self.calculated.img_check("dungeon_again.jpg",overtime=2):
                time.sleep(5)
            if self.calculated.has_red((1085,930,1120,960)) and self.calculated.img_click("dungeon_exit.jpg"):
                time.sleep(2)
                return True
            self.calculated.img_click("dungeon_again.jpg")
            self.calculated.img_click("sure.jpg",(1118,650,1225,693))
            # 历战余响次数用尽
            if dungeon_id == '5' and self.calculated.img_click("exit3.jpg"):
                return True
            time.sleep(2)
            nums = nums - 1
        while not self.calculated.img_check("dungeon_again.jpg",overtime=2):
            time.sleep(5)
        self.calculated.img_click("dungeon_exit.jpg")
        self.calculated.wait_fight_end()

    def start(self):
        log.info("游戏初始化设置")
        self.calculated.set_windowsize()
        if self.team_change:
            log.info("清体力---切换队伍")
            self.calculated.change_team(self.teamid,self.id)
        log.info("清体力---开始")
        for dungeon in self.dungeon_list:
            for key,value in dungeon.items():
                log.info(f"清体力---执行副本{key}---{value}")
                dungeonpath = read_json_info("dungeon.json",key,prepath="dungeon")
                self.enter_dungeon(dungeonpath,value)
        log.info("清体力---执行完毕")
        message("清体力---执行完毕")
