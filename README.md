# StarRail-FastRun
![Static Badge](https://img.shields.io/badge/platfrom-Windows-blue?color=blue)
![GitHub release (with filter)](https://img.shields.io/github/v/release/Souloco/StarRail-FastRun)
![GitHub all releases](https://img.shields.io/github/downloads/Souloco/StarRail-FastRun/total)


# 免责声明
本软件是一个外部工具旨在自动化崩坏星轨的游戏玩法。它被设计成仅通过现有用户界面与游戏交互,并遵守相关法律法规。该软件包旨在提供简化和用户通过功能与游戏交互,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。

This software is open source, free of charge and for learning and exchange purposes only. The developer team has the final right to interpret this project. All problems arising from the use of this software are not related to this project and the developer team. If you encounter a merchant using this software to practice on your behalf and charging for it, it may be the cost of equipment and time, etc. The problems and consequences arising from this software have nothing to do with it.

本软件开源、免费，仅供学习交流使用。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。

请注意，根据MiHoYo的 崩坏:星穹铁道的公平游戏宣言:
```
"严禁使用外挂、加速器、脚本或其他破坏游戏公平性的第三方工具。"
"一经发现，米哈游（下亦称“我们”）将视违规严重程度及违规次数，采取扣除违规收益、冻结游戏账号、永久封禁游戏账号等措施。"
```
# 使用说明
- 环境配置
    - python安装
        - 版本要求```3.11.x```
        - [python推荐安装版本3.11.3](https://www.python.org/downloads/release/python-3113/)
        - 页面拉至底部，下载Windows installer (64-bit)
        - 点击安装包进行安装
        - 勾选Add Python 3.x to PATH
    - 依赖安装
        - 安装方式一:
            - 打开```cmd```并切换到StarRail-FastRun文件夹路径
                - 方法一：win+R输入cmd,输入```cd 文件夹路径```切换到StarRail-FastRun文件夹路径
                - 方法二:打开StarRail-FastRun文件夹,在```文件夹路径处输入cmd```
            - 输入```pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/```
            - 根据提示确认是否安装完毕
        - 安装方式二：
            - 下载```setup.exe```在StarRail-FastRun文件夹目录下启动
            - 根据提示确认是否安装完毕
- 游戏设置
    - 是否沿用自动战斗设置---```是```
    - 操作模式：疾跑---```长按进入疾跑状态```
    - 视角灵敏度---3
    - 游戏分辨率```1920x1080```---有窗口化选窗口化没有就选全屏幕
- 软件设置
    - 以管理员身份运行```gui.exe```
    - ```英文(不带空格)```路径下使用
- 软件使用
    - 锄大地
        - ```远程角色```带队最佳
        - 路线测试角色```佩拉|驭空|青雀|艾丝妲|符玄|娜塔莎|托帕```
        - 切换锄地路线---```编辑配置下切换|通用路线|驭空路线---全程秘技跑---暂未完善```
        - 秘技使用---```部分路线打地图上的秘技点|托帕不必准备食物,地图上秘技点够用```
        - 秘技食物---```消耗补充秘技点的食物```
        - 截图记录---```存放至logs\image下|日志页面清理按钮可清空图片log|不对路线有所改动不必打开```
        - 自动关机---```关闭游戏|关闭程序|执行强制关机指令```
        - 重跑路线---```捡漏代替选项|后续捡漏功能实装时会删除|重跑次数为0不执行```
        - 疾跑切换---```执行前切换疾跑模式为长按进入疾跑状态|执行完毕后切换后短按|与模拟宇宙跑步模式适配```
        - 委托开关
        - 切换队伍
    - 清体力
        - 默认执行```当前选中配置```
    - 多功能执行
        - 执行顺序```清体力-清委托-锄大地-自动关机```
        - 清委托执行需打开```委托开关```
        - 自动关机需打开```自动关机```
    - 快速启动---用于定时执行|自动开机执行
        - 在多功能执行页面```配置```
        - 清体力支持时间条件执行|默认执行```配置1```
        - 编辑配置页面---游戏路径设置成本体路径```Game/StarRail.exe```
        - 执行顺序```启动游戏-清体力-清委托-锄大地-自动关机```
        - 以管理员身份运行```FastStart.exe```
    - 快捷键---在日志界面触发
        - 开始---```f7```
        - 暂停---```f8```
        - 结束---```f10```
    - 编辑配置
        - gui字体设置
        - gui字体大小
        - 切换锄地路线---```自定义锄地路线请仿造maps下的文件夹格式```
        - 更新代理---更新不成功自行更换可用的代理网址末尾需带有```/```
        - 游戏路径
    - 桌面通知
        - 运行```notify.exe```
- 进阶使用
    - 调用模拟宇宙(https://github.com/CHNZYX/Auto_Simulated_Universe)     
        - 点击Code---Download ZIP---下载Auto_Simulated_Universe-main.zip
        - 在本项目下解压成Auto_Simulated_Universe-main文件夹
        - 模拟宇宙详细配置请使用模拟宇宙本体gui
    - 定时执行
        - ```计算机管理-任务计划程序-创建任务```
        - 常规-```使用最高权限运行|配置```
        - 触发器-```设定时间```
        - 操作-```启动程序-选择FastStart.exe```
        - 条件|设置-自行设定
    - 自动开机执行
        - BIOS电源设置自动开机时间由于不同品牌设置不同自行百度设置
        - 电源选项-选择电源按钮的功能-点击```更改当前不可用的设置```将```启用快速启动(推荐)```取消
        - 搭配```定时执行```
- 在线更新
    - 自行在main分支下下载```发布包体不带有update.exe```
    - 运行```update.exe```
# 实现功能
- [x] 锄大地
- [x] 清体力
- [x] 清委托
- [x] 多功能合一执行
- [ ] 捡漏
# Star History
[![Star History Chart](https://api.star-history.com/svg?repos=Souloco/StarRail-FastRun&type=Date)](https://star-history.com/#Souloco/StarRail-FastRun&Date)
