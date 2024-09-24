##### 起因

最近postgreSQL有点火,想弄一个玩玩。但是不太想在电脑上安装(电脑安装了双系统，archlinux我只分配140G，并且上面已经存在mysql)。于是想着在服务器上安装，但是服务器上已经有很多东西。最终想到了之前折腾很久的termux。在termux中安装postgreSQL并使其在公网中可以访问。首先声明：瞎搞有风险，上手需谨慎。

---



##### 安装termux

Termux是Android平台上的一个终端模拟器，之所以称它为模拟器而非虚拟机，是因为它并非像PC端的VirtualBox等虚拟机软件那样，在宿主机中虚拟出一个完全独立且完整的系统环境，而只是提供一个接口，以安装和运行面向新环境交叉编译后的程序。这里给出项目地址：[termux](https://github.com/termux/termux-app)。

1. 安装：使用[f-droid](https://f-droid.org/zh_Hans/packages/)安装`termux`和`termux:styling`(注意先后顺序)。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202409121314805.png" style="zoom:67%;" />

2. 长按termux的界面，选择more后选择style。里面的`choose color`和`choose font`可以自定义颜色和字体。字体建议`Fantasque Sans Mono`(实际上后面会手动配置字体),配色建议`Base16 Codeschool light`即可。

3. 换源直接运行`termux-change-repo`,在图形界面引导下，使用自带方向键可上下移动。第一步使用空格选择镜像组mirror group，之后在第二步选择中国的镜像源。确认无误后回车，镜像源会自动完成更换。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202409121324176.jpg" style="zoom: 33%;" />

   <br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202409121324195.jpg" style="zoom: 33%;" />

4. apt换源使用如下命令行替换官方源为TUNA镜像源：

   ```bash
   sed -i 's@^\(deb.*stable main\)$@#\1\ndeb https://mirrors.tuna.tsinghua.edu.cn/termux/apt/termux-main stable main@' $PREFIX/etc/apt/sources.list
   apt update && apt upgrade
   ```

5. termux运行`termux-setup-storage`访问手机存储区,获取权限后,在 home 目录下会有一个storage文件夹, 可以通过这个文件夹访问手机储存(就类似于wsl的`/mnt`)。<span style="color:red">一定要在手机的Termux软件中执行，不要用任何远程连接软件。</span>

6. 换源之后记得运行`pkg update -y && pkg updrade -y`更新一下，不然可能无法使用`passwd`等命令。

7. 运行`pkg install termux-auth`后使用`passwd`设置密码。

----



##### ssh远程

1. 将手机与电脑连接在同一个局域网，或者手机开热点给电脑连接。

2. 运行下面命令安装并启动`openssh`。

   ```bash
   # 更新源
   pkg update
   
   # 安装ssh
   pkg install openssh
   
   # 启动ssh(默认端口号8022)
   sshd
   
   # 查看ip
   ifconfig
   ```

3. 运行`whoami`查询当前用户名，若需设置用户密码则需使用`passwd`命令。

4. 通过`ssh 用户名@ip -p 8022`连接`termux`即可。

5. 以后每次重启`mutex`客户端的时候，都需要输入`sshd`命令来开启ssh服务，不然连不上。为此我们可以设置其开机自启:

   ```bash
   pkg install termux-services
   
   # 重启(不然找不到命令)
   
   sv-enable sshd
   ```

6. 关于`ssh`连接经常断开的问题：在安卓系统上打开设置搜索应用启动管理关闭自动管理，打开后台启动。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202409121332417.jpg" style="zoom:33%;" />


---

##### neovim(非必要)

1. 使用`pkg install neovim`安装,使用`nvim -v`查看版本。下述文件夹若不存在，需要自行创建。

2. 安装依赖：

   ```bash
   pkg install git clang wget unzip nodejs python3 luarocks lazygit gdb cgdb
   apt install clang cmake
   ```

3. 安装字体：[Nerd Fonts](https://www.nerdfonts.com/font-downloads)找到满意字体右键复制链接

   ```bash
   mkdir -p ~/.termux/font
   cd ~/.termux/font
   wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/FiraCode.zip
   unzip FiraCode.zip
   rm LICENSE  README.md FiraCode.zip
   
   termux-reload-settings
   ```

4. 若上述步骤不行，则`nvim ~/.termux/termux.properties`，下面内容设置成你自己的字体路径。重新加载设置`termux-reload-settings`(似乎不行得重启)

   ```bash
   font-family: "~/.termux/font/ FiraCodeNerdFont-Medium.ttf"
   ```

5. 编辑`nvim ~/.config/nvim/lua/config/options.lua`:配置也是之前在网上抄的。

   ```lua
   -- 显示模式(关闭)
   vim.o.showmode = false
   
   -- utf8：设置编码为UTF-8
   vim.g.encoding = "UTF-8"
   vim.o.fileencoding = 'utf-8'
   
   -- jkhl 移动时光标周围保留8行
   vim.o.scrolloff = 8
   vim.o.sidescrolloff = 8
   
   -- 使用相对行号
   vim.wo.number = true
   vim.wo.relativenumber = true
   
   -- 高亮所在行
   vim.wo.cursorline = true
   
   -- 显示左侧图标指示列
   vim.wo.signcolumn = "yes"
   
   -- 右侧参考线，超过表示代码太长了，考虑换行
   -- vim.wo.colorcolumn = "80"
   
   -- 缩进4个空格等于一个Tab
   vim.o.tabstop = 4
   vim.bo.tabstop = 4
   vim.o.softtabstop = 4
   --vim.bo.shiftwidth = 4
   vim.o.shiftround = true
   
   -- >> << 时移动长度
   vim.o.shiftwidth = 2
   vim.bo.shiftwidth = 2
   
   -- 新行对齐当前行，空格替代tab
   --vim.o.expandtab = true
   --vim.bo.expandtab = true
   
   -- 新行对齐当前行
   vim.o.autoindent = true
   vim.bo.autoindent = true
   vim.o.smartindent = true
   
   -- 搜索大小写不敏感，除非包含大写
   vim.o.ignorecase = true
   vim.o.smartcase = true
   
   -- 当文件被外部程序修改时，自动加载
   vim.o.autoread = true
   vim.bo.autoread = true
   
   -- 自动缩进
   vim.o.autoindent = true
   vim.bo.autoindent = true
   
   -- 搜索不要高亮
   vim.o.hlsearch = false
   
   -- 边输入边搜索
   vim.o.incsearch = true
   
   -- 使用增强状态栏后不再需要vim的模式提示
   --vim.o.showmode = false
   
   -- 命令行高为2，提供足够的显示空间
   vim.o.cmdheight = 2
   
   -- 当文件被外部程序修改时，自动加载
   vim.o.autoread = true
   vim.bo.autoread = true
   
   -- 禁止折行
   vim.o.wrap = false
   vim.wo.wrap = false
   
   -- 行结尾可以跳到下一行
   vim.o.whichwrap = 'b,s,<,>,[,],h,l'
   
   -- 允许隐藏被修改过的buffer
   vim.o.hidden = true
   
   -- 鼠标支持
   vim.o.mouse = "a"
   
   -- 禁止创建备份文件
   vim.o.backup = false
   vim.o.writebackup = false
   vim.o.swapfile = false
   
   -- smaller updatetime 
   vim.o.updatetime = 300
   
   -- 设置 timeoutlen 为等待键盘快捷键连击时间500毫秒，可根据需要设置
   vim.o.timeoutlen = 500
   
   -- split window 从下边和右边出现
   vim.o.splitbelow = true
   vim.o.splitright = true
   
   -- 自动补全不自动选中(自动补全插件会用到)
   vim.g.completeopt = "menu,menuone,noselect,noinsert"
   
   -- 样式(dark/light)
   vim.o.background = "light" --dark干扰主题配置
   vim.o.termguicolors = true
   vim.opt.termguicolors = true
   
   -- 不可见字符的显示，这里只把空格显示为一个点（space:·）
   vim.o.list = true
   vim.o.listchars = "space:·"
   
   -- 补全增强
   vim.o.wildmenu = true
   
   -- 补全最多显示10行
   vim.o.pumheight = 10
   
   -- Dont' pass messages to |ins-completin menu|
   vim.o.shortmess = vim.o.shortmess .. 'c'
   
   -- 永远显示 tabline
   vim.o.showtabline = 2
   
   -- 不创建交换文件(wsl)
   vim.o.swapfile = false
   --删除交换文件(wsl)
   vim.cmd [[set noswapfile]] 
   -- 使用系统剪切板(wsl)
   vim.cmd[[set clipboard+=unnamedplus]]
   ```

6. 配置`~/.config/nvim/init.lua`

   ```lua
   require("options")
   ```

7. 新增`nvim ~/.config/nvim/lua/config/lazy.lua`:

   ```lua
   -- Bootstrap lazy.nvim
   local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
   if not (vim.uv or vim.loop).fs_stat(lazypath) then
       local lazyrepo = "https://github.com/folke/lazy.nvim.git"
       local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
       if vim.v.shell_error ~= 0 then
           vim.api.nvim_echo({
                   { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
                   { out, "WarningMsg" },
                   { "\nPress any key to exit..." },
               }, true, {})
           vim.fn.getchar()
           os.exit(1)
       end
   end
   vim.opt.rtp:prepend(lazypath)
   
   -- Make sure to setup `mapleader` and `maplocalleader` before
   -- loading lazy.nvim so that mappings are correct.
   -- This is also a good place to setup other settings (vim.opt)
   vim.g.mapleader = " "
   vim.g.maplocalleader = "\\"
   
   -- Setup lazy.nvim
   require("lazy").setup({
           spec = {
               -- import your plugins
               { "LazyVim/LazyVim", import = "lazyvim.plugins" },
               -- import/override with your plugins
               { import = "plugins" },
           },
           -- Configure any other settings here. See the documentation for more details.
           -- colorscheme that will be used when installing plugins.
           -- (改)install = { colorscheme = { "habamax" } },"tokyonight",
           install = { colorscheme = { "tokyonight" } },
           -- automatically check for plugin updates
           checker = { enabled = true },
       })
   ```

8. 在`nvim ~/.config/nvim/init.lua`中配置：

   ```lua
   require("config.lazy")
   ```

9. catppuccin主题:在`~/.config/nvim/lua/plugins/`添加主题catppuccin插件文件`catppuccin.lua`,注意禁用其他主题插件。修改一下lazy.lua配置中的插件安装主题，不再使用`tokyonight`。

   ```lua
   return{
       "catppuccin/nvim", 
       name = "catppuccin", 
       -- enabled=false(禁用插件)
       priority = 1000,
       config = function()
           vim.cmd.colorscheme "catppuccin"
           vim.o.background = "light" -- 可能options.lua中配置被覆盖了
   
       end,
       setup = {
           flavour = "auto", -- latte, frappe, macchiato, mocha
           background = { -- :h background
               light = "latte",
               dark = "mocha",
           },
           transparent_background = true, -- disables setting the background color.
       }
   }
   ```


8. 其他快捷键之类的配置：略。

> 其实配置完lazy后,去看官方文档就会发现它内置了很多插件，你只需要启用就可以了。此外文档中也介绍了如何配置neovim和搭建配置文件的目录结构。

---



##### postgresql

1. 文档：[Postgresql - Termux Wiki](https://wiki.termux.com/wiki/Postgresql)

2. 安装：

   ```bash
   # 安装
   pkg install postgresql
   
   # 建立数据库工作区文件夹
   mkdir -p $PREFIX/var/lib/postgresql
   
   # 初始化工作区
   initdb $PREFIX/var/lib/postgresql
   
   # 启动服务端:pg_ctl用于管理PgSQL服务器的控制工具，可以用它来启动、停止或重启服务器
   pg_ctl -D /data/data/com.termux/files/usr/var/lib/postgresql -l logfile start	
   
   # 关闭
   pg_ctl stop -D $PREFIX/var/lib/postgresql
   pg_ctl stop -D $PREFIX/var/lib/postgresql -m smart 		# 等待所有连接关闭后关闭(默认)
   pg_ctl stop -D $PREFIX/var/lib/postgresql -m fast		# 快速关闭服务器，取消所有未处理的事务，并强制断开所有连接。
   pg_ctl stop -D $PREFIX/var/lib/postgresql -m immediate 	# 立刻关闭服务器，终止所有进程，不等待任何操作完成。
   
   # 客户端登录
   whoami   # 获取用户名
   psql -U your_name -d postgres  # 登录
   
   psql -U $(whoami) -d postgres 
   
   
   # 修改用户密码(登陆后)
   \password
   
   
   # 退出
   \q
   ```

3. 配置远程链接

   1. 编辑配置文件:`vim $PREFIX/var/lib/postgresql/postgresql.conf`

      ```bash
      #listen_addresses = 'localhost'
      # 改为允许监听所有ip地址
      listen_addresses = '*'
      ```

   2. 编辑身份验证文件：`vim $PREFIX/var/lib/postgresql/pg_hba.conf`末尾添加如下内容：

      ```bash
      host    all             all             0.0.0.0/0               md5
      ```

   3. 重启数据库：`pg_ctl restart -D $PREFIX/var/lib/postgresql`

   4. 我这里使用idea远程连接测试：端口号默认5432

      <br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202409121335263.png" style="zoom:67%;" />

----



##### frp

1. 项目地址：[frp](https://github.com/fatedier/frp)

2. 据说是国人开发的，果然方便很多:[中文文档]([frp (gofrp.org)](https://gofrp.org/zh-cn/))

3. 在云服务器上安装好docker配置好镜像。使用`docker pull snowdreamtech/frps`命令拉去镜像。

4. 在服务器的某个文件夹创建`frps.toml`文件，这里我选择`/frps/frps.toml`:

   ```toml
   [common]
   bind_port = 7000  # frps 绑定的端口
   dashboard_port = 7500  # 控制面板的端口
   dashboard_addr = 0.0.0.0  # 控制面板可以在所有 IP 地址上访问
   dashboard_user = dream_fish  # 控制面板的用户名
   dashboard_pwd = 19450815  # 控制面板的密码
   vhost_http_port = 8888  # HTTP 虚拟主机端口
   vhost_https_port = 9999  # HTTPS 虚拟主机端口
   log_file = ./frps.log  # 日志文件路径
   log_level = info  # 日志记录级别
   log_max_days = 2  # 日志保存的天数
   authentication_timeout = 900  # 认证超时时间，单位秒
   token = 123123123  # 客户端与服务端之间的安全令牌
   max_pool_count = 50  # 代理池的最大连接数
   max_ports_per_client = 0  # 每个客户端允许的最大端口数，0 表示无限制
   token = 123456789 # 验证令牌
   ```

5. 使用如下命令创建并启动容器：其中`6005:6005`的端口映射是为了后面能访问数据库。但是实际上这种端口逐个映射很不方便，我们不采用。<font color=red>此外`7000、7500、6005`以及后续客户端使用的端口需要在用户组中开放</font>：

   ```bash
   # 一般方式
   docker run -d --name frps -p 7000:7000 -p 7500:7500  -p 6005:6005 -v /frps/frps.toml:/frp/frps.toml snowdreamtech/frps -c /frp/frps.toml
   
   # 使用主机网络：(有风险,待测试)
   docker run -d --name frps --network 3host -v /frps/frps.toml:/frp/frps.toml snowdreamtech/frps -c /frp/frps.toml
   
   # 映射端口范围:(不建议,docker崩了)
   docker run -d --name frps -p 6000-7500:6000-7500 -v /frps/frps.toml:/frp/frps.toml snowdreamtech/frps -c /frp/frps.toml
   ```

6. 客户端安装：我的是termux，选择如下版本，右键复制下载链接。

   <br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202409121516378.png" style="zoom:67%;" />

7. 安装以来并下载客户端：

   ```bash
   pkg update && pkg install tar wget		# 安装wget、tar
   
   wget <url>								# 下载frp压缩包,<url>为复制的下载链接
   
   tar -zxvf frp_xxxxx_linux_arm64.tar.gz  # 解压frp
   
   cd <frp_xxxxx_linux_arm64> 				# 进入文件夹
   ```

8. 在解压的目录中创建配置客户端配置文件`frpc.toml`:

   ```toml
   [common]
   server_addr = xxx.xxx.xxx.xxx 	# 服务端ip
   server_port = 7000 				# 服务端监听端口
   token = 123456789 				# 验证令牌
   
   [pgsql]
   type = tcp 						# 类型
   local_ip = 127.0.0.1 			# 本地ip
   local_port = 5432 				# 本地端口(这里是我的pgsql的端口)
   remote_port = 6005 				# 服务端端口
   ```

9. 启动`./frpc -c ./frpc.toml`客户端(后续可以编写一个脚本来启动)。

10. 通过`http://<server_addr>:6005`访问客户端的pgsql：<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202409121554789.png" style="zoom:67%;" />

11. 其实后续若是想将个人电脑暴露出去，或者搭建私人的远程桌面也就有了思路。





> 顺便提一嘴：之前尝试过在termux中安装docker，都失败了。最近又试了termux中安装qemu虚拟机，在qemu中安装AlpineLinux，然后在AlpineLinux中跑docker。成功了，但是虚拟机启动贼慢，并且docker也卡。当然，这些都不是问题，我正想着是不是可以将docker端口映射到虚拟机，将虚拟机端口映射到termux，将termux通过frp内网穿透暴露到公网，于是我打算将所有东西重装一遍(之前摸索的时候，有一些不必要的步骤导致系统比较乱，有洁癖)，这时候我发现我竟然无法卸载termux也无法关闭termux(一涉及到termux系统就直接卡死，原因不明)，后面重启了好几次才缓过来(不敢再装虚拟机了，想法泡汤了)。瞎搞一定要慎重啊！！！