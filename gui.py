import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from utils.config import read_map,read_maplist_name,set_config,get_config,save_dungeon_info,read_json_info
from utils.map import Map
from utils.dungeon import Dungeon
from utils.cdk import CDK
import os
import logging
from utils.log import log
from pynput import keyboard
import pyuac
import requests
import time
import win32console
import win32gui
# 全局属性
# 标题
TITLE_NAME = 'StarRail-FastRun'
# 版本号
VER = get_config("version")
# 版本更新提示
ver_update = False
# 用于日志文本框
class TextboxHandler(logging.Handler):
    def __init__(self, textbox:tk.Text):
        logging.Handler.__init__(self)
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.insert("end", msg + "\n")
# 事件
# 进入锄大地页面
def Enter_frame2():
    mainframe.pack_forget()
    hoe_frame.pack()
    root.update()
# 进入主页面
def Enter_mainframe():
    logframe.pack_forget()
    announce_frame.pack_forget()
    allframe.pack_forget()
    hoe_frame.pack_forget()
    dungeonframe.pack_forget()
    mainframe.pack()
    root.update()

# 打包地图列表
def get_map_list(map_value_list):
    map_use_list = []
    for i in range(len(map_value_list)):
        value = map_value_list[i].get()
        if value == 1:
            map_use_list.append(map_list[i])
    return map_use_list
# 保存
def save_config():
    map_use_list = get_map_list(map_value_list)
    auto_map_use_list = get_map_list(auto_map_value_list)
    set_config("map_list_data",map_use_list)
    set_config("auto_map_list_data",auto_map_use_list)
    set_config("team_id",teamid_sets.get())
    set_config("character_id",id_sets.get())
    set_config("team_change",team_change_var.get())
    set_config("img_log",img_log_Var.get())
    set_config("close_game",close_game_var.get())
    set_config("auto_map_nums",auto_map_nums.get())
    set_config("commission",commission_var.get())
# 进入日志页面
def Enter_logframe():
    hoe_frame.pack_forget()
    logframe.pack()
    root.update()
# 进入兑换码页面
def Enter_cdkframe():
    mainframe.pack_forget()
    cdkframe.pack()
    root.update()
# 进入清体力页面
def Enter_dungeonframe():
    mainframe.pack_forget()
    dungeonframe.pack()
    root.update()
# 进入多功能合一执行页面
def Enter_allframe():
    mainframe.pack_forget()
    allframe.pack()
    root.update()
# 锄地线程
def Enter_map():
    map_use_list = get_map_list(map_value_list)
    auto_map_use_list = get_map_list(auto_map_value_list)
    auto_map.calculated.get_hwnd()
    if auto_map.calculated.hwnd == 0:
        log.warning("未检测到游戏运行,请启动游戏")
    else:
        auto_map.calculated.img_log_value = img_log_Var.get()   # 是否启用截图记录
        auto_map.calculated.set_windowsize()
        auto_map.calculated.active_window()
        if commission_var.get():
            auto_map.calculated.commission()
        if team_change_var.get():
            auto_map.calculated.change_team(teamid=teamid_sets.get(),id=id_sets.get())
        auto_map.map_init()
        t = threading.Thread(name='chudi',target=auto_map.Enter_map_all,args=(map_use_list,auto_map_use_list,close_game_var.get(),auto_map_nums.get()))
        t.daemon = True
        t.start()
# cdk线程
def Enter_cdk():
    count = int(cdktext.index('end').split('.')[0])
    auto_cdk = CDK()
    cdk_list = []
    for i in range(1,count):
        contect = cdktext.get(str(i)+".0",str(i)+".end")
        cdk_list.append(contect)
    auto_cdk.calculated.set_windowsize()
    auto_cdk.calculated.active_window()
    t = threading.Thread(name='cdk',target=auto_cdk.cdk_all,args=(cdk_list,))
    t.daemon = True
    t.start()
