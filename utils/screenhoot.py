import numpy as np
import win32gui
import win32ui
import win32con
import cv2
class Screenhoot():
    def __init__(self):
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        self.hwndDC = win32gui.GetWindowDC(0)
        # 根据窗口的DC获取mfcDC
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        # mfcDC创建可兼容的DC
        self.saveDC = self.mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        self.saveBitMap = win32ui.CreateBitmap()
        # 截取窗口大小
        self.width = 1920
        self.height = 1080
        # 为bitmap开辟空间
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC,self.width, self.height)
        # 将截图保存到saveBitmap中
        self.saveDC.SelectObject(self.saveBitMap)

    def grab(self,x,y):
        self.saveDC.BitBlt((0, 0), (self.width, self.height), self.mfcDC, (x,y), win32con.SRCCOPY)
        # self.saveBitMap.SaveBitmapFile(self.saveDC,"")
        img_buf = self.saveBitMap.GetBitmapBits(True)
        return np.frombuffer(img_buf, dtype="uint8").reshape(self.height,self.width,4)[:,:,:3]

    def __del__(self):
        # 释放内存
        self.mfcDC.DeleteDC()
        win32gui.DeleteObject(self.saveBitMap.GetHandle())