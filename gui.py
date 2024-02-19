import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
from utils.config import read_map,read_maplist_name,set_config,get_config,read_json_info,check_config
from utils.StarRail import StarRail
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
VER = read_json_info('version.json','version')
# 版本更新提示
ver_update = False
# 模拟宇宙标志符
u_flag = os.path.isdir("./Auto_Simulated_Universe-main")
if u_flag:
    with open("./Auto_Simulated_Universe-main/logs/notif.txt",'r',encoding="utf-8") as file:
        u_text = f"模拟宇宙完成次数:{file.readline()}"
        file.close()
else:
    u_text = "未获取到模拟宇宙完成次数"
# 用于日志文本框
class TextboxHandler(logging.Handler):
    def __init__(self, textbox:tk.Text):
        logging.Handler.__init__(self)
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.insert("end", msg + "\n")
        self.textbox.see("end")
# 事件
# 进入锄大地页面
def Enter_hoeframe():
    if not sra.thread.is_alive():
        logframe.pack_forget()
        mainframe.pack_forget()
        hoe_frame.pack()
        root.update()
        sra.mode = 0
    else:
        log.warning("功能线程还在运行！")
# 进入主页面
def Enter_mainframe():
    logframe.pack_forget()
    announce_frame.pack_forget()
    universe_frame.pack_forget()
    allframe.pack_forget()
    hoe_frame.pack_forget()
    dungeonframe.pack_forget()
    configframe.pack_forget()
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

# 进入模拟宇宙页面
def Enter_Universeframe():
    if not sra.thread.is_alive():
        logframe.pack_forget()
        mainframe.pack_forget()
        universe_frame.pack()
        root.update()
        sra.mode = 0
    else:
        log.warning("功能线程还在运行！")
# 应用模拟宇宙配置
def universe_config():
    sra.universe_bonus = universe_bonus.get()
    sra.universe_nums = universe_nums.get()
# 保存模拟宇宙配置
def save_universe_config():
    set_config("universe_bonus",universe_bonus.get())
    set_config("universe_nums",universe_nums.get())
# 保存配置
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
    set_config("skill",skill_var.get())
    set_config("run_change",run_change_var.get())
# 进入日志页面
def Enter_logframe(logmode:int = 1):
    # 页面初始化
    hoe_frame.pack_forget()
    dungeonframe.pack_forget()
    universe_frame.pack_forget()
    allframe.pack_forget()
    logframe.pack()
    sra.mode = logmode
    if logmode == 1:
        # 锄大地启用配置
        map_config()
        logreturn.configure(command=Enter_hoeframe)
    elif logmode == 2:
        # 清体力启用配置
        dungeon_config()
        logreturn.configure(command=Enter_dungeonframe)
    elif logmode == 3:
        # 锄大地启用配置
        map_config()
        # 清体力启用配置
        dungeon_config()
        # 模拟宇宙启用配置
        universe_config()
        # 多功能执行启用配置
        allfunction_config()
        logreturn.configure(command=Enter_allframe)
    elif logmode == 4:
        # 模拟宇宙启用配置
        universe_config()
        logreturn.configure(command=Enter_Universeframe)
    root.update()
# 进入清体力页面
def Enter_dungeonframe():
    if not sra.thread.is_alive():
        logframe.pack_forget()
        mainframe.pack_forget()
        dungeonframe.pack()
        root.update()
        sra.mode = 0
    else:
        log.warning("功能线程还在运行！")
# 进入多功能合一执行页面
def Enter_allframe():
    if not sra.thread.is_alive():
        logframe.pack_forget()
        mainframe.pack_forget()
        allframe.pack()
        root.update()
        sra.mode = 0
    else:
        log.warning("功能线程还在运行！")
# 进入编辑配置页面
def Enter_configframe():
    mainframe.pack_forget()
    configframe.pack()
    root.update()
# 多功能执行配置
def allfunction_config():
    sra.map_flag = auto_map_var.get()
    sra.dungeon_flag = auto_dungeon_var.get()
    sra.universe_flag = auto_universe_var.get()
    # 清任务配置启用
    sra.task.commission_flag = task_commission_var.get()
    sra.task.supportrewards_flag = task_supportrewards_var.get()
    sra.task.dailytask_flag = task_dailytask_var.get()
    sra.task.rewards_flag = task_rewards_var.get()
    # 自动关机配置启用
    sra.close_game = close_game_var.get()
