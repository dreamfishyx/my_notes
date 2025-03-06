##### 前言

1. 最近在学习 redis，由于电脑性能问题，没有采用虚拟机搭建，而是使用 wsl 的 docker 搭建，进而在搭建包括后期使用 springboot 连接过程中出现一些问题。因此稍微记录一下。
2. 主要是记录一下踩的坑，redis 哨兵，集群搭建过程不完整叙述。
3. 懒得写docker compose 的文件，所以直接搭建。



##### redis单机

1. redis 配置文件中 `daemonize` 参数改回 `no` ,不然会与 docker 容器启动参数 `-d` 冲突导致容器无法启动。
2. `Failed to write PID file: Permission denied`：Redis 无法写入 PID 文件，可能是权限问题。使用参数`--privileged=true`启动容器，容器内的进程几乎拥有与宿主机 root 用户相同的权限。



##### 搭建哨兵

1. 不要使用容器名作为 ip 指定 master容器:最初搭建哨兵+主从复制集群的过程中，为了方便连接，我构建一个新的 docker 网络。各个 slave 通过 master 容器名访问 master，但是当 master 宕机后，容器名就无法解析，此时哨兵会报错，甚至在故障转移时会出现一些问题。解决方式:
   1. 使用 host 网络(推荐)。
   2. 使用静态 ip 启动容器。
2. 不要直接挂载配置文件，改为挂载配置文件目录:在故障转移时，哨兵需要重新修改 redis 配置文件，此时可能会报`Could not rename tmp config file (Device or resource busy)` 错误。关于这一点的解释 deepseek的解释是:当容器内的 redis 进程尝试修改配置文件时，会生成一个临时配置文件,然后通过 `rename()` 系统调用将临时配置文件重命名为原配置文件，以实现原子性更新。如果宿主机上的原配置文件被直接挂载到容器内，则 `rename()` 操作会直接作用于宿主机的文件系统。某些文件系统或挂载方式会限制对挂载文件的 `rename` 操作，导致错误。
3. `Could not create tmp config file (Permission denied), CONFIG REWRITE failed: Permission denied`错误：主机运行` sudo chmod -R 777 <config_dir>` 赋予对配置文件所在目录读写权限。
4. `Failed to resolve hostname`:哨兵默认关闭主机名解析，此时无法通过容器名访问 master，需要使用配置`sentinel resolve-hostnames yes`开启主机名解析。但是前面提了，不建议使用容器名 。





##### 集群

> 关于springboot配置部分目前还是猜测，尝试过调试但是一直在不同线程之间切换，绕晕了!!!

1. 目前不知道为啥，我在 springboot 中 配置 redis 集群各节点的 ip ，但是 springboot 似乎连接到一个节点上后会获取改节点维护的集群节点的ip，然后按照这些 ip 访问集群中的节点。它的流程似乎是:Spring Boot → 连接 localhost:6379 → Redis 节点返回集群拓扑(含172.18.43.141:xxx） → Lettuce 尝试连接 172.18.43.141 → 超时<br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202503061558980.png" alt="image-20250306143048550" style="zoom:67%;" /><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202503061558665.png" alt="image-20250306142933558" style="zoom:80%;" />

2. 若是同样在 wsl 的 docker 中搭建 redis 集群，不建议使用静态 ip 。若是使用自建网络的静态 ip，这导致 redis 集群中维护的各节点的 ip 都是容器内部的，后面再window上访问不到这些 ip ，无法在springboot 中连接。

3. 先说明一下我的一些配置改动情况:

   1. 我曾经为了 wsl 能够直接使用主机代理，做过一下配置:C:\Users\<your_username>目录下创建一个.wslconfig文件，然后在文件中写入如下内容。而我此时所有的不幸就归功于这个 mirrored 模式,mirrored网络模式意味着 wsl 子系统的网络接口与宿主机的网络接口完全一致，虚拟机和宿主机共享相同的 IP 地址。这可能会导致 IP 地址冲突或网络层面的混乱。

      ```bash
      [experimental]
      autoMemoryReclaim=gradual  
      networkingMode=mirrored
      dnsTunneling=true
      firewall=true
      autoProxy=true
      ```

      <br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202503061558889.png" alt="image-20250306153449650" style="zoom:67%;" /><br><img src="https://raw.githubusercontent.com/dreamfishyx/pictures/main/pic/202503061558156.png" alt="image-20250306153556755" style="zoom:80%;" />

   2. 最简单的验证方式就是，我在 docker 中启动单个 redis 实例，使用 idea 中的数据库连接工具，使用 local时可以连接，但是使用 wsl 的 ip 时连接不上。上述配置似乎导致 windows 中访问 wsl 无法通过 ip (二者 ip 一致，但是在windows 中，会认为是本机，最简单的验证方式就是在 windows 中使用 shh 远程连接 wsl)，而是使用 127.0.0.1 或者localhost。

4. 还是推荐使用 host 网络搭建，这里就有一些情况:

   1. 若是 wsl 开启 mirrored 模式，则搭建集群时使用 127.0.0.1 ，springboot连接时使用 127.0.0.1 。
   2. wsl 关闭 mirrored 模式改用默认 NAT 模式，则搭建集群时使用 wsl 的 ip ，springboot连接时使用 wsl 的 ip 。