# 副本线程
def enter_dungeon_all():
    auto_dungeon.calculated.get_hwnd()
    if auto_dungeon.calculated.hwnd == 0:
        log.warning("未检测到游戏运行,请启动游戏")
    else:
        auto_dungeon.calculated.active_window()
        auto_dungeon.calculated.set_windowsize()
        id = dungeon_notebook.index("current")
        t = threading.Thread(name='dungeon',target=auto_dungeon.enter_dungeon_list,args=(dungeon_config_list[id],))
        t.daemon = True
        t.start()

# 多功能执行
def enter_function():
    # 清体力执行
    auto_dungeon.calculated.active_window()
    auto_dungeon.calculated.set_windowsize()
    id = dungeon_notebook.index("current")
    auto_dungeon.enter_dungeon_list(dungeon_config_list[id])
    # 锄地执行
    map_use_list = get_map_list(map_value_list)
    auto_map_use_list = get_map_list(auto_map_value_list)
    auto_map.calculated.img_log_value = img_log_Var.get()   # 是否启用截图记录
    auto_map.calculated.set_windowsize()
    auto_map.calculated.active_window()
    auto_map.map_init()
    auto_map.Enter_map_all(map_use_list,auto_map_use_list,close_game_var.get(),auto_map_nums.get())
# 多功能执行线程
def enter_function_all():
    auto_map.calculated.get_hwnd()
    if auto_map.calculated.hwnd == 0:
        log.warning("未检测到游戏运行,请启动游戏")
    else:
        t = threading.Thread(name='allfunction',target=enter_function)
        t.daemon = True
        t.start()
# 添加副本配置项
def add_dungeon_config():
    id = dungeon_notebook.index("current")
    dungeon_config_list[id].append({dungeon_choose.get():dungeon_nums.get()})
    dungeon_config_lable_list[id].append(ttk.Label(dungeon_tab_list[id],text=f"{dungeon_config_list[id][-1]}",font=('',12)))
    dungeon_config_lable_list[id][-1].pack(anchor='center')
    root.update()
# 删除副本配置项
def delete_dungeon_config():
    id = dungeon_notebook.index("current")
    dungeon_config_list[id].pop()
    dungeon_config_lable_list[id][-1].pack_forget()
    dungeon_config_lable_list[id][-1].destroy()
    dungeon_config_lable_list[id].pop()
    root.update()
# 保存副本配置项
def save_dungeon_config():
    id = dungeon_notebook.index("current")
    save_dungeon_info("dungeon.json",dungeon_title[id],dungeon_config_list[id])
# 清理图片log
def clear_imglog():
    logpath = "./logs/image"
    imglog_list = os.listdir(logpath)
    for img in imglog_list:
        os.remove(os.path.join(logpath,img))
    log.info("图片log清理完毕")

# 关闭程序
def close_window():
    root.destroy()
    auto_map.calculated.release_mouse_keyboard()

# 按键关闭程序
def btn_close_window():
    def on_press(key):
        if key == keyboard.Key.f8:
            close_window()
    with keyboard.Listener(on_press=on_press) as listener:  # 创建按键监听线程
        listener.join()  # 等待按键监听线程结束
# map_value_list的值初始化
def set_map_value_list(map_value_list,value):
    for map_value in map_value_list:
        map_value.set(value)
# 清体力下拉框
def index_dungeon_change(event):
    dungeon_list = read_json_info("dungeon.json",index_dungeon_choose.get(),prepath="dungeon")
    dungeon_box.config(values=dungeon_list)
    dungeon_choose.set(dungeon_list[0])
    root.update()
# 显隐cmd
CMD = win32console.GetConsoleWindow()
def hide_cmd():
    if win32gui.IsWindowVisible(CMD):
        win32gui.ShowWindow(CMD, 0)  # 隐藏命令行窗口
    else:
        win32gui.ShowWindow(CMD, 1)  # 显示命令行窗口
