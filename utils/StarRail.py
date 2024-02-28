from .calculated import Calculated
from .dungeon import Dungeon
from .map import Map
from .task import Task
from .log import log
import threading
import ctypes
import inspect
import subprocess
import os
class StarRail:
    def __init__(self,base:Calculated = Calculated()):
        self.calculated = base
        self.dungeon = Dungeon(base)
        self.map = Map(base)
        self.task = Task(base)
        self.thread = threading.Thread()
        # 启动功能参数
        self.mode = 0
        # 多功能执行配置
        self.map_flag = False
        self.dungeon_flag = False
        self.universe_flag = False
        # 模拟宇宙启动参数
        self.universe_bonus = 0
        self.universe_nums = 0
        self.u = None
        # 模拟宇宙奖励配置
        self.universe_reward_flag = False
        # 关闭游戏参数
        self.close_game = 0

    def allfunction(self):
        """
            说明：多功能执行
        """
        # 游戏初始化设置
        self.calculated.set_windowsize()
        # 清委托执行
        if self.task.commission_flag:
            self.task.commission()
        # 领取支援奖励执行
        if self.task.supportrewards_flag:
            self.task.support_rewards()
        # 清体力执行
        if self.dungeon_flag:
            self.dungeon.start()
        # 锄大地执行
        if self.map_flag:
            self.map.start()
        # 模拟宇宙执行
        if self.universe_flag:
            self.Universe()
        # 每日实训执行
        if self.task.dailytask_flag:
            self.task.daily_task()
        # 无名勋礼执行
        if self.task.rewards_flag:
            self.task.rewards()
        # 关闭模式执行
        self.calculated.close_game(self.close_game)

    def enter_universe(self):
        """
            说明：进入模拟宇宙页面
        """
        # 进入模拟宇宙页面
        log.info("进入模拟宇宙页面")
        self.dungeon.open_dungeon()
        self.dungeon.calculated.dungeon_img_click("universe.jpg")
        if self.calculated.ocr_check(text="扩展装置",points=(90,40,200,100)):
            self.calculated.img_click("universe_change.jpg")

    def universe_rewards(self):
        """
            说明：领取模拟宇宙奖励
        """
        log.info("领取模拟宇宙奖励")

    def Universe(self):
        """
            说明：模拟宇宙执行
        """
        log.info("模拟宇宙运行中")
        # 进入模拟宇宙页面
        self.enter_universe()
        # 模拟宇宙奖励领取
        if self.universe_reward_flag:
            self.universe_rewards()
        # 启动模拟宇宙
        command = ["python","states.py",f"--bonus={self.universe_bonus}",f"--nums={self.universe_nums}"]
        self.u = subprocess.Popen(command,text=True,cwd="./Auto_Simulated_Universe-main")
        self.u.wait()

    def start(self):
        # 获取窗口句柄
        self.calculated.get_hwnd()
        if self.calculated.hwnd == 0:
            log.warning("未检测到游戏运行,请启动游戏")
        # 激活窗口
        self.calculated.active_window()
        # 启动功能
        if not self.thread.is_alive():
            if self.mode == 1:
                self.thread = threading.Thread(name='chudi',target=self.map.start,daemon=True)
            elif self.mode == 2:
                self.thread = threading.Thread(name='dungeon',target=self.dungeon.start,daemon=True)
            elif self.mode == 3:
                self.thread = threading.Thread(name='allfunction',target=self.allfunction,daemon=True)
            if self.mode == 4:
                self.Universe()
            elif self.mode != 0:
                self.thread.start()
            else:
                log.warning("线程配置参数错误")
        else:
            log.warning("功能线程还在运行")

    def stop(self):
        """
            说明：关闭功能线程|进程
        """
        log.info("停止")
        if self.u is not None:
            self.u.kill()
        if self.thread.is_alive():
            self.stop_thread(self.thread)
        self.calculated.release_mouse_keyboard()

    def stop_thread(self,thread:threading.Thread):
        """
            说明：立即关闭线程
        """
        def _async_raise(tid, exctype):
            """raises the exception, performs cleanup if needed"""
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                # """if it returns a number greater than one, you're in trouble,
                # and you should call it again with exc=NULL to revert the effect"""
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
        if thread.is_alive():
            _async_raise(thread.ident,SystemExit)
