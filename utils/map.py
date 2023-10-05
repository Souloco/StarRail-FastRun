import win32gui
import time
from .config import read_json_info
from .calculated import Calculated
from .log import log
from pynput import mouse
from pyautogui import drag
class Map:
    def __init__(self):
        self.calculated = Calculated()
        self.team_change = False
        self.teamid = 1
        self.id = 1
        self.commission = False
        self.close_game = False
        self.nums = 0

    def Enter_map_start(self,mapjson):
        """
        说明:
            执行mapjson的start列表
        参数:
            mapjson:路线json名
        """
        start_list = read_json_info(mapjson,"start",prepath="map")
        map_name_dir = mapjson[0:mapjson.index("_",5)] + ".jpg"
        map_name = read_json_info(mapjson,"name",prepath="map").split("-")[0]
        planet_id = int(mapjson[mapjson.index('_') + 1:mapjson.index('-')])
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
                        log.info("进入星球")
                        for i in range(3):
                            if self.calculated.img_check("planet_navigation.jpg",(40,40,100,100),2):
                                break
                            else:
                                self.calculated.img_click("Enter_planet.jpg",(1440,115,1870,160))
                        planet_img = "orientation_{planet_id}.png".format(planet_id=planet_id)
                        for i in range(3):
                            if self.calculated.img_check("map_navigation.jpg",(40,40,100,100),2):
                                break
                            else:
                                self.calculated.img_click(planet_img)
                        # 进入地名
                        log.info("进入地名")
                        # 滚动寻找
                        # 向下滚动寻找
                        for i in range(5):
                            if not self.calculated.img_check(map_name_dir,(1420,180,1890,1020),1):
                                self.calculated.Mouse.position = self.calculated.mouse_pos((1750,250))
                                self.calculated.Mouse.scroll(0,-200)
                            else:
                                break
                        # 向上滚动寻找
                        for i in range(5):
                            if not self.calculated.img_check(map_name_dir,(1420,180,1890,1020),1):
                                self.calculated.Mouse.position = self.calculated.mouse_pos((1750,250))
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
                        self.calculated.ocr_click(value+"层",(0,700,125,1010),1)
                elif "point" in key:
                    log.info("寻找传送点")
                    # 向下滚动寻找
                    for i in range(5):
                        if not self.calculated.img_check(key,(0,0,0,0),1):
                            self.calculated.Mouse.position = self.calculated.mouse_pos((1330,440))
                            drag(0,-400, 1,button='left')
                        else:
                            break
                    # 向上滚动寻找
                    for i in range(5):
                        if not self.calculated.img_check(key,(0,0,0,0),1):
                            self.calculated.Mouse.position = self.calculated.mouse_pos((1330,640))
                            drag(0,400, 1,button='left')
                        else:
                            break
                    self.calculated.img_click(key,(0,0,0,0),overtime=value)
                elif key == "transfer":
                    log.info("进行传送")
                    self.calculated.img_click("transfer.jpg",(1470,945,1840,1000),overtime=value)
                    self.calculated.check_main_interface()
                else:
                    self.calculated.img_click(key,(0,0,0,0),overtime=value)

    def Enter_map_fighting(self,mapjson):
        """
        说明:
            执行mapjson的map列表
        参数:
            mapjson:路线json名
        """
        map_name = mapjson[0:mapjson.index(".")]
        operate_list = read_json_info(mapjson,"map",prepath="map")
        for operate in operate_list:
            for key,value in operate.items():
                if key in ["w","s","a","d"]:
                    self.calculated.move(key,value)
                elif key == "fighting":
                    self.calculated.fighting(value)
                elif key == "mouse_move":
                    self.calculated.mouse_move(value)
                elif key == "f":
                    self.calculated.interaction(value)
                elif key == "delay":
                    time.sleep(value)
            logtime = time.strftime("%m-%d-%H-%M-%S",time.localtime())
            self.calculated.save_screenshot(f"{map_name}-{logtime}")

    def Enter_map_onejson(self,mapjson):
        """
        说明:
            执行单个mapjson
        参数:
            mapjson:路线json名
        """
        map_name = read_json_info(mapjson,"name",prepath="map")
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
        self.calculated.img_click("map_init_2.jpg",(600,970,660,1000))
        while not self.calculated.img_check("map_init_1.jpg",(660,970,695,1000),2):
            self.calculated.Mouse.press(mouse.Button.left)
            time.sleep(2)
            self.calculated.Mouse.release(mouse.Button.left)
        self.calculated.Keyboard.press("m")
        self.calculated.Keyboard.release("m")
        time.sleep(1)

    def start(self,map_list,auto_map_list):
        log.info("游戏初始化设置")
        self.calculated.set_windowsize()
        if self.commission:
            log.info("清委托")
            self.calculated.commission()
        if self.team_change:
            log.info("锄大地---切换队伍")
            self.calculated.change_team(self.teamid,self.id)
        log.info("锄大地---地图初始化")
        self.map_init()
        log.info("锄大地---必跑路线")
        self.Enter_map_jsonlist(map_list)
        log.info("锄大地---重跑路线")
        for i in range(self.nums):
            self.Enter_map_jsonlist(auto_map_list)
        if self.close_game:
            log.info("锄大地---自动关机")
            self.calculated.close_game()
        log.info("锄大地---执行完毕")

    def check_map(self):
        log.info("锄大地---打开背包")
        self.calculated.Keyboard.press('b')
        self.calculated.Keyboard.release("b")
        self.calculated.img_click("check1.jpg",(0,0,1300,950),overtime=2)
