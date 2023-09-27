import time
from .calculated import Calculated
from .config import read_json_info
from .log import log
from pynput import mouse
from pyautogui import drag
from pynput.keyboard import Key
class Dungeon:
    def __init__(self):
        self.calculated = Calculated()

    def open_dungeon(self):
        self.calculated.check_main_interface()
        self.calculated.Keyboard.press(Key.f4)
        time.sleep(0.05)
        self.calculated.Keyboard.release(Key.f4)
        self.calculated.img_click("dungeon_main.png",overtime=2)

    def enter_dungeon(self,dungeonpath:str,nums=1):
        self.open_dungeon()
        dungeon_id = dungeonpath[dungeonpath.index("_")+1:dungeonpath.index("-")]
        dungeon_name_dir = dungeonpath[0:dungeonpath.index("-")] + ".jpg"
        # 向下滚动寻找
        if not self.calculated.img_check(dungeon_name_dir,(0,0,0,0),1):
            self.calculated.Mouse.position = self.calculated.mouse_pos((450,400))
            drag(0,-150, 1,button='left')
        self.calculated.img_click(dungeon_name_dir)
        # 向下滚动寻找
        for i in range(5):
            if not self.calculated.img_check(dungeonpath,(0,0,0,0),1):
                self.calculated.Mouse.position = self.calculated.mouse_pos((1200,900))
                drag(0,-300, 1,button='left')
            else:
                break
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
            if self.calculated.has_red((1085,930,1120,960)):
                self.calculated.img_click("dungeon_exit.jpg")
                time.sleep(2)
                return True
            self.calculated.img_click("dungeon_again.jpg")
            time.sleep(2)
            nums = nums - 1
        while not self.calculated.img_check("dungeon_again.jpg",overtime=2):
            time.sleep(5)
        self.calculated.img_click("dungeon_exit.jpg")
        self.calculated.wait_fight_end()

    def enter_dungeon_list(self,dungeonlist):
        log.info("清体力开始")
        for dungeon in dungeonlist:
            for key,value in dungeon.items():
                log.info(f"执行副本{key}---{value}")
                dungeonpath = read_json_info("dungeon.json",key,prepath="dungeon")
                self.enter_dungeon(dungeonpath,value)
        log.info("清体力结束")
