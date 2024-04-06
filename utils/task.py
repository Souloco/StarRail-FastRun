from .calculated import Calculated
from .log import log
import time
from pynput.keyboard import Key
class Task:
    def __init__(self,base:Calculated = Calculated()):
        self.calculated = base
        # 任务配置启用
        self.commission_flag = False
        self.dailytask_flag = False
        self.supportrewards_flag = False
        self.rewards_flag = False

    def open_esc(self):
        """
        说明:
            打开ESC界面/手机界面
        """
        starttime = time.time()
        maxtime = 10
        while not self.calculated.ocr_check(text='委托',points=(1700,395,1755,430),overtime=1) and time.time() - starttime < maxtime:
            self.calculated.Keyboard.press(Key.esc)
            time.sleep(0.05)
            self.calculated.Keyboard.release(Key.esc)

    def close_esc(self):
        """
        说明:
            关闭ESC界面/手机界面
        """
        starttime = time.time()
        maxtime = 20
        while not self.calculated.img_check("liaotian.png",(20,900,80,970),1) and time.time() - starttime < maxtime:
            self.calculated.Keyboard.press(Key.esc)
            time.sleep(0.05)
            self.calculated.Keyboard.release(Key.esc)
        time.sleep(2)   # 等待人物模型出现

    def commission(self):
        """
        说明:
            委托功能
        """
        log.info("清委托")
        starttime = time.time()
        maxtime = 100
        self.open_esc()
        self.calculated.ocr_click(text='委托',points=(1700,395,1755,430))
        while self.calculated.ocr_check(text='委托',points=(100,0,170,70),overtime=2) and self.calculated.img_check('red_notice.jpg',overtime=5,rates=0.80) and time.time() - starttime < maxtime:
            if self.calculated.ocr_click(text='一键领取',points=(430,880,560,920),overtime=2):
                self.calculated.ocr_click(text='再次派遣',points=(1170,930,1300,960),overtime=2,mode=2)
        self.close_esc()

    def daily_task(self):
        """
        说明:
            每日实训功能
        """
        log.info("完成每日实训")
        starttime = time.time()
        maxtime = 100
        self.calculated.Keyboard.press(Key.f4)
        time.sleep(0.05)
        self.calculated.Keyboard.release(Key.f4)
        while self.calculated.ocr_click(text='领取',points=(280,800,1600,880),overtime=2) and time.time() - starttime < maxtime:
            time.sleep(0.5)
        while self.calculated.img_click('dailytask.jpg',overtime=2) and time.time() - starttime < maxtime:
            time.sleep(0.5)
            self.calculated.mouse_click()
        self.close_esc()

    def support_rewards(self):
        """
        说明:
            支援奖励功能
        """
        log.info("领取支援奖励")
        starttime = time.time()
        maxtime = 100
        self.open_esc()
        if self.calculated.img_click('red_notice.jpg',overtime=3,points=(1700,40,1800,100),rates=0.80):
            if self.calculated.ocr_click(text='漫游签证',points=(1450,100,1700,170),overtime=2,mode=2):
                self.calculated.img_click('support_gift.jpg',overtime=3,rates=0.90)
        self.close_esc()

    def rewards(self):
        """
        说明:
            无名勋礼功能
        """
        log.info("完成无名勋礼")
        self.calculated.Keyboard.press(Key.f2)
        time.sleep(0.05)
        self.calculated.Keyboard.release(Key.f2)
        time.sleep(1)
        if self.calculated.img_click('red_notice.jpg',overtime=3,rates=0.80):
            self.calculated.ocr_click(text='领取',points=(1330,880,1750,940),overtime=2,mode=2)
        self.close_esc()

    def make_skillfood(self):
        log.info("合成奇巧零食")
        self.open_esc()
        starttime = time.time()
        maxtime = 15
        self.calculated.ocr_click(text='合成',points=(1575,525,1625,565))
        while not self.calculated.ocr_check(text='奇巧零食',points=(1020,160,1175,210),overtime=1.5) and time.time() - starttime < maxtime:
            self.calculated.img_click('food3.jpg')
        if self.calculated.ocr_check(text='奇巧零食',points=(1020,160,1175,210),overtime=1.5):
            self.calculated.Mouse.position = self.calculated.mouse_pos((1435,870))
            self.calculated.mouse_click()
            if self.calculated.ocr_click(text='合成',points=(1150,965,1210,1000)):
                self.calculated.img_click("sure.jpg")
                time.sleep(0.5)
        self.close_esc()
