from win32 import win32api,win32gui
from PIL import ImageGrab
import time
import cv2 as cv
import numpy as np
from .config import read_picture,model_dir
from .log import log
from cnocr import CnOcr
import os
import ctypes
from pynput import mouse, keyboard
from pynput.keyboard import Key
class Calculated:
    def __init__(self):
        # 获取窗口句柄
        self.hwnd = win32gui.FindWindow("UnityWndClass","崩坏：星穹铁道")
        # 边框
        self.left_border = int(8)
        self.up_border = int(31)
        # 缩放比例
        self.scale = ctypes.windll.user32.GetDpiForSystem() / 96.0
        self.borderless = False
        # OCR识别
        self.reader = CnOcr(det_model_name="ch_PP-OCRv3_det", rec_model_name="densenet_lite_136-fc",det_root=os.path.join(model_dir, "cnocr"), rec_root=os.path.join(model_dir, "cnstr"))
        # 键鼠控制
        self.Mouse = mouse.Controller()
        self.Keyboard = keyboard.Controller()
        # 列表比较
        self.compare_lists = lambda a, b: all(x <= y for x, y in zip(a, b))
        # 图片logs是否记录
        self.img_log_value = False

    def get_hwnd(self):
        self.hwnd = win32gui.FindWindow("UnityWndClass","崩坏：星穹铁道")

    def active_window(self):
        win32gui.SetForegroundWindow(self.hwnd)

    def set_windowsize(self):
        """
        说明:
            设置窗口化或者全屏幕参数让截图区域正确
        """
        rect = win32gui.GetWindowRect(self.hwnd)
        w = rect[2]-rect[0]
        h = rect[3]-rect[1]
        self.borderless = True if w == 1920 and h == 1080 else False
        self.left_border = int((w-1920)/2)
        self.up_border = (h-1080)-self.left_border
        log.info(f"游戏分辨率:{w}x{h}x{self.scale}---{self.borderless}".replace("True","全屏幕").replace("False","窗口"))

    def get_WindowRect(self,hwnd):
        """
        说明:
            返回准确的窗口信息
        参数:
            hwnd: 窗口句柄
        """
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if not self.borderless:
            left, top, right, bottom = left+self.left_border,top+self.up_border,right-self.left_border,bottom-self.left_border
        return (left, top, right, bottom)

    def take_screenshot(self,points=(0,0,0,0)):
        """
        说明:
            返回RGB图像
        参数:
            points: 图像截取范围
        """
        left, top, right, bottom = self.get_WindowRect(self.hwnd)
        screenshot = ImageGrab.grab((left, top, right, bottom))
        if points != (0,0,0,0):
            screenshot = screenshot.crop(points)
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
        return screenshot

    def save_screenshot(self,name:str):
        """
        说明:
            保存截图名字为name至log/image
        参数"
            name: 文件名字
        """
        if self.img_log_value:
            left, top, right, bottom = self.get_WindowRect(self.hwnd)
            screenshot = ImageGrab.grab((left, top, right, bottom))
            screenshot.save(f"./logs/image/{name}.jpg")

    def img_match(self,img,templeimg):
        """
        说明:
            返回最佳匹配系数与最佳匹配位置
        参数:
            img:原始图像
            templeimg:模板图像
        """
        res = cv.matchTemplate(img,templeimg,cv.TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc = cv.minMaxLoc(res)
        return max_val,max_loc

    def img_click(self,templepath,points=(0,0,0,0),overtime=5.0,rates=0.90):
        """
        说明:
            识别到图片并点击,否则不点击
        参数:
            templepath:模板图像路径
            points:截图区域
            overtime:识别时间
            rates:对比度要求
        """
        templeimg = read_picture(templepath)
        img = self.take_screenshot(points)
        val,loc = self.img_match(img,templeimg)
        start_time = time.time()
        while val < rates and time.time() - start_time < overtime:
            img = self.take_screenshot(points)
            val,loc = self.img_match(img,templeimg)
            time.sleep(0.05)
        log.info(f"图片点击-{val}")
        if val >= rates:
            w = templeimg.shape[1]
            h = templeimg.shape[0]
            left, top, right, bottom = self.get_WindowRect(self.hwnd)
            x = left + points[0] + loc[0] + int(w/2)
            y = top + points[1]+loc[1] + int(h/2)
            self.Mouse.position = (x,y)
            time.sleep(0.1)
            self.Mouse.press(mouse.Button.left)
            time.sleep(0.5)
            self.Mouse.release(mouse.Button.left)
            return True
        else:
            log.info("识别超时")
            return False

    def img_check(self,templepath,points=(0,0,0,0),overtime=5.0,rates=0.90):
        """
        说明:
            识别图片返回布尔值
        参数:
            templepath:模板图像路径
            points:截图区域
            overtime:识别时间
            rates:对比度要求
        """
        templeimg = read_picture(templepath)
        img = self.take_screenshot(points)
        val,loc = self.img_match(img,templeimg)
        start_time = time.time()
        while val < rates and time.time() - start_time < overtime:
            img = self.take_screenshot(points)
            val,loc = self.img_match(img,templeimg)
            time.sleep(0.05)
        # log.info(f"图片检测-{val}")
        if val >= rates:
            return True
        else:
            return False

    def dungeon_img_click(self,templepath,points=(0,0,0,0),overtime=5.0,rates=0.90):
        """
        说明:
            识别图片返回布尔值
        参数:
            templepath:模板图像路径
            points:截图区域
            overtime:识别时间
            rates:对比度要求
        """
        templeimg = read_picture(templepath)
        img = self.take_screenshot(points)
        val,loc = self.img_match(img,templeimg)
        start_time = time.time()
        while val < rates and time.time() - start_time < overtime:
            img = self.take_screenshot(points)
            val,loc = self.img_match(img,templeimg)
            time.sleep(0.05)
        log.info(f"图片点击-{val}")
        if val >= rates:
            h = templeimg.shape[0]
            print((0,loc[1],1920,loc[1]+h))
            self.img_click("dungeon_transfer.jpg",points=(0,loc[1],1920,loc[1]+h))
        else:
            log.info("识别超时")

    def ocr_match(self,img,text:str,mode=1):
        """
        说明:
            返回匹配位置与匹配系数
        参数:
            img:图像
            text:匹配文本
            mode:匹配模式
        """
        result = self.reader.ocr(img)
        nums = len(text)
        ocr_num = 0
        # print(result)
        for res in result:
            loc = res['position']
            content = str(res['text']).replace(" ", "")
            rate = res['score']
            # 完全匹配
            if mode == 1:
                if text == content:
                    x = int((loc[0][0]+loc[1][0]+loc[2][0]+loc[3][0])/4)
                    y = int((loc[0][1]+loc[1][1]+loc[2][1]+loc[3][1])/4)
                    return (x,y),rate
            # 部分匹配/误差字数为1
            if mode == 2:
                for t in text:
                    if t in content[ocr_num:]:
                        ocr_num = ocr_num + 1
                if ocr_num >= nums - 1:
                    x = int((loc[0][0]+loc[1][0]+loc[2][0]+loc[3][0])/4)
                    y = int((loc[0][1]+loc[1][1]+loc[2][1]+loc[3][1])/4)
                    return (x,y),rate
        return (0,0),0

    def ocr_click(self,text:str,points=(0,0,0,0),overtime=5.0,rates=0.1,mode=1):
        """
        说明:
            识别到文本点击，否则不点击
        参数:
            text:需要检测的文本内容
            points:截图区域
            overtime:识别时间
            rates:对比度要求
            mode:匹配模式
        """
        img = self.take_screenshot(points)
        pos,rate = self.ocr_match(img,text,mode)
        start_time = time.time()
        while rate < rates and time.time() - start_time < overtime:
            img = self.take_screenshot(points)
            pos,rate = self.ocr_match(img,text,mode)
            time.sleep(0.05)
        if rate >= rates:
            log.info(f"OCR点击-{rate}")
            left, top, right, bottom = self.get_WindowRect(self.hwnd)
            x = left + points[0] + pos[0]
            y = top + points[1] + pos[1]
            self.Mouse.position = (x,y)
            time.sleep(0.1)
            self.Mouse.press(mouse.Button.left)
            time.sleep(0.5)
            self.Mouse.release(mouse.Button.left)
            return True
        else:
            log.warning(f"OCR点击失败-{rate}")
            return False

    def ocr_check(self,text:str,points=(0,0,0,0),overtime=5.0,rates=0.1,mode=1):
        """
        说明:
            识别文本返回布尔值
        参数:
            text:需要检测的文本内容
            points:截图区域
            overtime:识别时间
            rates:对比度要求
            mode:匹配模式
        """
        img = self.take_screenshot(points)
        pos,rate = self.ocr_match(img,text,mode)
        start_time = time.time()
        while rate < rates and time.time() - start_time < overtime:
            img = self.take_screenshot(points)
            pos,rate = self.ocr_match(img,text,mode)
            time.sleep(0.05)
        if rate >= rates:
            log.info(f"OCR检测-{rate}")
            return True
        else:
            log.warning(f"OCR检测-{rate}")
            return False

    def mouse_pos(self,points):
        """
        说明:
            返回实际鼠标坐标
        参数:
            points:相对游戏坐标
        """
        left, top, right, bottom = self.get_WindowRect(self.hwnd)
        x = left + points[0]
        y = top + points[1]
        return (x,y)

    def move(self,key:str = ["w","a","s","d"],times=1.0):
        """
        说明:
            移动
        参数:
            key:方位按键
            times:执行时间
        """
        log.info(f"执行{key}---{times}")
        self.Keyboard.press(Key.shift_l)
        self.Keyboard.press(key)
        start_time = time.perf_counter()
        while time.perf_counter() - start_time < times:
            pass
        self.Keyboard.release(key)
        self.Keyboard.release(Key.shift_l)

    def mouse_move(self,value:int):
        win32api.mouse_event(1,int(value*self.scale),0)
        time.sleep(0.5)

    def has_red(self, points=(0,0,0,0)):
        """
        说明:
            判断游戏指定位置是否有红色
        参数:
            points: 图像截取范围
        """
        img = self.take_screenshot(points)
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv.inRange(hsv_img, lower_red, upper_red)
        mask2 = cv.inRange(hsv_img, lower_red2, upper_red2)
        mask = cv.bitwise_or(mask1, mask2)
        # 统计掩膜中的像素数目
        red_pixel_count = cv.countNonZero(mask)
        print(red_pixel_count)
        return red_pixel_count > 50

    def get_whiteimg(self,img):
        """
        说明:
            对白色做提取处理,返回RGB图像
        参数:
            img:提供的原始图片
        """
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # 设置白色提取范围
        lower_white = np.array([0,0,70])
        upper_white = np.array([180,43,255])

        mask = cv.inRange(hsv_img,lower_white,upper_white)
        # 维度扩充并归一化
        mask = cv.merge([mask,mask,mask])
        return mask

    def get_pix_hsv(self,points=(0,0)):
        """
        说明:
            返回hsv像素值
        参数:
            points:相对游戏坐标
        """
        img = self.take_screenshot()
        hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)
        x = points[0]
        y = points[1]
        h = hsv[y,x,0]
        s = hsv[y,x,1]
        v = hsv[y,x,2]
        return [h,s,v]

    def fighting(self,mode=1):
        if mode == 1:   # 打怪
            log.info("打怪")
            self.Mouse.click(mouse.Button.left)
            time.sleep(1)
            if self.img_check("finish_fighting.jpg",(1735,1025,1920,1080),2):
                if self.has_red((50,68,230,245)):
                    self.wait_fight_end()
                    return True
            else:
                self.wait_fight_end()
                return True
        else:   # 打障碍物
            self.Mouse.click(mouse.Button.left)
            time.sleep(0.7)
            return True

    def wait_main_interface(self):
        start_time = time.time()    # 开始计算等待时间
        while True:
            if self.img_click("fighting_lost.jpg",(700,140,1200,400),2):
                log.info("战斗失败")
                break
            if self.img_check("finish_fighting.jpg",(1735,1025,1920,1080),2):
                break
            time.sleep(3)
            if time.time() - start_time > 600:
                return False
        time.sleep(2)   # 等待人物模型出现
        return True

    def check_main_interface(self):
        log.info("强制在主界面")
        if self.img_check("finish_fighting.jpg",(1735,1025,1920,1080),10):
            time.sleep(2)   # 等待人物模型出现
        else:
            while not self.img_check("finish_fighting.jpg",(1735,1025,1920,1080),1):
                self.Keyboard.press(Key.esc)
                time.sleep(0.05)
                self.Keyboard.release(Key.esc)
                time.sleep(1)
        return True

    def wait_fight_end(self):
        """
        说明:
            等待战斗结束
        """
        log.info("等待战斗结束")
        time.sleep(7)   # 缓冲
        self.wait_main_interface()

    def interaction(self,mode=1):
        """
        说明:
            等待传送结束
        """
        log.info("执行交互---传送")
        time.sleep(0.5)
        self.Keyboard.press("f")
        time.sleep(0.05)
        self.Keyboard.release("f")
        time.sleep(2)   # 缓冲
        self.wait_main_interface()

    def open_map(self):
        """
        说明:
            打开地图
        """
        log.info("进入地图")
        while not self.img_check("map_navigation.jpg",(40,40,100,100),2):
            self.Keyboard.press("m")
            time.sleep(0.05)
            self.Keyboard.release("m")

    def release_mouse_keyboard(self):
        """
        说明:
            释放键鼠操作
        """
        self.Mouse.release(mouse.Button.left)
        for key in ["w","a","s","d","f",Key.esc,Key.alt_l]:
            self.Keyboard.release(key)
        return True

    def close_game(self):
        """
        说明:
            自动关机
        """
        # 关闭游戏
        self.Keyboard.press(Key.esc)
        time.sleep(0.05)
        self.Keyboard.release(Key.esc)
        self.img_click("exit1.png")
        self.img_click("sure.jpg")
        self.img_click("exit2.png",overtime=60)
        self.img_click("sure2.png",overtime=10)
        # 关机
        time.sleep(5)
        os.system('shutdown /s /t 60')
        # 关闭程序
        self.Keyboard.press(Key.f8)
        time.sleep(0.05)
        self.Keyboard.release(Key.f8)
        return True

    def change_team(self,teamid:int,id:int):
        """
        说明:
            切换队伍
        """
        log.info("切换队伍")
        self.Keyboard.press('t')
        time.sleep(0.5)
        self.Keyboard.release('t')
        time.sleep(1)   # 缓冲
        teamid = '0' + str(teamid)
        self.ocr_click(text=teamid,points=(550,0,1300,130))
        self.img_click("team_sure.png",points=(1500,950,1920,1080),overtime=2)
        time.sleep(2)   # 缓冲
        self.Keyboard.press(Key.esc)
        time.sleep(0.05)
        self.Keyboard.release(Key.esc)
        self.check_main_interface()
        if id >= 1 and id <= 4:
            id = str(id)
            self.Keyboard.press(id)
            time.sleep(0.05)
            self.Keyboard.release(id)

    def commission(self):
        """
        说明:
            委托功能
        """
        log.info("清委托")
        self.Keyboard.press(Key.esc)
        time.sleep(0.05)
        self.Keyboard.release(Key.esc)
        self.ocr_click(text='委托',points=(1700,400,1755,425))
        while self.img_click('red_notice.jpg',overtime=5,rates=0.80):
            if self.ocr_click(text='领取',points=(1460,880,1520,920),overtime=2):
                self.ocr_click(text='再次派遣',points=(1170,930,1300,960),overtime=2,mode=2)
        while not self.img_check("finish_fighting.jpg",(1735,1025,1920,1080),1):
            self.Keyboard.press(Key.esc)
            time.sleep(0.05)
            self.Keyboard.release(Key.esc)

    def login(self):
        """
        说明:
            登录功能
        """
        log.info("登录界面")
        while not self.img_check("finish_fighting.jpg",(1735,1025,1920,1080),1):
            self.Mouse.position = self.mouse_pos((950,900))
            self.Mouse.click(mouse.Button.left)
            time.sleep(1)
