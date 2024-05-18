# StarRail-FastRun
![Static Badge](https://img.shields.io/badge/platfrom-Windows-blue?color=blue)
![GitHub release (with filter)](https://img.shields.io/github/v/release/Souloco/StarRail-FastRun)
![GitHub all releases](https://img.shields.io/github/downloads/Souloco/StarRail-FastRun/total)
![Static Badge](https://img.shields.io/badge/QQ%E7%BE%A4-906995514-purple)



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
        - 通用路线```远程角色```带队最佳|黄泉路线```需备足零食```|gui编辑配置下切换路线后重启软件
        - 通用路线测试角色```佩拉|驭空|青雀|艾丝妲|符玄|娜塔莎|托帕|布洛妮娅|阮梅|黑天鹅```
        - 秘技使用---```部分路线打地图上的秘技点|托帕不必准备食物,地图上秘技点够用```
        - 秘技食物---```消耗补充秘技点的食物```
        - 截图记录---```存放至logs\image下|日志页面清理按钮可清空图片log|不对路线有所改动不必打开```
        - 自动关机---```关闭游戏|关闭程序|执行强制关机指令```
        - 重跑路线---```重跑次数为0不执行```
        - 疾跑切换---```执行前切换疾跑模式为长按进入疾跑状态|执行完毕后切换后短按|与模拟宇宙跑步模式适配```
        - 切换队伍---```按照配置切换队伍```
    - 清体力
        - 默认执行```当前选中配置```
        - 根据配置可按```时间指定配置```
    - 清任务
        - 请到```多功能执行页面```配置
        - 委托开关---领取委托
        - 支援奖励---领取支援奖励
        - 每日实训---领取每日实训奖励
        - 无名勋礼---领取无名勋礼任务
        - 零食购买---```需使用黄泉```
        - 零食合成---合成奇巧零食
    - 多功能执行
        - 执行顺序```清委托-领取支援奖励-清体力-锄大地-模拟宇宙-领取每日实训-灵位无名勋礼-自动关机```
        - 清体力---是否执行清体力
        - 锄大地---是否执行锄大地
        - 模拟宇宙---是否执行模拟宇宙
        - 关闭模式---```禁止---不关闭任何东西|关闭---关闭游戏和程序|关机---关闭+关机|注销---关闭+注销```
    - 快捷键---在日志界面触发
        - 开始---```f7```
        - 暂停---```f8```
        - 结束---```f10```
    - 编辑配置
        - gui字体设置
        - gui字体大小
        - 切换锄地路线---```自定义锄地路线请仿造maps下自带路线格式```
            - 自带路线说明
                - map---`兼容大部分远程角色使用|已停止更新`
                - huangquan---`黄泉路线---提前自备足够的零食|用时较短`
                - huangquan-full---`黄泉full路线---尽可能减小零食消耗|会打更多的破坏物|用时较长|@淡提供维护更新`
        - 更新代理---更新不成功自行更换可用的代理网址末尾需带有```/```
        - 游戏路径---```游戏本体路径Game\StarRail.exe```
        - 战斗时间---默认为900s```练度过低需要调高此数值```
        - 旋转系数---```如果转视角不准确,请调整此数值```|正确的转视角白日梦酒店-1初始旋转后正对电梯开关|旋转公式:旋转数值x旋转系数x分辨率
    - 快速启动---用于定时执行|自动开机执行
        - 在多功能执行页面```配置```
        - 清体力支持时间条件执行|默认执行```配置1```
        - 编辑配置页面---游戏路径设置成本体路径```Game/StarRail.exe```
        - 执行顺序```启动游戏-多功能执行顺序```
        - 以管理员身份运行```FastStart.exe```
        - 不支持快捷键
    - 桌面通知
        - 运行```notify.exe```
# 常见问题
- 运行过程中卡在图片点击阶段,请自行截取相应图片替换picture文件夹下的对应图片
- 调低画质设置,可以降低漏怪概率|黄泉路线最稳定
- 因设备差异,可能转视角有所差异,请借助录图的转向键```<和>```键(M键右边俩)让角色转向```获取正确旋转数值```计算对应旋转系数=```正确的旋转数值```/路线设置旋转数值
# 进阶使用
- 在线更新
    - 如果更新不成功请自行更换配置镜像源
    - 自行在main分支下下载```发布包体不带有update.exe```
    - 运行```update.exe```
- 调用模拟宇宙(https://github.com/CHNZYX/Auto_Simulated_Universe)     
    - 点击Code---Download ZIP---下载Auto_Simulated_Universe-main.zip
    - 在本项目下解压成Auto_Simulated_Universe-main文件夹
    - 请先确保你已安装模拟宇宙需求的依赖环境
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
# 配置文件说明
## 锄大地路线```map_X-X-X.json```
- 参数说明
    - start列表参数

    | 参数 | 说明 |
    | --- | --- |
    | map | 数值为寻找的指定楼层,""不寻找楼层|
    | 图片名字带格式 | 寻找传送点---目前默认为1.5s|
    | transfer | 点击传送,目前默认数值为1.5s|

    - map列表参数

    | 参数 | 说明 |
    | --- | --- |
    | a,s,w,d | 移动跑步---按下[a,s,w,d]+shift指定秒数|
    | A,S,W,D | 移动走路---按下[a,s,w,d]指定秒数 |
    | e | 使用秘技---数值为秘技使用动画时间,单位为秒,目前默认为1.2s|
    | r | 使用梦泡---数值为r键按下时间,目前默认为1s|
    | fighting | 攻击---数值为1,攻击完后等待战斗判定结束;其他数值攻击完后无战斗判断,2代表可破坏物标记,3代表秘技点标记|
    | loc_angle | 校准视角---数值0-360,右为0，上为90,左为180，下为270|
    | mouse_move | 水平移动视角---数值正负分别代表视角移动方向,单位为px|
    | delay | 延迟---数值为延迟时间,单位为秒 |
## 录图
- 启动录制脚本```record.bat```
- ```不要同时按多个键```，疾跑```先按住shift```再赶路（转弯时注意衔接不要掉速）或者```按住鼠标右键```保持疾跑状态
- 鼠标操作请使用攻击键、转向键（绝对转向时可先用鼠标）
- 交互键:```F 使用交互 R 使用梦泡```---f交互键按下之前，请先超快短按补一个wasd位移，录入蹭的方向（例如先w再f最终记为f:w）
- 秘技键:```E 使用秘技 ```
- 攻击键：```X 打怪 V 打罐子```
- 转向键：```<和>```键(M键右边俩)让角色转向，多次点按直到转朝目标
- 绝对转向：手动转到目标方向，然后按```F7键```，通过小地图箭头记录视角(get_loc_angle)
- 视角转正：```方向键↑↓←→```，视角转朝小地图对应方向(loc_angle)
- ```F8保存+重录，F9保存+退出，F10闪退```
- 保存在```maps/save```文件夹下
# 实现功能
- [x] 锄大地
- [x] 清体力
- [x] 清任务
- [x] 多功能合一执行
# Star History
[![Star History Chart](https://api.star-history.com/svg?repos=Souloco/StarRail-FastRun&type=Date)](https://star-history.com/#Souloco/StarRail-FastRun&Date)
# 打赏
如果喜欢本项目，可以微信赞赏,您的支持就是作者开发和维护项目的动力
![](picture/tip.jpg)
