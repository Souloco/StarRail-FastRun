import win32gui
import time
from .config import read_json_info,message
from .calculated import Calculated
from .log import log
from pynput import mouse
from pyautogui import drag
class Map:
    def __init__(self,base:Calculated = Calculated()):
        self.calculated = base
        self.team_change = False
        self.teamid = 1
        self.id = 1
        self.nums = 0
        self.skill = True
        self.skill_food = True
        self.mappath = "maps\\map"
        self.planetid = 0
        self.run_change = False
        self.map_list = []
        self.auto_map_list = []

    def Enter_map_start(self,mapjson):
        """
        说明:
            执行mapjson的start列表
        参数:
            mapjson:路线json名
        """
        start_list = read_json_info(mapjson,"start",prepath=self.mappath)
        map_name_dir = mapjson[0:mapjson.index("_",5)] + ".jpg"
        map_name = read_json_info(mapjson,"name",prepath=self.mappath).split("-")[0]
        planet_id = int(mapjson[mapjson.index('_') + 1:mapjson.index('-')])
        # map_id = str(mapjson[mapjson.index('_') + 1:mapjson.rindex('_')])
        for start in start_list:
            for key,value in start.items():
                if key == "map":
                    # 激活窗口
                    win32gui.SetForegroundWindow(self.calculated.hwnd)
                    self.calculated.wait_main_interface()
                    if not self.calculated.ocr_check(map_name,(0,0,200,40),1,mode=2):
                        # 进入地图
                        self.calculated.open_map()
                        # 进入星球
                        if self.planetid != planet_id:
                            self.planetid = planet_id
                            log.info("进入星球")
                            for i in range(3):
                                if self.calculated.img_check("planet_navigation.jpg",(40,40,100,100),2):
                                    break
                                else:
                                    self.calculated.img_click("Enter_planet.jpg",(1440,115,1870,160))
                            planet_img = "orientation_{planet_id}.jpg".format(planet_id=planet_id)
                            for i in range(3):
                                if self.calculated.img_check("map_navigation.jpg",(40,40,100,100),2):
                                    break
                                else:
                                    if not self.calculated.img_click(planet_img,overtime=2):
                                        self.calculated.Mouse.position = self.calculated.mouse_pos((1000,100))
                                        drag(400,0, 1,button='left')
                        # 进入地名
                        log.info("进入地名")
                        # 滚动寻找
                        # 向下滚动寻找
                        for i in range(4):
                            if not self.calculated.img_check(map_name_dir,(1420,180,1890,1020),1):
                                self.calculated.Mouse.position = self.calculated.mouse_pos((1750,250))
                                for j in range(2):
                                    self.calculated.Mouse.scroll(0,-200)
                            else:
                                break
                        # 向上滚动寻找
                        for i in range(4):
                            if not self.calculated.img_check(map_name_dir,(1420,180,1890,1020),1):
                                self.calculated.Mouse.position = self.calculated.mouse_pos((1750,250))
                                for j in range(2):
                                    self.calculated.Mouse.scroll(0,200)
                            else:
                                break
                        self.calculated.img_click(map_name_dir,(1420,180,1890,1020),2)
                    else:
                        # 进入地图
                        self.calculated.open_map()
                    if value != "":
                        # 进入层数
                        log.info(f"进入{value}层")
                        self.find_floor(value)
                elif "point" in key:
                    log.info("寻找传送点")
                    self.find_transfer_point(key)
                    self.calculated.img_click(key,(0,0,0,0),overtime=value)
                elif key == "transfer":
                    log.info("进行传送")
                    if not self.calculated.img_click("transfer.jpg",(1470,945,1840,1000),overtime=value):
                        self.calculated.img_click("transfer1.jpg",overtime=0.5)
                        self.calculated.img_click("transfer2.jpg",overtime=0.5)
                        self.calculated.img_click("transfer3.png",overtime=0.5)
                        self.calculated.img_click("transfer.jpg",(1470,945,1840,1000),overtime=value)
                    time.sleep(3)
                    self.calculated.check_main_interface()
                    # 复活切换远程角色
                    if self.team_change:
                        self.calculated.change_team(0,self.id)
                else:
                    self.calculated.img_click(key,(0,0,0,0),overtime=value)

    def find_transfer_point(self,key):
        """
        说明:
            寻找传送点
        """
        start_time = time.time()
        while not self.calculated.img_check(key,(0,0,0,0),1) and time.time() - start_time < 30:
            # 向下滚动寻找
            for i in range(3):
                if not self.calculated.img_check(key,(0,0,0,0),1):
                    self.calculated.Mouse.position = self.calculated.mouse_pos((1330,440))
                    drag(0,-400, 1,button='left')
                else:
                    break
            # 向左滚动寻找
            for i in range(3):
                if not self.calculated.img_check(key,(0,0,0,0),1):
                    self.calculated.Mouse.position = self.calculated.mouse_pos((1330,440))
                    drag(400,0, 1,button='left')
                else:
                    break
            # 向上滚动寻找
            for i in range(3):
                if not self.calculated.img_check(key,(0,0,0,0),1):
                    self.calculated.Mouse.position = self.calculated.mouse_pos((1330,640))
                    drag(0,400, 1,button='left')
                else:
                    break
            # 向右滚动寻找
            for i in range(3):
                if not self.calculated.img_check(key,(0,0,0,0),1):
                    self.calculated.Mouse.position = self.calculated.mouse_pos((1330,440))
                    drag(-400,0, 1,button='left')
                else:
                    break

    def find_floor(self,value):
        """
        说明：
            寻找楼层
        """
        self.calculated.ocr_click(value+"层",(0,700,125,1010),1)
        self.calculated.img_click(f"floor_{value}.png",(0,700,125,1010),1,rates=0.95)

    def Enter_map_fighting(self,mapjson):
        """
        说明:
            执行mapjson的map列表
        参数:
            mapjson:路线json名
        """
        map_name = mapjson[0:mapjson.index(".")]
        operate_list = read_json_info(mapjson,"map",prepath=self.mappath)
        for operate in operate_list:
            step_num = 0
            for key,value in operate.items():
                if key in ["w","s","a","d"]:
                    self.calculated.move(key,value)
                elif key == "e" and self.skill:
                    self.skill_food = self.calculated.use_skill(self.skill_food,value)
                elif key == "fighting":
                    self.calculated.fighting(value)
                elif key == "mouse_move":
                    self.calculated.mouse_move(value)
                elif key == "f":
                    self.calculated.interaction(value)
                elif key == "r":
                    self.calculated.key_press("r")
                    time.sleep(2)
                elif key == "delay":
                    time.sleep(value)
            # logtime = time.strftime("%m-%d-%H-%M-%S",time.localtime())
                step_num += 1
            self.calculated.save_screenshot(f"{map_name}---{step_num}-{operate}")

    def Enter_map_onejson(self,mapjson):
        """
        说明:
            执行单个mapjson
        参数:
            mapjson:路线json名
        """
        map_name = read_json_info(mapjson,"name",prepath=self.mappath)
        log.info(f"当前执行路线:{map_name}")
        self.Enter_map_start(mapjson)
        self.Enter_map_fighting(mapjson)

    def Enter_map_jsonlist(self,jsonlist):
        """
        说明:
            执行json列表
        参数:
            mapjson:路线json列表
        """
        for mapjson in jsonlist:
            self.Enter_map_onejson(mapjson)

    def map_init(self):
        log.info("地图初始化")
        self.calculated.Keyboard.press("m")
        self.calculated.Keyboard.release("m")
        self.calculated.img_check("map_navigation.jpg",(40,40,100,100),2)
        self.calculated.img_click("return.jpg",overtime=1)
        self.calculated.img_click("map_init_2.jpg",(600,970,660,1000))
        while not self.calculated.img_check("map_init_1.jpg",(660,970,695,1000),0.5):
            self.calculated.Mouse.press(mouse.Button.left)
            time.sleep(2)
            self.calculated.Mouse.release(mouse.Button.left)
        self.calculated.Keyboard.press("m")
        self.calculated.Keyboard.release("m")
        time.sleep(1)

    def start(self):
        log.info("游戏初始化设置")
        self.calculated.set_windowsize()
        self.calculated.check_main_interface()
        if self.run_change:
            log.info("锄大地---疾跑模式切换")
            self.calculated.run_change(1)
        if self.team_change:
            log.info("锄大地---切换队伍")
            self.calculated.change_team(self.teamid,self.id)
        log.info("锄大地---地图初始化")
        self.map_init()
        log.info("锄大地---必跑路线")
        self.Enter_map_jsonlist(self.map_list)
        log.info("锄大地---重跑路线")
        for i in range(self.nums):
            self.Enter_map_jsonlist(self.auto_map_list)
        if self.run_change:
            log.info("锄大地---疾跑模式切换")
            self.calculated.run_change(0)
        log.info("锄大地---执行完毕")
        message("锄大地---执行完毕")

    def check_map(self):
        log.info("锄大地---打开背包")
        self.calculated.Keyboard.press('b')
        self.calculated.Keyboard.release("b")
        self.calculated.img_click("check1.jpg",(0,0,1300,950),overtime=2)