# 锄地配置启用
def map_config():
    sra.map.map_list = get_map_list(map_value_list)
    sra.map.auto_map_list = get_map_list(auto_map_value_list)
    sra.map.calculated.img_log_value = img_log_Var.get()
    sra.map.team_change = team_change_var.get()
    sra.map.teamid = teamid_sets.get()
    sra.map.id = id_sets.get()
    sra.map.nums = auto_map_nums.get()
    sra.map.skill = skill_var.get()
    sra.map.skill_food = skill_food_var.get()
    sra.map.run_change = run_change_var.get()
    sra.map.planetid = 0
    sra.calculated.fight_time = fight_time.get()
# 副本配置启用
def dungeon_config():
    sra.dungeon.team_change = team_change_var.get()
    sra.dungeon.teamid = dungeon_teamid_sets.get()
    sra.dungeon.id = dungeon_id_sets.get()
    if dungeon_time_flag.get():
        id = dungeon_title.index(dungeon_time[today_id])
    else:
        id = dungeon_notebook.index("current")
    sra.dungeon.dungeon_list = dungeon_config_list[id]
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
    for id in range(len(dungeon_title)):
        set_config(dungeon_title[id],dungeon_config_list[id])
    set_config("dungeon_team_id",dungeon_teamid_sets.get())
    set_config("dungeon_character_id",dungeon_id_sets.get())
    set_config("team_change",team_change_var.get())
    set_config("dungeon_time",dungeon_time)
    set_config("dungeon_time_flag",dungeon_time_flag.get())
# 保存多脚本执行配置项
def save_all_config():
    save_dungeon_config()
    save_config()
    set_config("auto_map",auto_map_var.get())
    set_config("auto_dungeon",auto_dungeon_var.get())
    set_config("auto_universe",auto_universe_var.get())
    set_config("task_commission",task_commission_var.get())
    set_config("task_supportrewards",task_supportrewards_var.get())
    set_config("task_dailytask",task_dailytask_var.get())
    set_config("task_rewards",task_rewards_var.get())
# 应用与保存gui配置项
def save_gui_config():
    defaultfont.configure(family=fontfamilt_sets.get(),size=font_sizes.get())
    titlefont.configure(family=fontfamilt_sets.get(),size=font_sizes.get()+12)
    versionfont.configure(family=fontfamilt_sets.get(),size=font_sizes.get()+6)
    root.update()
    set_config("fontsize",font_sizes.get())
    set_config("fontfamily",fontfamilt_sets.get())
    set_config("map_type",map_type_sets.get())
    set_config("proxy",proxy_text.get())
    set_config("gamepath",game_path.get())
    set_config("fight_time",fight_time.get())

# 清理图片log
def clear_imglog():
    logpath = "./logs/image"
    imglog_list = os.listdir(logpath)
    log.info("图片log清理开始")
    for img in imglog_list:
        os.remove(os.path.join(logpath,img))
    log.info("图片log清理完毕")

# 关闭程序
def close_window():
    sra.stop()
    root.destroy()

# 按键监听线程
def btn_close_window():
    def on_press(key):
        if key == keyboard.Key.f7:
            sra.start()
        if key == keyboard.Key.f10:
            close_window()
        if key == keyboard.Key.f8:
            sra.stop()
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
# 显隐重跑路线
def hide_auto_map():
    if auto_map_notebook.winfo_ismapped():
        auto_map_label.grid_forget()
        auto_map_notebook.grid_forget()
        auto_map_btn1.grid_forget()
        auto_map_btn2.grid_forget()
        auto_map_btn3.grid_forget()
        auto_map_btn4.grid_forget()
        set_config("auto_map_hide",False)
    else:
        auto_map_label.grid(row=5,columnspan=5)
        auto_map_notebook.grid(row=6,columnspan=5)
        auto_map_btn1.grid(row=7,column=0)
        auto_map_btn2.grid(row=7,column=1)
        auto_map_btn3.grid(row=7,column=3)
        auto_map_btn4.grid(row=7,column=4)
        set_config("auto_map_hide",True)
    root.update()
