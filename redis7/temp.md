主从复制，是否需要开启 aof、rdb???

config set设置主机密码。

![image-20250228140255937](./assets/image-20250228140255937.png)

![image-20250228142237971](./assets/image-20250228142237971.png)

![image-20250228142507599](./assets/image-20250228142507599.png)

哨兵不光改master配置，也要改slave配置告诉新master是谁，强烈建议实验前先备份conf，以便恢复
