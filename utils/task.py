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
        while not self.calculated.img_check("exit1.png",(1800,950,1920,1080),overtime=1) and time.time() - starttime < maxtime:
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

    def commission(self):
        """
        说明:
            委托功能
        """
        log.info("清委托")
        starttime = time.time()
        maxtime = 100
        self.open_esc()
        self.calculated.ocr_click(text='委托',points=(1700,400,1755,425))
        while self.calculated.ocr_check(text='委托',points=(100,0,170,70),overtime=2) and self.calculated.img_click('red_notice.jpg',overtime=5,rates=0.80) and time.time() - starttime < maxtime:
            if self.calculated.ocr_click(text='领取',points=(1460,880,1520,920),overtime=2):
                self.calculated.ocr_click(text='再次派遣',points=(1170,930,1300,960),overtime=2,mode=2)
        self.close_esc()

    def daily_task(self):
        """
        说明:
            每日实训功能
        """
        log.info("完成每日实训")

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
