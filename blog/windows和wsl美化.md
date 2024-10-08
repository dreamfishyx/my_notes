#### 前言&展示

作为一个颜狗，很喜欢archlinx搭配hyprland的配置，但是Wayland桌面+fcitx5输入法,在typora和chrome间切换有大概率会输入法无法聚焦，导致无法输入(作为重度用户，无法接受，很不方便)，尝试许多方法未得到解决。于是卸载双系统重新改回 win11+wsl ,折腾了一天，成果展示:<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241007220814.png" style="zoom: 35%;" /><br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241007223458.png" style="zoom: 50%;" />

---





#### 配置过程

##### Terminal

1. win11 默认安装 Terminal ，可以直接使用。

2. 安装推荐字体进入[Nerd Fonts](https://www.nerdfonts.com/)随便下载一款字体(推荐 FiraCode Nerd Font )，并在 windows 上安装,然后在 Terminal 的 设置->默认值->外观->字体 中设置你安装的字体即可。

3. 安装 oh-my-posh ，实际详细配置参考[官网](https://ohmyposh.dev/docs/installation/windows)。管理员权限下的 powershell 运行`winget install JanDeDobbeleer.OhMyPosh -s winget --location D:\Environment\oh-my-posh\` 安装 oh-my-posh 到指定位置(我这里是D:\Environment\oh-my-posh)。

4. 配置环境变量:`POSH_THEMES_PATH`中配置主题文件目录位置：

   <br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241008081151.png" style="zoom:67%;" />

5. (补充)：为 powershell 安装一些图标美化插件`Install-Module -Name Terminal-Icons -Repository PSGallery`

6. 管理员 powershell 运行`notepad $profile`编辑 powershell 配置文件。其中`--config`后面接主题配置的文件位置(全部在 oh-my-posh 安装目录的 themes 目录下)。

   ```powershell
   # 图标美化
   Import-Module -Name Terminal-Icons
   
   # oh-my-posh 主题
   oh-my-posh --init --shell pwsh --config "$env:POSH_THEMES_PATH\catppuccin_frappe.omp.json" | Invoke-Expression
   ```


5. 运行`. $profile`使配置生效。

6. 对于 cmd 无法使用 oh-my-posh ，但是官方提供解决方式：下载[clink](https://github.com/chrisant996/clink/releases)工具，安装一个已知位置。然后，进入 clink 安装目录，创建`oh-my-posh.lua`文件，添加如下内容：

   ```shell
   load(io.popen('oh-my-posh init cmd --config D:\\Environment\\oh-my-posh\\themes\\catppuccin_frappe.omp.json'):read("*a"))()
   ```

7. 最新的 window 已经内置 sudo 命令，无需安装 gsudo 软件，只需要在 设置->系统->开发者选项 中启用 sudo 命令，并建议设置为内联启动即可。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241008083451.png" style="zoom:67%;" />

8. 此外我们可以为powershell添加一些配色主题：[iTerm2-Color-Schemes](https://github.com/mbadolato/iTerm2-Color-Schemes) 项目的 windwosterminal 目录对应的 json 文件复制样式，将样式粘贴到windwos terminal配置文件(`CTRL+SHIFT+,`打开配置文件)的 schemes 数组中即可(Purple Peter、Nord、Catppuccin Macchiato、Catppuccin Frappé)。

   ```json
   "schemes": 
   [
       {
           "background": "#F7F7F7",
           "black": "#090300",
           "blue": "#01A0E4",
           "brightBlack": "#5C5855",
           "brightBlue": "#807D7C",
           "brightCyan": "#CDAB53",
           "brightGreen": "#3A3432",
           "brightPurple": "#D6D5D4",
           "brightRed": "#E8BBD0",
           "brightWhite": "#F7F7F7",
           "brightYellow": "#4A4543",
           "cursorColor": "#4A4543",
           "cyan": "#B5E4F4",
           "foreground": "#4A4543",
           "green": "#01A252",
           "name": "3024 Day", 
           "purple": "#A16A94",
           "red": "#DB2D20",
           "selectionBackground": "#A5A2A2",
           "white": "#A5A2A2",
           "yellow": "#FDED02"
       },
   ]
   ```

9. powershell的上方标签栏很碍眼，在Terminal设置的操作中设置一个切换专注模式的快捷键，然后在 设置->启动->启动参数->启动模式 设置为专注模式即可。

---



##### wsl安装

1. 需要说明的是，安装windows子系统，需要开启`Hyper-V`，启动方式参考网上教程。检查是否开启，打开任务管理器，选择任务一栏。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241008083645.png" style="zoom: 80%;" />

2. 但是，开启`Hyper-V`可能导致一些旧版本VMware等虚拟机无法使用，但是最新的虚拟机已经支持`Hyper-V`。

3. 打开控制面板，选择程序后，选择启动或者关闭windows功能(其实在 设置->系统->可选功能->添加可选功能 里面也可以启用)。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241008083842.png" style="zoom: 80%;" />

4. 开启虚拟机平台和适用于linux的windows子系统，重启计算机。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241008084027.png" style="zoom:67%;" />

5. 在 设置->系统->开发者选项 中启用开发人员模式。

6. 管理员权限下，使用`cmd`需要运行`wsl --update`更新WSL，而后运行命令`wsl --set-default-version 2`设置WSL版本。

7. `wsl --list --online`查看可安装的Linux发行版。这里提一下，不带版本号的`ubuntu`可以更新更高版本，带版本号的不能更新到更高版本。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241008090704.png" style="zoom:67%;" />

8. 运行`wsl --install <DistroName>`安装 linux 发行版。例如安装`wsl --install Ubuntu-22.04`，此后等待一段时间后，会要求设置账户和密码(这里是普通账户)。但是上面没有 Archlinux (用习惯了)，这里不采用上述方式安装linux发行版。

9. 下载安装包：[arch.zip](https://github.com/yuk7/ArchWSL),解压到合适的位置后运行Arch.exe文件(细节问题参考官方文档)。cmd 运行 wsl 命令启动，使用 passwd 命令设置 root 用户密码。

10. 换源和安装yay：

    1. `vim /etc/pacman.d/mirrorlist`添加如下源：

       ```tex
       # 中国科学技术大学开源镜像站
       Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch 
       # 清华大学开源软件镜像站
       Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch 
       # 华为开源镜像站
       Server = https://repo.huaweicloud.com/archlinux/$repo/os/$arch 
       # 兰州大学开源镜像站
       Server = http://mirror.lzu.edu.cn/archlinux/$repo/os/$arch 
       ```

    2. 开启32位支持库与ArchLinux中文社区仓库archlinuxcn。编辑`vim /etc/pacman.conf`：

       ```bash
       # 取消注释
       [multilib]
       Include = /etc/pacman.d/mirrorlist
       
       # 添加镜像源(选一个即可)
       [archlinuxcn]
       Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch # 中国科学技术大学开源镜像站
       Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch # 清华大学开源软件镜像站
       Server = https://mirrors.hit.edu.cn/archlinuxcn/$arch # 哈尔滨工业大学开源镜像站
       Server = https://repo.huaweicloud.com/archlinuxcn/$arch # 华为开源镜像站
       ```

    3. 配置签名：

       ```bash
       sudo pacman-key --init
       sudo pacman-key --populate
       sudo pacman -S archlinux-keyring # archlinux源签名
       sudo pacman -Syyu
       ```

    4. 安装 archlinuxcn 源签名和 yay :

       ```bash
       sudo pacman -S archlinuxcn-keyring # cn源中的签名
       sudo pacman -S yay
       ```

11. 创建新用户：

    1. `useradd -m -G wheel -s /bin/bash <username>`创建用户

    2. `passwd <username>`设置密码

    3. `EDITOR=vim visudo`打开配置，设置用户组权限：

       ```bash
       # 取消注释
       %wheel ALL=(ALL:ALL) ALL
       ```

    4. 退出wsl，设置启动时默认用户:`./Arch.exe config --default-user <username>`

12. 安装字体和一些基本软件：

    ```bash
    sudo pacman -S adobe-source-han-sans-cn-fonts adobe-source-han-serif-cn-fonts noto-fonts-cjk wqy-microhei wqy-microhei-lite wqy-bitmapfont wqy-zenhei ttf-arphic-ukai ttf-arphic-uming noto-fonts noto-fonts-cjk noto-fonts-emoji noto-fonts-extra
    
    sudo pacman -S base base-devel git curl wget neofetch net-tools dnsutils inetutils
    ```

13. 修改编码：`vim /etc/locale.gen`去掉`en_US.UTF-8 UTF-8`以及`zh_CN.UTF-8 UTF-8`行前的注释符号,后运行`locale-gen`和`echo 'LANG=en_US.UTF-8'  > /etc/locale.conf`

14. `wsl:检测到localhost代理配置，但未镜像到WSL。NAT模式下的WSL不支持localhost代理`的解决措施：在 C:\Users\用户名\ 下创建一个 .wslconfig 文件，然后在文件中写入如下内容:

    ```bash
    [experimental]
    autoMemoryReclaim=gradual  
    networkingMode=mirrored
    dnsTunneling=true
    firewall=true
    autoProxy=true
    ```

15. 设置root默认编辑器：`vim ~/.bash_profile`

    ```bash
    export EDITOR='vim'
    ```

---



##### wsl美化

1. 配置zsh:

   1. ` sudo pacman -S zsh`安装 zsh ，后运行`chsh -s $(which zsh)`配置为当前用户的默认shell(若不存在which先安装基本软件`pacman -S base-devel`)，然后运行`echo $SHELL`查看当前默认shell(其他用户登录时，可能会有一个选项，选择0生成`~/.zshrc`配置文件即可)。

   2. 安装 oh-my-zsh :`sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`

   3. 安装 powerlevel10k :`git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k`

   4. 装完后使用 `vim ~/.zshrc`配置好 `ZSH_THEME="powerlevel10k/powerlevel10k"`，运行`p10k configure`配置美化(安装要求选择即可)。

   5. 安装几个插件(仅对当前用户生效)：

      ```shell
      # zsh-syntax-highlighting:终端命令语法高亮
      git clone https://github.com/zsh-users/zsh-syntax-highlighting ~/.oh-my-zsh/plugins/zsh-syntax-highlighting
      
      # zsh-autosuggestions:自动补全
      git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/plugins/zsh-autosuggestions
      ```

   6. `vim ~/.zshrc`编辑文件，添加插件：

      ```bash
      plugins=(
      ...  # 之前已经声明的插件名称
      zsh-autosuggestions
      zsh-syntax-highlighting
      )
      ```

   7. 运行`source ~/.zshrc`重新加载配置文件。

2. 安装neovim替代vim: 略。

3. 显示信息：`pacman -S fastfetch`，然后运行`echo 'fastfetch' >> ~/.zshrc`。但是实际使用时发现 fastfetch 会卡死,参考下面讨论内容添加服务文件后修复：

   1. https://github.com/fastfetch-cli/fastfetch/issues/746

   2. https://github.com/microsoft/wslg/issues/1156

   3. https://github.com/microsoft/WSL/issues/6999#issuecomment-2303010704

   4. 此外可以配置要显示的组件模块：

      ```bash
      # 生成默认配置文件
      fastfetch --gen-config
      
      # 修改配置文件
      vim $HOME/.config/fastfetch/config.jsonc
      ```

---



##### 桌面美化软件

1. 壁纸配置: steam 安装壁纸引擎(Wallpaper Engine,收费)，按照自己的喜好设置壁纸,设置为开机自启。
2. dock栏： steam 安装 mybockfinder(收费) ，按照自己的喜好设置即可。或者也可以使用[Winstep Nexus](https://www.winstep.net/nexus.asp)。我需要通过系统托盘关一些后台软件，所以才用的mybockfinder 。
3. 状态栏透明:[TranslucentTB](https://github.com/TranslucentTB/TranslucentTB)(也可以直接在微软商店下载)，实际上 mybockfinder 占用内存还是有点大(不能接受)，所以还是直接透明化任务栏吧。右键状态栏，选择任务栏设置，然后在里面设置任务栏自动隐藏。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241008203835.png" style="zoom:80%;" />
4. 桌面组件：官网安装[雨滴插件](https://www.rainmeter.net/)，然后下载安装主题即可(推荐[致美化](https://zhutix.com/tag/rainmeter/))。
5. 鼠标样式：
   1. [致美化](https://zhutix.com/tag/cursors/)找自己喜欢的鼠标样式下载解压([目前正在使用](https://zhutix.com/ico/breeze-snow-hd-cus/))，右键`.inf`文件安装鼠标样式。
   2. [LeoRH123/Windows-11-Cursor-Concept-Pro-v2.0](https://github.com/LeoRH123/Windows-11-Cursor-Concept-Pro-v2.0?tab=readme-ov-file)直接下载源文件，右键`.inf`文件安装鼠标样式。
6. 搜狗输入法：可以配置一个打字跟随的输入法皮肤。
7. 一些推荐字体：
   1.  Fira Code：https://github.com/tonsky/FiraCode
   2.  Hack: https://github.com/source-foundry/Hack
   3. Inconsolata: https://github.com/googlefonts/Inconsolata


---



##### 软件图标生成

1. [1:1裁剪](https://picwish.cn/crop-image)

2. [在线抠图](https://picwish.cn/remove-background)

3. [图片圆角](https://www.butterpig.top/radius)

4. [图标ico格式](https://www.butterpig.top/icopro)和[图标png格式](http://androidasset.studio/icons-launcher.html#foreground.type=image&foreground.space.trim=1&foreground.space.pad=0.05&foreColor=rgba(96%2C%20125%2C%20139%2C%200)&backColor=rgb(96%2C%20125%2C%20139)&crop=0&backgroundShape=none&effects=none&name=ic_launcher)

5. 上述png图片格式图标可用于mydockfinder中。

6. 修改磁盘或者U盘的图标：创建好ico图标文件，在磁盘或者U盘内创建`autorun.inf`,添加如下内容指定图标位置，然后重启系统(U盘只需要重新插入即可)。当然你还可以将图标和文件隐藏，只需要右键后选择属性然后勾选隐藏即可。：

   ```bash
   [autorun]
   icon=.\disk.ico
   ```

   <br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/20241008111036.png" style="zoom:80%;" />

---



##### 软件推荐

1. picgo: 配置github或者阿里云OSS等搭建个人图床。

2. drawio: 画图软件。

3. motrix: 下载器，也可以试一试IDM和aria2。

4. 傲梅分区助手: 之前双系统EFI分区大小不足时就是用的这个软件拓展的(有风险，使用前备份分区，做好重装系统得准备)。

5. everything: 当软件不知道安装在哪儿或者配置文件找不到时，我总能想起它，哈哈。

6. Snipaste: 截图软件。

7. [7-zip](https://www.7-zip.org/download.html): 解压神器。

8. 火绒安全: 弹窗拦截。

9. scoop: Windows下的一个包管理器，它与Mac下的brew是一个类似的工具。爽！！！

   1. 在管理员下运行powershell,并运行以下安装命令：

      ```powershell
      Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
      
      irm get.scoop.sh | iex
      ```

   2. 当然上述软件的安装位置使用默认，作为一个合格的系统管理员，这是极其难受的，参考官方[Scoop安装程序](https://github.com/ScoopInstaller/Install#readme)得到第二种安装方式:

      ```bash
      irm get.scoop.sh -outfile 'install.ps1'
      
      # 配置一下软件安装目录(不需要管理员下运行,可以删除-RunAsAdmin参数)
      .\install.ps1 -ScoopDir 'D:\Scoop' -ScoopGlobalDir 'D:\Scoop\Global' -RunAsAdmin
      ```

   3. 若是开启系统代理，则需要配置配置代理(不配置会报错：Remove-Item:找不到路径“D:\Scoop\apps\scoop\new”，因为该路径不存在)：`scoop config proxy 127.0.0.1:10809`，此外删除代理命令为`scoop config rm proxy`。

   4. 其他配置参考这篇:[Windows包管理工具Scoop安装及使用](https://www.mobaijun.com/posts/908521329.html)



