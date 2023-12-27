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
        self.task_flag = False
        self.universe_flag = False
        # 模拟宇宙启动参数
        self.universe_bonus = 0
        self.universe_nums = 0
        self.u = None

    def allfunction(self):
        """
            说明：多功能执行
        """
        if self.dungeon_flag:
            self.dungeon.start()
        if self.map_flag:
            self.map.start()
        if self.universe_flag:
            self.Universe()

    def Universe(self):
        """
            说明：模拟宇宙执行
        """
        # 进入模拟宇宙页面
        log.info("模拟宇宙运行中")
        self.dungeon.open_dungeon()
        self.dungeon.calculated.dungeon_img_click("universe.jpg")
        # 启动模拟宇宙
        command = ["python","states.py",f"--bonus={self.universe_bonus}",f"--nums={self.universe_nums}"]
        self.u = subprocess.Popen(command,text=True,cwd="./Auto_Simulated_Universe-main")

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
