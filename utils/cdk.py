from .calculated import Calculated
from .log import log
import win32clipboard
from pynput.keyboard import Key
import time
class CDK:
    def __init__(self):
        self.calculated = Calculated()

    def writeToClipBoard(self,text):
        """
        说明：
            写入剪切板
        参数：
            text：写入的文本
        """
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()

    def Enter_cdk(self):
        """
        说明：
            进入兑换码页面
        """
        self.calculated.Keyboard.press(Key.esc)
        time.sleep(0.05)
        self.calculated.Keyboard.release(Key.esc)
        self.calculated.img_click("cdk_1.jpg",(1710,70,1800,120))
        self.calculated.img_click("cdk_2.jpg",(1410,180,1800,260))

    def cdk(self,text,times):
        if times <= 3:
            log.info(f"兑换中---{text}---第{times}次")
            self.writeToClipBoard(text)
            self.calculated.img_click("cdk_clear.jpg",(400,320,1525,755),1)
            self.calculated.img_click("cdk_copy.jpg",(400,320,1525,755))
            self.calculated.img_click("sure.jpg",(400,320,1525,755))
            if self.calculated.img_check("cdk_yes.jpg",(400,320,1525,755),2):
                self.calculated.img_click("sure.jpg",(400,320,1525,755))
                log.info(f"兑换中---{text}---兑换成功")
            else:
                log.info(f"兑换中---{text}---兑换失败")
                time.sleep(5)
                self.cdk(text,times+1)

    def cdk_all(self,cdk_list):
        log.info("兑换开始")
        self.Enter_cdk()
        for cdk in cdk_list:
            self.cdk(cdk,1)
        log.info("兑换结束")
        return True
