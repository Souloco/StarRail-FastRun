# StarRail-FastRun
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
    - 键鼠模式显示底部提示---```是```---V1.3.6版本及以后已弃用
    - 操作模式：疾跑---```长按进入疾跑状态```
    - 视角灵敏度---3
    - 游戏分辨率```1920x1080```---有窗口化选窗口化没有就选全屏幕
- 软件设置
    - 以管理员身份运行```gui.exe```
    - 英文路径下使用
- 软件使用
    - 锄大地
        - ```远程角色```带队最佳
    - 清体力
        - 默认执行```当前选中配置```
    - 多功能执行
        - 执行顺序```清体力-清委托-锄大地-自动关机```
        - 清委托执行需打开```委托开关```
        - 自动关机需打开```自动关机```
    - 快速启动---用于定时执行|自动开机执行
        - 在多功能执行页面```配置```
        - 清体力默认执行```配置1```
        - 执行顺序```启动游戏-清体力-清委托-锄大地-自动关机```
        - 以管理员身份运行```FastStart.exe```
    - 快捷键---在日志界面触发
        - 开始---```f7```
        - 暂停---```f8```
        - 结束---```f10```
- 进阶使用
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
    - 运行```update.exe```
# 实现功能
- [x] 锄大地
- [x] 清体力
- [x] 清委托
- [x] 多功能合一执行
- [ ] 捡漏
# Star History
[![Star History Chart](https://api.star-history.com/svg?repos=Souloco/StarRail-FastRun&type=Date)](https://star-history.com/#Souloco/StarRail-FastRun&Date)
