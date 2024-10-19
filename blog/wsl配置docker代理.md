#### 前言

1. 起因:我在搭建 cig 监控管理平台时，docker hub 中的老版本 google/cadvisor 不支持 `cgroup2`依赖的是 `cgroup v1`。于是我打算尝试最新版的`gcr.io/cadvisor/cadvisor`，但是我无法访问 gcr.io 。

2. 在此之前，需要介绍一下我之前对 wsl 的改动情况:之前在配置 wsl 的网络时，有这样一步,在C:\Users\<your_username>目录下创建一个.wslconfig文件，然后在文件中写入如下内容:具体可以参考[官方文档](https://learn.microsoft.com/zh-cn/windows/wsl/networking)

   ```toml
   [experimental]
   autoMemoryReclaim=gradual  
   networkingMode=mirrored
   dnsTunneling=true
   firewall=true
   autoProxy=true
   ```

3. 这里只是配置一下docker Daemon 的代理配置（`docker pull` 是由 dockerd 守护进程执行），其他一些代理设置，用到再说：[文档](https://docs.docker.com/engine/cli/proxy/)。此外对于docker Daemon 的代理配置，官方提供两种方式，对于配置配置文件的方式，这里未使用，参考:[文档](https://docs.docker.com/engine/daemon/proxy/)。





#### docker代理

> 我是在windows中开启代理软件，故在配置代理之前，需要解决一个重要问题，那就是 wsl 如何使用 windows 主机代理(当然也可以尝试在 wsl 中开启代理，对于linux而言 dae/daed 使用起来还不错)。



##### 方式一

1. 首先对于前言中提到的改动，启用了 `autoProxy=true`，这会导致 WSL 会自动继承 Windows 主机的代理设置,我们可以在 wsl 直接查看代理配置:

   ```bash
   echo $HTTP_PROXY
   echo $HTTPS_PROXY
   echo $NO_PROXY
   ```

2. 显然此时代理信息可以直接在环境变量中获取，这就很方便。配置`vim ~/.zshrc`( bash 则配置 `~/.bashrc`)，启动时生成 docker 代理的自定义配置文件(其实这里是一个 EnvironmentFile )，配置完成后不要忘记 `source ~/.zshrc`:你可以将自己的镜像加速排除在外。

   ```bash
   # 指定配置文件的位置: ~/.docker_proxy.env
   docker_proxy_env="$HOME/.docker_proxy.env"
   
   # 删除遗留配置文件(放置后续没有获取代理信息时沿用遗留的配置)
   rm -f ${docker_proxy_env}
   
   # 根据 windows 是否开启代理动态生成配置文件。
   if [ -n "$HTTP_PROXY" ] && [ -n "$HTTPS_PROXY" ]; then  
     echo "HTTP_PROXY=\"${HTTP_PROXY}\"" > ${docker_proxy_env}
     echo "HTTPS_PROXY=\"${HTTPS_PROXY}\"" >> ${docker_proxy_env}
     echo "NO_PROXY=\"${NO_PROXY},docker.dreamsea.top\"" >> ${docker_proxy_env}
   fi
   ```

   > 这里顺便推荐一个搭建个人 docker 镜像加速的项目:https://github.com/cmliu/CF-Workers-docker.io

3. 手动创建 Docker 的 systemd 服务配置目录(若不存在), 然后创建或编辑 `http-proxy.conf` 文件,添加如下内容:

   ```bash
   sudo mkdir -p /etc/systemd/system/docker.service.d
   
   sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
   ```

4. `http-proxy.conf` 文件内容如下(这里没有采用官方的配置 Environment 环境变量，而是使用 EnvironmentFile 提供一个环境变量配置文件):

   ```toml
   [Service]
   EnvironmentFile=- /home/fish/.docker_proxy.env
   ```

   > EnvironmentFile 使用 `-` 在目录前，作用是忽略文件不存在。这样我们就可以根据主机的代理是否启动去动态的设置 docker 的代理。

5. 在配置好代理后，你需要重新加载 systemd 配置并重启 Docker 服务，以使更改生效：

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart docker
   ```

6. 此时第一中配置方式就已经完成，使用 `docker info`来检查 Docker 是否已经使用了代理：

   ```bash
   $ docker info
   Client:
    Version:    27.3.1
    Context:    default
    Debug Mode: false
    Plugins:
     compose: Docker Compose (Docker Inc.)
       Version:  2.29.7
       Path:     /usr/lib/docker/cli-plugins/docker-compose
   
   Server:
    ...
    HTTP Proxy: http://127.0.0.1:10809
    HTTPS Proxy: http://127.0.0.1:10809
    ...
   ```

   > 我在写这篇博客时发现一个盲点，那就是若是 docker 的启动顺序 在我的 zsh(或者bash) 之前, 那么就会导致 docker 读取到遗留的配置文件，或者说读不到配置文件，这样就会导致代理配置错误:
   >
   > 1. 对此,chatgpt 提出几种解决措施:
   >
   >    1. 使用 `After`指令: 在 Docker 的 systemd 服务文件中，添加 `After=graphical.target` 或 `After=multi-user.target`，确保 Docker 在图形用户界面或多用户环境准备好后启动。
   >    2. 使用 `ExecStartPost`: 在 Docker 的服务文件中使用 `ExecStartPost`，执行一个脚本，确保用户的 shell 环境已经加载。
   >    3. 延迟启动 Docker: 可以创建一个系统服务，使用 `systemd` 的定时功能，延迟 Docker 启动。例如，使用 `WantedBy` 指定到某个目标下，并设置延迟启动。
   >    4. 手动控制启动： 在用户的 shell 配置文件（如 `~/.bashrc` 或 `~/.zshrc`）中添加命令，在登录后手动启动 Docker,运行`systemctl start docker` 来实现。
   >
   > 2. 先不着急行动，手动删除当前生成的docker自定义配置文件，(开启 windows 代理)然后关闭 wsl ，再启动 wsl 。使用 `docker info` 发现已经配置代理信息。也就是说 docker 的启动顺序在 zsh/bash 之后。
   >
   > 3. 以我目前的能力还很难去研究其具体的启动顺序,我们使用 `systemd-analyze blame` 大致看一下启动时间，发现` docker.service`在 `user@1000.service` 之后启动的。
   >
   >    ```bash
   >    $ systemd-analyze blame
   >    2min 159ms systemd-networkd-wait-online.service
   >         685ms docker.service
   >         398ms dev-sdc.device
   >         269ms systemd-resolved.service
   >         254ms user@1000.service
   >         196ms containerd.service
   >         144ms docker.socket
   >         133ms systemd-networkd.service
   >         127ms systemd-tmpfiles-setup-dev-early.service
   >         101ms systemd-logind.service
   >         ...
   >    ```
   >
   > 4. 这里的启动时间有时间再研究，待补。
   >
   > 5. docker 的系统服务文件位置 `/lib/systemd/system/docker.service`，若是存在启动问题，可参考上述内容。
   >
   > 6. 关于系统服务配置: 可以参考一下[博客](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)





##### 方式二

1. 至于第二种配置方式(懒得配置测试，理论上可行，细节上可能会存在一些问题)，根据[官方文档](https://learn.microsoft.com/zh-cn/windows/wsl/networking):,我们可以直接通过`ip route show | grep -i default | awk '{ print $3}'` 获取到 windows 的 ip地址。

2. 那么接下来就很简单(同上):配置`vim ~/.zshrc`( bash 则配置 `~/.bashrc`)，启动时生成 docker 代理的自定义配置文件(其实这里是一个 EnvironmentFile )，配置完成后不要忘记 `source ~/.zshrc`:你可以将自己的镜像加速排除在外。

   ```bash
   # 指定配置文件的位置: ~/.docker_proxy.env
   docker_proxy_env="$HOME/.docker_proxy.env"
   
   # 获取 windows 的 ip 地址
   proxy_ip=$(ip route show | grep -i default | awk 'NR==2 {print $3}')
   
   # 删除遗留配置文件(放置后续没有获取代理信息时沿用遗留的配置)
   rm -f ${docker_proxy_env}
   
   # 这里的端口需要根据你的代理软件配置
   echo "HTTP_PROXY=\"${proxy_ip}:10808\"" > ${docker_proxy_env}
   echo "HTTPS_PROXY=\"${proxy_ip}:10809\"" >> ${docker_proxy_env}
   echo "NO_PROXY=\"localhost,127.0.0.1,<docker镜像加速地址>\"" >> ${docker_proxy_env}
   ```

3. 手动创建 Docker 的 systemd 服务配置目录(若不存在), 然后创建或编辑 `http-proxy.conf` 文件,添加如下内容:

   ```bash
   sudo mkdir -p /etc/systemd/system/docker.service.d
   
   sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
   ```

4. `http-proxy.conf` 文件内容如下(这里没有采用官方的配置 Environment 环境变量，而是使用 EnvironmentFile 提供一个环境变量配置文件):

   ```toml
   [Service]
   EnvironmentFile=- /home/fish/.docker_proxy.env
   ```

   > EnvironmentFile 使用 `-` 在目录前，作用是忽略文件不存在。这样我们就可以根据主机的代理是否启动去动态的设置 docker 的代理。

5. 在配置好代理后，你需要重新加载 systemd 配置并重启 Docker 服务，以使更改生效：

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart docker
   ```

6. 此时第一中配置方式就已经完成，使用 `docker info`来检查 Docker 是否已经使用了代理，这种配置方式无法根据 windows 是否配置代理来动态设置 docker 代理。