if __name__ == '__main__':
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        # messagebox.showerror("运行错误", "请以管理员权限运行")
        # raise Exception("请以管理员身份运行")
    # 锄大地实例
    auto_map = Map()
    # 清体力实例
    auto_dungeon = Dungeon()
    # gui页面
    root = tk.Tk()
    root.tk.call("source", "./tkinter/azure.tcl")
    root.tk.call("set_theme", "light")
    root.iconbitmap('./favicon.ico')
    # root.geometry('800x800+100+100')
    root.title(TITLE_NAME)
    root.resizable(True,True)
    # 主页面
    mainframe = ttk.Frame(root)
    ttk.Label(mainframe,text=TITLE_NAME,font=('Arial Black', 24)).grid()
    ttk.Label(mainframe,text=VER,font=('Arial Black', 16)).grid()
    ttk.Button(mainframe,text='锄大地',width=10,command=Enter_frame2).grid(pady=5,ipady=10)
    ttk.Button(mainframe,text='清体力',width=10,command=Enter_dungeonframe).grid(pady=5,ipady=10)
    ttk.Button(mainframe,text='兑换码',width=10,command=Enter_cdkframe).grid(pady=5,ipady=10)
    ttk.Button(mainframe,text='多脚本执行',width=10,command=Enter_allframe).grid(pady=5,ipady=10)
    ttk.Button(mainframe,text='显隐cmd',width=10,command=hide_cmd).grid(pady=5,ipady=10)
    # ttk.Button(mainframe,text='编辑配置',width=10).grid(pady=5,ipady=10)

    # 公告页面
    announce_frame = ttk.Frame(root)
    ttk.Label(announce_frame,text=TITLE_NAME,font=('Arial Black', 24)).grid(columnspan=2)
    ttk.Label(announce_frame,text=VER,font=('Arial Black', 16)).grid(columnspan=2)
    ttk.Label(announce_frame,text='项目地址:',font=('Arial Black', 16)).grid(column=0,row=2)
    repo_url = "https://github.com/Souloco/StarRail-FastRun"
    repo_url_text = ttk.Entry(announce_frame,width=40)
    repo_url_text.insert(0,repo_url)
    repo_url_text.grid(column=1,row=2)
    ttk.Label(announce_frame,text='公告',font=('Arial Black', 16)).grid(columnspan=2)
    s = ttk.Scrollbar(announce_frame)
    announce_text = tk.Text(announce_frame,font=('',16),undo=True, autoseparators=False,wrap='none', yscrollcommand=s.set)
    # 获取信息
    repos_url = 'https://api.github.com/repos/Souloco/StarRail-FastRun/releases/latest'
    # 请求版本最新信息
    try:
        response = requests.get(repos_url)
        if response.status_code == 200:
            data = response.json()
            # 获取版本信息
            version = data['tag_name']
            lowversion = str(data["body"]).split("lowversion:")[1]
            announce_text.insert('end',data["body"])
            if lowversion > VER:
                ver_update = True
                messagebox.showerror("版本更新","当前版本过低，请更新")
        else:
            announce_text.insert('end',"网络获取失败")
    except Exception:
        announce_text.insert('end',"疑似网络超时")
    announce_text.configure(state='disabled')
    announce_text.grid(columnspan=2,padx=5,pady=5)
    ttk.Button(announce_frame,text='确认',width=10,command=Enter_mainframe).grid(columnspan=2)
    announce_frame.pack()

    # 锄大地页面
    hoe_frame = ttk.Frame(root)
    ttk.Label(hoe_frame,text=TITLE_NAME,font=('Arial Black', 24)).grid(columnspan=4)
    ttk.Label(hoe_frame,text=VER,font=('Arial Black', 16)).grid(columnspan=4)
    ttk.Label(hoe_frame,text='必跑路线',font=('Arial Black', 16)).grid(columnspan=4)
    # notebook地图选项
    map_list = read_map()
    map_title = [('空间站「黑塔」',1),('雅利洛-VI',2),('仙舟「罗浮」',3),('匹诺康尼',4)]    # 星球选项
    map_notebook = ttk.Notebook(hoe_frame)
    map_tab_list = []
    map_value_list = []
    map_checkbutton_list = []
    map_list_data = get_config("map_list_data")
    map_allname_list1 = read_maplist_name()
    for i in range(len(map_title)):
        map_tab_list.append(ttk.Frame(map_notebook))
        map_notebook.add(map_tab_list[i],text=map_title[i][0])

    for i in range(len(map_list)):
        planet_id = map_list[i][map_list[i].index('_') + 1:map_list[i].index('-')]
        map_id = map_list[i][map_list[i].index('-') + 1:map_list[i].index('_',5)]
        index_id = map_list[i][map_list[i].index('_',5) + 1:map_list[i].index('.')]
        map_value_list.append(tk.IntVar(value=0))
        if map_list[i] in map_list_data:
            map_value_list[i].set(1)
        map_checkbutton_list.append(ttk.Checkbutton(map_tab_list[int(planet_id)-1],text=map_allname_list1[i],variable=map_value_list[i],onvalue=1, offvalue=0,width=10))
        map_checkbutton_list[i].grid(row=int(map_id),column=int(index_id))
    map_notebook.grid(columnspan=4)
    # 按钮
    ttk.Button(hoe_frame,text='全选',width=10,command=lambda:set_map_value_list(map_value_list,1)).grid(row=4,column=0,columnspan=2)
    ttk.Button(hoe_frame,text='清空',width=10,command=lambda:set_map_value_list(map_value_list,0)).grid(row=4,column=2,columnspan=2)
    # auto_notebook地图选项
    ttk.Label(hoe_frame,text='重跑路线',font=('Arial Black', 16)).grid(columnspan=4)
    auto_map_notebook = ttk.Notebook(hoe_frame)
    auto_map_tab_list = []
    auto_map_value_list = []
    auto_map_checkbutton_list = []
    auto_map_list_data = get_config("auto_map_list_data")
    for i in range(len(map_title)):
        auto_map_tab_list.append(ttk.Frame(auto_map_notebook))
        auto_map_notebook.add(auto_map_tab_list[i],text=map_title[i][0])
    for i in range(len(map_list)):
        planet_id = map_list[i][map_list[i].index('_') + 1:map_list[i].index('-')]
        map_id = map_list[i][map_list[i].index('-') + 1:map_list[i].index('_',5)]
        index_id = map_list[i][map_list[i].index('_',5) + 1:map_list[i].index('.')]
        auto_map_value_list.append(tk.IntVar(value=0))
        if map_list[i] in auto_map_list_data:
            auto_map_value_list[i].set(1)
        auto_map_checkbutton_list.append(ttk.Checkbutton(auto_map_tab_list[int(planet_id)-1],text=map_allname_list1[i],variable=auto_map_value_list[i],onvalue=1, offvalue=0,width=10))
        auto_map_checkbutton_list[i].grid(row=int(map_id),column=int(index_id))
    auto_map_notebook.grid(columnspan=4)
    # 按钮
    ttk.Button(hoe_frame,text='全选',width=10,command=lambda:set_map_value_list(auto_map_value_list,1)).grid(row=7,column=0)
    ttk.Button(hoe_frame,text='清空',width=10,command=lambda:set_map_value_list(auto_map_value_list,0)).grid(row=7,column=1)
    # 锄大地配置
    # 重跑次数
    ttk.Label(hoe_frame,text='重跑次数:',font=('', 12)).grid(row=7,column=2)
    auto_map_nums = tk.IntVar()
    auto_map_nums.set(get_config("auto_map_nums"))
    auto_map_spinbox = ttk.Spinbox(hoe_frame,from_=0, to=10, increment=1,textvariable=auto_map_nums)
    auto_map_spinbox.grid(row=7,column=3)
    # 切换队伍
    teamid_sets = tk.IntVar()
    teamid_option_list = [1,2,3,4,5,6]
    id_sets = tk.IntVar()
    id_option_list = [1,2,3,4]
    ttk.Label(hoe_frame,text='队伍/人物编号:').grid(row=8,column=0,pady=5)
    ttk.OptionMenu(hoe_frame,teamid_sets,get_config("team_id"),*teamid_option_list).grid(row=9,column=0,pady=5)
    ttk.OptionMenu(hoe_frame,id_sets,get_config("character_id"),*id_option_list).grid(row=10,column=0,pady=5)
    team_change_var = tk.BooleanVar()
    team_change_var.set(get_config("team_change"))
    img_log_Var = tk.BooleanVar()
    img_log_Var.set(get_config("img_log"))
    close_game_var = tk.BooleanVar()
    close_game_var.set(get_config("close_game"))
    commission_var = tk.BooleanVar()
    commission_var.set(get_config("commission"))
    # 配置开关
    ttk.Checkbutton(hoe_frame,text="切换队伍",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=team_change_var).grid(row=8,column=1,pady=5)
    ttk.Checkbutton(hoe_frame,text="委托开关",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=commission_var).grid(row=8,column=2,pady=5)
    ttk.Checkbutton(hoe_frame,text="截图记录",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=img_log_Var).grid(row=9,column=1,pady=5)
    ttk.Checkbutton(hoe_frame,text="自动关机",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=close_game_var).grid(row=9,column=2,pady=5)
    # 按钮
    ttk.Button(hoe_frame,text='确定',width=10,command=Enter_logframe).grid(row=8,column=3)
    ttk.Button(hoe_frame,text='保存',width=10,command=save_config).grid(row=9,column=3)
    ttk.Button(hoe_frame,text='返回',width=10,command=Enter_mainframe).grid(row=10,column=3)

    # 日志页面
    logframe = ttk.Frame(root)
    ttk.Label(logframe, text='实时日志', font=('Arial Black', 16)).pack(anchor='nw')   # justify控制对其方向，anchor控制位置 共同使文本靠左
    ttk.Button(logframe, text='开始',width=5,command=Enter_map).place(relx=0.60,rely=0)
    ttk.Button(logframe, text='清理',width=5,command=clear_imglog).place(relx=0.70,rely=0)
    ttk.Button(logframe, text='结束',width=5,command=close_window).place(relx=0.80,rely=0)
    ttk.Button(logframe, text='返回',width=5,command=Enter_mainframe).place(relx=0.90,rely=0)
    s2 = ttk.Scrollbar(logframe)      # 设置垂直滚动条
    b2 = ttk.Scrollbar(logframe, orient='horizontal')    # 水平滚动条
    s2.pack(side='right', fill='y')     # 靠右，充满Y轴
    b2.pack(side='bottom', fill='x')    # 靠下，充满x轴
    logtext = tk.Text(logframe,font=('Consolas', 9),undo=True, autoseparators=False,wrap='none', xscrollcommand=b2.set, yscrollcommand=s2.set)  # , state=DISABLED, wrap='none'表示不自动换行
    logtext.pack(fill='both', expand='yes')
    logtext.insert('end', 'Successfully connected to log\n')
    s2.config(command=logtext.yview)  # Text随着滚动条移动被控制移动
    b2.config(command=logtext.xview)
    handler = TextboxHandler(logtext)
    log.add(handler,format="{time:HH:mm:ss} " + "|{level}| " + "{module}.{function}:{line} - {message}")

    # 兑换码页面
    cdkframe = ttk.Frame(root)
    ttk.Label(cdkframe, text='兑换码助手', font=('Arial Black', 16)).pack(anchor='nw')   # justify控制对其方向，anchor控制位置 共同使文本靠左
    ttk.Button(cdkframe, text='兑换',width=5,command=Enter_cdk).place(relx=0.80,rely=0)
    ttk.Button(cdkframe, text='结束',width=5,command=close_window).place(relx=0.90,rely=0)
    s1 = ttk.Scrollbar(cdkframe)      # 设置垂直滚动条
    s1.pack(side='right', fill='y')     # 靠右，充满Y轴
    cdktext = tk.Text(cdkframe,font=('Consolas',15),undo=True, autoseparators=False,wrap='none', yscrollcommand=s1.set)  # , state=DISABLED, wrap='none'表示不自动换行
    cdktext.pack(fill='both', expand='yes')
    s1.config(command=logtext.yview)  # Text随着滚动条移动被控制移动

    # 清体力页面
    dungeonframe = ttk.Frame(root)
    ttk.Label(dungeonframe,text=TITLE_NAME,font=('Arial Black', 24)).grid(columnspan=4)
    ttk.Label(dungeonframe,text=VER,font=('Arial Black', 16)).grid(columnspan=4)
    ttk.Label(dungeonframe,text='副本类型:',font=('helvetica', 12)).grid(row=2,column=0)
    index_dungeon_list = read_json_info("dungeon.json","indexname",prepath="dungeon")
    index_dungeon_choose = tk.StringVar()
    index_dungeon_choose.set(index_dungeon_list[0])
    index_dungeon_box = ttk.Combobox(dungeonframe,textvariable=index_dungeon_choose,values=index_dungeon_list,width=25)
    index_dungeon_box.bind("<<ComboboxSelected>>",index_dungeon_change)
    index_dungeon_box.grid(row=2,column=1)
    ttk.Label(dungeonframe,text='具体副本:',font=('helvetica', 12)).grid(row=2,column=2)
    dungeon_list = read_json_info("dungeon.json",index_dungeon_choose.get(),prepath="dungeon")
    dungeon_choose = tk.StringVar()
    dungeon_choose.set(dungeon_list[0])
    dungeon_box = ttk.Combobox(dungeonframe,textvariable=dungeon_choose,values=dungeon_list,width=25)
    dungeon_box.grid(row=2,column=3)
    ttk.Label(dungeonframe,text='执行次数:',font=('helvetica', 12)).grid(row=3,column=0)
    dungeon_nums = tk.IntVar()
    dungeon_nums.set(1)
    dungeon_spinbox = ttk.Spinbox(dungeonframe,from_=1, to=100, increment=1,textvariable=dungeon_nums)
    dungeon_spinbox.grid(row=3,column=1)
    ttk.Button(dungeonframe,text='添加',command=add_dungeon_config).grid(row=3,column=2)
    ttk.Button(dungeonframe,text='删除',command=delete_dungeon_config).grid(row=3,column=3)
    # notebook副本配置
    dungeon_notebook = ttk.Notebook(dungeonframe)
    dungeon_title = read_json_info("dungeon.json","configname",prepath="dungeon")
    dungeon_tab_list = []
    dungeon_config_list = []
    dungeon_config_lable_list = []
    for i in range(len(dungeon_title)):
        dungeon_tab_list.append(ttk.Frame(dungeon_notebook))
        dungeon_notebook.add(dungeon_tab_list[i],text=dungeon_title[i])
        dungeon_config_list.append(read_json_info("dungeon.json",dungeon_title[i],prepath="dungeon"))
        dungeon_config_lable = []
        for j in range(len(dungeon_config_list[i])):
            dungeon_config_lable.append(ttk.Label(dungeon_tab_list[i],text=f"{dungeon_config_list[i][j]}",font=('', 12)))
            dungeon_config_lable[j].pack(anchor='center')
        dungeon_config_lable_list.append(dungeon_config_lable)
    dungeon_notebook.grid(columnspan=4)
    ttk.Button(dungeonframe,text='开始',width=10,command=enter_dungeon_all).grid(columnspan=4,pady=5)
    ttk.Button(dungeonframe,text='保存',width=10,command=save_dungeon_config).grid(columnspan=4,pady=5)
    ttk.Button(dungeonframe,text='返回',width=10,command=Enter_mainframe).grid(columnspan=4,pady=5)
    # 多功能合一执行页面
    allframe = ttk.Frame(root)
    ttk.Label(allframe,text=TITLE_NAME,font=('Arial Black', 24)).grid(columnspan=4)
    ttk.Label(allframe,text=VER,font=('Arial Black', 16)).grid(columnspan=4)
    ttk.Checkbutton(allframe,text="截图记录",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=img_log_Var).grid(row=2,column=0)
    ttk.Checkbutton(allframe,text="自动关机",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=close_game_var).grid(row=2,column=2)
    ttk.Button(allframe,text='开始',width=10,command=enter_function_all).grid(columnspan=4,pady=5)
    ttk.Button(allframe,text='返回',width=10,command=Enter_mainframe).grid(columnspan=4,pady=5)
    # 按键监听线程
    t1 = threading.Thread(name='btn_close',target=btn_close_window)
    t1.daemon = True
    t1.start()
    # 版本更新
    if ver_update:
        time.sleep(5)
        close_window()
    win32gui.ShowWindow(CMD, 0)  # 隐藏命令行窗口
    root.mainloop()
