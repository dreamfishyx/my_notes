> 最近在学习 nginx 和 docker swarm，不太想把笔记往博客上搬运，就随便写写。



##### nextchat

> 之前一直使用免费的 gpt3 (白嫖一年多)，对于平时学习赶作业基本上够。但是免费的连接不是很稳定，并且需要魔法；有时候在写实验报告，总是会写一半就断开(代码的话断开后又是续不上)，于是还是决定花钱办事。

1. 首先肯定还是需要购买 API 额度的，官方的有点贵。目前我使用的是一个 B 站 up 推荐的 [deepbricks](https://deepbricks.ai/) ,价格比较便宜，不需要配置代理，可以直接在国内使用，最重要的是可以使用支付宝和微信支付(不知道是不是个人问题，我使用 visa 卡显示不支持)。使用方法也很简单，注册登录之后，充值即可。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072204614.png" style="zoom:67%;" />

   > deepbricks 不止可以使用 chatgpt，还有 LLama、Claude等可供选择(目前正在试用 gpt4o ，后续也许会尝试其他的 api 提供商)

2. 然后创建个人的 api key :<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072234310.png" style="zoom:55%;" />

3. 之后就是下载 [nextchat](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web) ,下载合适的系统版本:<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072234426.png" style="zoom:67%;" />

4. 之后就是打开 nextchat，配置一下 api key :这里的接口地址需要填写 deepbricks 的 `https://api.deepbricks.ai` ,具体可以参考 deepbricks 使用文档，其他的一些配置就不在赘述。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072233903.png" style="zoom:67%;" />

5. 然后就可以愉快的使用 chatgpt:<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072217652.png" style="zoom:67%;" />

   > 当然其实也可以在 docker 部署，或者直接在 1panel 面板快捷部署。







##### github加速

> 之前在本地的时候，其实不太有 github 的访问问题，下载压缩包的时候都是使用油猴脚本。访问的话有一些免费的加速器 stream++(现在叫 Watt Toolkit ) 等，实在不行就使用魔法。但是后面在服务器上从 github 下载软件，才真正体会到访问超时的痛苦，真的慢。

1. 后面找到一个 github 项目，即[gh-proxy](https://github.com/hunshcn/gh-proxy),它可以利用 cloudflare(大善人)的 workers 配置 github 加速。

2. 首先还是注册登录 [cloudflare](https://dash.cloudflare.com/) (无法访问可以尝试国内版)，然后创建一个 woker，<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072243353.png" style="zoom:55%;" /><br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072255844.png" style="zoom:67%;" />

3. 将 gh-proxy 项目中的 index.js 的内容复制到 worker 中，然后点击部署即可:<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072239016.png" style="zoom:60%;" />

4. (可选)添加自定义域名:<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072251824.png" style="zoom:55%;" />

5. 后续下载 github 上的资源(包括 git ) 直接在资源路径前套一层 worker 的访问路径。假设我的域名是 dreamfish.com (未配置域名就是使用默认的 workers.dev 的 url 访问) , PREFIX前缀为/，那么:

   ```bash
   # 未使用加速:
   git clone https://github.com/xxxx/xxxx
   
   # 使用自建加速:
   git clone https://dreamfish.com/https://github.com/xxxx/xxxx
   ```

6. 当然，还可以直接访问 worker ，里面提供一个下载界面，将资源 url 粘贴上下载即可。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411072253940.png" style="zoom:67%;" />





##### docker仓库镜像代理

> 之前有一段时间，dockerhub 无法访问，大多数镜像加速也不好用，找到这个项目，搭建自己的镜像仓库加速，用到目前还是挺可以的。

1. 使用方式其实也挺简单的，首先复刻项目[CF-Workers-docker](https://github.com/cmliu/CF-Workers-docker.io?tab=readme-ov-file)到自己的 github 中。
1. 登录注册到 cloudflare 中创建一个 page ，然后导入该项目:<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411081424559.png" style="zoom:55%;" />
1. (可选)然后可以为 page 配置一个域名,后续就可以直接在 docker 中配置使用:<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411081501389.png" style="zoom:67%;" /><br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411081450201.png" style="zoom:67%;" />





##### drawio

1. [drawio](https://github.com/jgraph/drawio?tab=readme-ov-file)目前学习过程中的画图主力工具，主要是很喜欢里面的草图，有一种抽象的美。此外使用起来很方便，当然其实也有很多的web 端画图软件也很好用，只是本人用习惯。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411081434049.png" style="zoom:67%;" />
2. 若是不想安装，官方其实也提供在线使用[https://app.diagrams.net](https://app.diagrams.net/)，随时使用。





##### picgo

1.[picgo](https://github.com/Molunerfinn/PicGo)一个图片上传工具，在写笔记或者博客的时候用来上传图片，配合 github 或者 cloudflare r2 (也支持其他一些对象存储服务)搭建个人图床也是很香的。<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202411081456507.png" style="zoom:67%;" />





##### 安卓端制作系统盘

> 之前在家的重装系统的时候，系统U盘文件损坏，差点就要去售后花 100 重装系统；多亏了这个软件，我直接用手机重新制作一个系统盘。不过目前该软甲不支持 windows 系统镜像制作，可以先制作 ubuntu 镜像，然后安装成功后在 ubuntu 制制作 windows 系统盘(虽然有些麻烦，但是胜在不用跑一趟，不用花钱)。

[etchdroid](https://github.com/etchdroid/etchdroid)这个软件是安卓端的制作系统盘的软件，一般用不上，但是关键时候真的能救命。