if __name__ == '__main__':
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        # messagebox.showerror("运行错误", "请以管理员权限运行")
        # raise Exception("请以管理员身份运行")
    # 配置检查
    check_config()
    # 功能实例
    sra = StarRail()
    # gui页面
    root = tk.Tk()
    root.tk.call("source", "./tkinter/azure.tcl")
    root.tk.call("set_theme", "light")
    root.iconbitmap('./favicon.ico')
    root.geometry("+{}+{}".format(int(root.winfo_screenwidth()/4),int(root.winfo_screenheight()/8)))
    root.title(TITLE_NAME)
    root.resizable(True,True)
    # 字体设置
    defaultfontfamily = get_config("fontfamily")
    defaultfontsize = get_config("fontsize")
    defaultfont = tkfont.Font(family=defaultfontfamily,size=defaultfontsize)
    titlefont = tkfont.Font(family=defaultfontfamily,size=defaultfontsize+12,weight='bold')
    versionfont = tkfont.Font(family=defaultfontfamily,size=defaultfontsize+6,weight='bold')
    ttk.Style().configure(".",font=defaultfont)
    root.option_add("*Font",defaultfont)
    # 主页面
    mainframe = ttk.Frame(root)
    ttk.Label(mainframe,text=TITLE_NAME,font=titlefont).grid()
    ttk.Label(mainframe,text=VER,font=versionfont).grid()
    ttk.Button(mainframe,text='锄大地',width=10,command=Enter_hoeframe).grid(pady=5,ipady=10)
    ttk.Button(mainframe,text='清体力',width=10,command=Enter_dungeonframe).grid(pady=5,ipady=10)
    if u_flag:
        ttk.Button(mainframe,text='模拟宇宙',command=Enter_Universeframe,width=10).grid(pady=5,ipady=10)
    ttk.Button(mainframe,text='多功能执行',width=10,command=Enter_allframe).grid(pady=5,ipady=10)
    ttk.Button(mainframe,text='显隐cmd',width=10,command=hide_cmd).grid(pady=5,ipady=10)
    ttk.Button(mainframe,text='编辑配置',width=10,command=Enter_configframe).grid(pady=5,ipady=10)

    # 公告页面
    announce_frame = ttk.Frame(root)
    ttk.Label(announce_frame,text=TITLE_NAME,font=titlefont).grid(columnspan=2)
    ttk.Label(announce_frame,text=VER,font=versionfont).grid(columnspan=2)
    ttk.Label(announce_frame,text='项目地址:',font=versionfont).grid(column=0,row=2)
    repo_url = "https://github.com/Souloco/StarRail-FastRun"
    repo_url_text = ttk.Entry(announce_frame,width=40)
    repo_url_text.insert(0,repo_url)
    repo_url_text.grid(column=1,row=2)
    s = ttk.Scrollbar(announce_frame)
    announce_text = tk.Text(announce_frame,undo=True, autoseparators=False,wrap='none', yscrollcommand=s.set)
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

    # 模拟宇宙页面
    universe_frame = ttk.Frame(root)
    ttk.Label(universe_frame,text=TITLE_NAME,font=titlefont).grid(columnspan=4)
    ttk.Label(universe_frame,text=VER,font=versionfont).grid(columnspan=4)
    ttk.Label(universe_frame,text="执行次数:").grid(columnspan=2,row=2,column=0)
    universe_nums = tk.IntVar()
    universe_nums.set(get_config("universe_nums"))
    universe_spinbox = ttk.Spinbox(universe_frame,from_=1, to=34, increment=1,textvariable=universe_nums)
    universe_spinbox.grid(columnspan=2,row=2,column=2)
    universe_bonus = tk.IntVar()
    universe_bonus.set(get_config("universe_bonus"))
    ttk.Label(universe_frame,text=u_text).grid(columnspan=4,pady=5)
    ttk.Checkbutton(universe_frame,text="沉浸奖励",style="Switch.TCheckbutton",onvalue=1,offvalue=0,variable=universe_bonus).grid(columnspan=4,pady=5)
    ttk.Button(universe_frame,text='确定',width=10,command=lambda:Enter_logframe(4)).grid(columnspan=4,pady=5)
    ttk.Button(universe_frame,text='保存',width=10,command=save_universe_config).grid(columnspan=4,pady=5)
    ttk.Button(universe_frame,text='返回',width=10,command=Enter_mainframe).grid(columnspan=4,pady=5)

    # 锄大地页面
    hoe_frame = ttk.Frame(root)
    ttk.Label(hoe_frame,text=TITLE_NAME,font=titlefont).grid(columnspan=5)
    ttk.Label(hoe_frame,text=VER,font=versionfont).grid(columnspan=5)
    map_type = get_config("map_type")
    sra.map.mappath = f"maps\\{map_type}"
    ttk.Label(hoe_frame,text=f'必跑路线---{map_type.replace("yukongmap","驭空路线").replace("map","通用路线")}',font=versionfont).grid(columnspan=5)
    # notebook地图选项
    map_list = read_map(map_type)
    map_title = [('空间站「黑塔」',1),('雅利洛-VI',2),('仙舟「罗浮」',3),('匹诺康尼',4)]    # 星球选项
    map_notebook = ttk.Notebook(hoe_frame)
    map_tab_list = []
    map_value_list = []
    map_planet_value_list = []
    map_checkbutton_list = []
    map_list_data = get_config("map_list_data")
    map_allname_list1 = read_maplist_name(map_type)
    for i in range(len(map_title)):
        map_tab_list.append(ttk.Frame(map_notebook))
        map_notebook.add(map_tab_list[i],text=map_title[i][0])
        map_planet_value_list.append([])

    for i in range(len(map_list)):
        planet_id = map_list[i][map_list[i].index('_') + 1:map_list[i].index('-')]
        map_id = map_list[i][map_list[i].index('-') + 1:map_list[i].index('_',5)]
        index_id = map_list[i][map_list[i].index('_',5) + 1:map_list[i].index('.')]
        map_value_list.append(tk.IntVar(value=0))
        map_planet_value_list[int(planet_id)-1].append(map_value_list[i])
        if map_list[i] in map_list_data:
            map_value_list[i].set(1)
        map_checkbutton_list.append(ttk.Checkbutton(map_tab_list[int(planet_id)-1],text=map_allname_list1[i],variable=map_value_list[i],onvalue=1, offvalue=0,width=12))
        map_checkbutton_list[i].grid(row=int(map_id),column=int(index_id))
    map_notebook.grid(columnspan=5)
    # 按钮
    ttk.Button(hoe_frame,text='单页选择',width=10,command=lambda:set_map_value_list(map_planet_value_list[map_notebook.index("current")],1)).grid(row=4,column=0)
    ttk.Button(hoe_frame,text='全部选择',width=10,command=lambda:set_map_value_list(map_value_list,1)).grid(row=4,column=1)
    ttk.Button(hoe_frame,text='单页清空',width=10,command=lambda:set_map_value_list(map_planet_value_list[map_notebook.index("current")],0)).grid(row=4,column=3)
    ttk.Button(hoe_frame,text='全部清空',width=10,command=lambda:set_map_value_list(map_value_list,0)).grid(row=4,column=4)
    ttk.Button(hoe_frame,text='显隐重跑路线',width=10,command=hide_auto_map).grid(row=4,column=2)
    # auto_notebook地图选项
    auto_map_label = ttk.Label(hoe_frame,text='重跑路线',font=versionfont)
    auto_map_notebook = ttk.Notebook(hoe_frame)
    auto_map_tab_list = []
    auto_map_value_list = []
    auto_map_planet_value_list = []
    auto_map_checkbutton_list = []
    auto_map_list_data = get_config("auto_map_list_data")
    for i in range(len(map_title)):
        auto_map_tab_list.append(ttk.Frame(auto_map_notebook))
        auto_map_notebook.add(auto_map_tab_list[i],text=map_title[i][0])
        auto_map_planet_value_list.append([])
    for i in range(len(map_list)):
        planet_id = map_list[i][map_list[i].index('_') + 1:map_list[i].index('-')]
        map_id = map_list[i][map_list[i].index('-') + 1:map_list[i].index('_',5)]
        index_id = map_list[i][map_list[i].index('_',5) + 1:map_list[i].index('.')]
        auto_map_value_list.append(tk.IntVar(value=0))
        auto_map_planet_value_list[int(planet_id)-1].append(auto_map_value_list[i])
        if map_list[i] in auto_map_list_data:
            auto_map_value_list[i].set(1)
        auto_map_checkbutton_list.append(ttk.Checkbutton(auto_map_tab_list[int(planet_id)-1],text=map_allname_list1[i],variable=auto_map_value_list[i],onvalue=1,offvalue=0,width=12))
        auto_map_checkbutton_list[i].grid(row=int(map_id),column=int(index_id))
    # 按钮
    auto_map_btn1 = ttk.Button(hoe_frame,text='单页选择',width=10,command=lambda:set_map_value_list(auto_map_planet_value_list[auto_map_notebook.index("current")],1))
    auto_map_btn2 = ttk.Button(hoe_frame,text='全部选择',width=10,command=lambda:set_map_value_list(auto_map_value_list,1))
    auto_map_btn3 = ttk.Button(hoe_frame,text='单页清空',width=10,command=lambda:set_map_value_list(auto_map_planet_value_list[auto_map_notebook.index("current")],0))
    auto_map_btn4 = ttk.Button(hoe_frame,text='全部清空',width=10,command=lambda:set_map_value_list(auto_map_value_list,0))
    if get_config("auto_map_hide"):
        hide_auto_map()
    # 锄大地配置
    # 重跑次数
    ttk.Label(hoe_frame,text='重跑次数:').grid(row=8,column=1,pady=5)
    auto_map_nums = tk.IntVar()
    auto_map_nums.set(get_config("auto_map_nums"))
    auto_map_spinbox = ttk.Spinbox(hoe_frame,from_=0, to=10, increment=1,textvariable=auto_map_nums)
    auto_map_spinbox.grid(row=8,column=2,pady=5)
    # 切换队伍
    teamid_sets = tk.IntVar()
    teamid_option_list = [1,2,3,4,5,6,7,8,9]
    id_sets = tk.IntVar()
    id_option_list = [1,2,3,4]
    ttk.Label(hoe_frame,text='队伍/人物编号:').grid(row=8,column=0,pady=5)
    ttk.OptionMenu(hoe_frame,teamid_sets,get_config("team_id"),*teamid_option_list).grid(row=9,column=0,pady=5)
    ttk.OptionMenu(hoe_frame,id_sets,get_config("character_id"),*id_option_list).grid(row=10,column=0,pady=5)
    team_change_var = tk.BooleanVar()
    team_change_var.set(get_config("team_change"))
    img_log_Var = tk.BooleanVar()
    img_log_Var.set(get_config("img_log"))
    skill_var = tk.BooleanVar()
    skill_var.set(get_config("skill"))
    skill_food_var = tk.BooleanVar()
    skill_food_var.set(get_config("skill_food"))
    run_change_var = tk.BooleanVar()
    run_change_var.set(get_config("run_change"))
    # 配置开关
    ttk.Checkbutton(hoe_frame,text="切换队伍",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=team_change_var).grid(row=9,column=1,pady=5)
    ttk.Checkbutton(hoe_frame,text="秘技使用",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=skill_var).grid(row=9,column=2,pady=5)
    ttk.Checkbutton(hoe_frame,text="疾跑切换",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=run_change_var).grid(row=9,column=3,pady=5)
    ttk.Checkbutton(hoe_frame,text="截图记录",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=img_log_Var).grid(row=10,column=1)
    ttk.Checkbutton(hoe_frame,text="秘技食物",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=skill_food_var).grid(row=10,column=2)

    ttk.Button(hoe_frame,text='确定',width=10,command=lambda:Enter_logframe(1)).grid(row=8,column=4,pady=5)
    ttk.Button(hoe_frame,text='保存',width=10,command=save_config).grid(row=9,column=4,pady=5)
    ttk.Button(hoe_frame,text='返回',width=10,command=Enter_mainframe).grid(row=10,column=4)

    # 日志页面
    logframe = ttk.Frame(root)
    ttk.Label(logframe, text='实时日志', font=('Arial Black',16)).pack(anchor='nw')   # justify控制对其方向，anchor控制位置 共同使文本靠左
    logstart = ttk.Button(logframe, text='开始',width=5,command=sra.start)
    logstart.place(relx=0.40,rely=0)
    ttk.Button(logframe, text='停止',width=5,command=sra.stop).place(relx=0.52,rely=0)
    ttk.Button(logframe, text='结束',width=5,command=close_window).place(relx=0.64,rely=0)
    ttk.Button(logframe, text='清理',width=5,command=clear_imglog).place(relx=0.76,rely=0)
    logreturn = ttk.Button(logframe, text='返回',width=5,command=Enter_mainframe)
    logreturn.place(relx=0.88,rely=0)
    s2 = ttk.Scrollbar(logframe)      # 设置垂直滚动条
    b2 = ttk.Scrollbar(logframe, orient='horizontal')    # 水平滚动条
    s2.pack(side='right', fill='y')     # 靠右，充满Y轴
    b2.pack(side='bottom', fill='x')    # 靠下，充满x轴
    logtext = tk.Text(logframe,font=('Consolas', 9),undo=True, autoseparators=False,wrap='none', xscrollcommand=b2.set, yscrollcommand=s2.set)  # , state=DISABLED, wrap='none'表示不自动换行
    logtext.pack(fill='both', expand='yes')
    s2.config(command=logtext.yview)  # Text随着滚动条移动被控制移动
    b2.config(command=logtext.xview)
    handler = TextboxHandler(logtext)
    log.add(handler,format="{time:HH:mm:ss} " + "|{level}| " + "{module}.{function}:{line} - {message}")
    # 清体力页面
    dungeonframe = ttk.Frame(root)
    ttk.Label(dungeonframe,text=TITLE_NAME,font=titlefont).grid(columnspan=4)
    ttk.Label(dungeonframe,text=VER,font=versionfont).grid(columnspan=4)
    ttk.Label(dungeonframe,text='副本类型:').grid(row=2,column=0)
    index_dungeon_list = read_json_info("dungeon.json","indexname",prepath="dungeon")
    index_dungeon_choose = tk.StringVar()
    index_dungeon_choose.set(index_dungeon_list[0])
    index_dungeon_box = ttk.Combobox(dungeonframe,textvariable=index_dungeon_choose,values=index_dungeon_list)
    index_dungeon_box.bind("<<ComboboxSelected>>",index_dungeon_change)
    index_dungeon_box.grid(row=2,column=1)
    ttk.Label(dungeonframe,text='具体副本:').grid(row=2,column=2)
    dungeon_list = read_json_info("dungeon.json",index_dungeon_choose.get(),prepath="dungeon")
    dungeon_choose = tk.StringVar()
    dungeon_choose.set(dungeon_list[0])
    dungeon_box = ttk.Combobox(dungeonframe,textvariable=dungeon_choose,values=dungeon_list)
    dungeon_box.grid(row=2,column=3)
    ttk.Label(dungeonframe,text='执行次数:').grid(row=3,column=0)
    dungeon_nums = tk.IntVar()
    dungeon_nums.set(1)
    dungeon_spinbox = ttk.Spinbox(dungeonframe,from_=1, to=100, increment=1,textvariable=dungeon_nums)
    dungeon_spinbox.grid(row=3,column=1)
    ttk.Button(dungeonframe,text='添加',command=add_dungeon_config).grid(row=3,column=2,padx=5)
    ttk.Button(dungeonframe,text='删除',command=delete_dungeon_config).grid(row=3,column=3)
    # 切换队伍
    dungeon_teamid_sets = tk.IntVar()
    dungeon_id_sets = tk.IntVar()
    ttk.Label(dungeonframe,text='队伍/人物编号:').grid(row=4,column=0,pady=5)
    ttk.OptionMenu(dungeonframe,dungeon_teamid_sets,get_config("dungeon_team_id"),*teamid_option_list).grid(row=4,column=1,pady=5)
    ttk.OptionMenu(dungeonframe,dungeon_id_sets,get_config("dungeon_character_id"),*id_option_list).grid(row=4,column=2,pady=5)
    ttk.Checkbutton(dungeonframe,text="切换队伍",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=team_change_var).grid(row=4,column=3,pady=5)
    # 时间条件执行
    days_title = ["周日","周一","周二","周三","周四","周五","周六"]
    today_id = int(time.strftime("%w", time.localtime()))
    index_days_choose = tk.StringVar()
    index_days_choose.set(days_title[today_id])
    index_days_box = ttk.Combobox(dungeonframe,textvariable=index_days_choose,values=days_title)

    def index_days_change(event):
        days_id = index_days_box.current()
        if days_id != -1:
            dungeon_days_choose.set(dungeon_time[days_id])

    index_days_box.bind("<<ComboboxSelected>>",index_days_change)
    index_days_box.grid(row=5,column=0)

    dungeon_title = read_json_info("dungeon.json","configname",prepath="dungeon")
    dungeon_time = get_config("dungeon_time")
    dungeon_days_choose = tk.StringVar()
    dungeon_days_choose.set(dungeon_time[today_id])
    days_box = ttk.Combobox(dungeonframe,textvariable=dungeon_days_choose,values=dungeon_title)

    def days_change(event):
        days_id = index_days_box.current()
        if days_id != -1:
            dungeon_time[days_id] = dungeon_days_choose.get()

    days_box.bind("<<ComboboxSelected>>",days_change)
    days_box.grid(row=5,column=1)
    dungeon_time_flag = tk.BooleanVar()
    dungeon_time_flag.set(get_config("dungeon_time_flag"))
    ttk.Checkbutton(dungeonframe,text="时间条件",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=dungeon_time_flag).grid(row=5,column=2,padx=5,pady=5)
    # notebook副本配置
    dungeon_notebook = ttk.Notebook(dungeonframe)
    dungeon_tab_list = []
    dungeon_config_list = []
    dungeon_config_lable_list = []
    for i in range(len(dungeon_title)):
        dungeon_tab_list.append(ttk.Frame(dungeon_notebook))
        dungeon_notebook.add(dungeon_tab_list[i],text=dungeon_title[i])
        dungeon_config_list.append(get_config(dungeon_title[i]))
        dungeon_config_lable = []
        for j in range(len(dungeon_config_list[i])):
            dungeon_config_lable.append(ttk.Label(dungeon_tab_list[i],text=f"{dungeon_config_list[i][j]}",font=('', 12)))
            dungeon_config_lable[j].pack(anchor='center')
        dungeon_config_lable_list.append(dungeon_config_lable)
    dungeon_notebook.grid(columnspan=4)
    ttk.Button(dungeonframe,text='确定',width=10,command=lambda:Enter_logframe(2)).grid(columnspan=4,pady=5)
    ttk.Button(dungeonframe,text='保存',width=10,command=save_dungeon_config).grid(columnspan=4,pady=5)
    ttk.Button(dungeonframe,text='返回',width=10,command=Enter_mainframe).grid(columnspan=4,pady=5)

    # 多功能合一执行页面
    allframe = ttk.Frame(root)
    ttk.Label(allframe,text=TITLE_NAME,font=titlefont).grid(columnspan=4)
    ttk.Label(allframe,text=VER,font=versionfont).grid(columnspan=4)
    ttk.Label(allframe,text='清体力队伍/人物编号:').grid(row=2,column=0,pady=5)
    ttk.OptionMenu(allframe,dungeon_teamid_sets,get_config("dungeon_team_id"),*teamid_option_list).grid(row=2,column=1,pady=5)
    ttk.OptionMenu(allframe,dungeon_id_sets,get_config("dungeon_character_id"),*id_option_list).grid(row=2,column=2,pady=5)
    ttk.Label(allframe,text='锄大地队伍/人物编号:').grid(row=3,column=0,pady=5)
    ttk.OptionMenu(allframe,teamid_sets,get_config("team_id"),*teamid_option_list).grid(row=3,column=1,pady=5)
    ttk.OptionMenu(allframe,id_sets,get_config("character_id"),*id_option_list).grid(row=3,column=2,pady=5)
    # 单项功能执行
    auto_universe_var = tk.BooleanVar()
    auto_universe_var.set(get_config("auto_universe"))
    auto_map_var = tk.BooleanVar()
    auto_map_var.set(get_config("auto_map"))
    auto_dungeon_var = tk.BooleanVar()
    auto_dungeon_var.set(get_config("auto_dungeon"))
    # 清任务功能执行
    task_commission_var = tk.BooleanVar()
    task_commission_var.set(get_config("task_commission"))
    task_supportrewards_var = tk.BooleanVar()
    task_supportrewards_var.set(get_config("task_supportrewards"))

    task_dailytask_var = tk.BooleanVar()
    task_dailytask_var.set(get_config("task_dailytask"))
    task_rewards_var = tk.BooleanVar()
    task_rewards_var.set(get_config("task_rewards"))
    # 自动关机功能执行
    close_game_var = tk.BooleanVar()
    close_game_var.set(get_config("close_game"))
    ttk.Checkbutton(allframe,text="清体力",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=auto_dungeon_var).grid(row=2,column=3,pady=5)
    ttk.Checkbutton(allframe,text="锄大地",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=auto_map_var).grid(row=3,column=3,pady=5)
    ttk.Checkbutton(allframe,text="委托开关",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=task_commission_var).grid(row=4,column=0,pady=5)
    ttk.Checkbutton(allframe,text="支援奖励",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=task_supportrewards_var).grid(row=4,column=1,pady=5)
    ttk.Checkbutton(allframe,text="每日实训",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=task_dailytask_var).grid(row=4,column=2,pady=5)
    ttk.Checkbutton(allframe,text="无名勋礼",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=task_rewards_var).grid(row=4,column=3,pady=5)
    if u_flag:
        ttk.Checkbutton(allframe,text="模拟宇宙",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=auto_universe_var).grid(row=5,column=3,pady=5)
    ttk.Checkbutton(allframe,text="切换队伍",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=team_change_var).grid(row=5,column=0,pady=5)
    ttk.Checkbutton(allframe,text="截图记录",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=img_log_Var).grid(row=5,column=1,pady=5)
    ttk.Checkbutton(allframe,text="自动关机",style="Switch.TCheckbutton",onvalue=True,offvalue=False,variable=close_game_var).grid(row=5,column=2,pady=5)
    ttk.Label(allframe,text=u_text).grid(columnspan=4)
    ttk.Button(allframe,text='确定',width=10,command=lambda:Enter_logframe(3)).grid(columnspan=4,pady=5)
    ttk.Button(allframe,text='保存',width=10,command=save_all_config).grid(columnspan=4,pady=5)
    ttk.Button(allframe,text='返回',width=10,command=Enter_mainframe).grid(columnspan=4,pady=5)
    # 编辑配置页面
    configframe = ttk.Frame(root)
    ttk.Label(configframe,text=TITLE_NAME,font=titlefont).grid(columnspan=4)
    ttk.Label(configframe,text=VER,font=versionfont).grid(columnspan=4)
    # 字体设置
    ttk.Label(configframe,text='字体设置:').grid(row=2,column=0,columnspan=2,pady=5)
    font_names = tkfont.families()
    fontfamilt_sets = tk.StringVar()
    ttk.OptionMenu(configframe,fontfamilt_sets,defaultfontfamily,*font_names).grid(row=2,column=2,columnspan=2,pady=5)
    ttk.Label(configframe,text='字体大小:').grid(row=3,column=0,columnspan=2,pady=5)
    font_sizes = tk.IntVar()
    font_sizes.set(get_config("fontsize"))
    ttk.Spinbox(configframe,from_=5, to=100, increment=1,textvariable=font_sizes).grid(row=3,column=2,columnspan=2,pady=5)
    ttk.Label(configframe,text='锄地路线:').grid(row=4,column=0,columnspan=2,pady=5)
    map_types = os.listdir("./maps")
    map_type_sets = tk.StringVar()
    map_type_sets.set(map_type)
    ttk.OptionMenu(configframe,map_type_sets,map_type,*map_types).grid(row=4,column=2,columnspan=2,pady=5)
    ttk.Label(configframe,text='更新代理:').grid(row=5,column=0,columnspan=2,pady=5)
    proxy_text = ttk.Entry(configframe)
    proxy_text.grid(row=5,column=2,columnspan=2,pady=5)
    proxy_text.insert(0,get_config("proxy"))
    ttk.Label(configframe,text='游戏路径:').grid(row=6,column=0,columnspan=2,pady=5)
    game_path = tk.StringVar()
    game_path.set(get_config("gamepath"))
    game_text = ttk.Entry(configframe,textvariable=game_path)
    game_text.grid(row=6,column=2,columnspan=2,pady=5)
    ttk.Label(configframe,text='战斗时间:').grid(row=7,column=0,columnspan=2,pady=5)
    fight_time = tk.IntVar()
    fight_time.set(get_config("fight_time"))
    fight_time_spinbox = ttk.Spinbox(configframe,from_=1, to=3600, increment=1,textvariable=fight_time)
    fight_time_spinbox.grid(row=7,column=2,columnspan=2,pady=5)
    ttk.Button(configframe,text='确定',width=10,command=save_gui_config).grid(columnspan=4,pady=5)
    ttk.Button(configframe,text='返回',width=10,command=Enter_mainframe).grid(columnspan=4,pady=5)
    # 按键监听线程
    t1 = threading.Thread(name='btn_close',target=btn_close_window,daemon=True)
    t1.start()
    # 版本更新
    if ver_update:
        time.sleep(5)
        close_window()
    win32gui.ShowWindow(CMD, 0)  # 隐藏命令行窗口
    root.mainloop()
