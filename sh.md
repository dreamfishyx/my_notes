#### 自动上传脚本

```bash
#! /bin/bash

log_file=~/work_hub/cmd/log/auto_save.log
dir=$(dirname "${log_file}")

if [ ! -e "$dir" ]; then
  echo "${dir} not exist,creating..."
  mkdir -p "$dir"
fi

if [ ! -e "$log_file" ]; then
  echo "${log_file} not exist,creating..."
  touch "$log_file"
fi

time=$(date "+%Y-%m/%d %H:%M:%S")
echo "${time} auto_save executed" >>$log_file

cd /home/fish/ || exit
cd ./work_hub/my_notes/ || exit
git add .
git commit -m "archlinux auto save"
git push
```



---

##### 删除git历史

1. 方法一：

   1. 切换到新分支：`git checkout --orphan latest`
   2. 缓存所有文件：`git add -A`
   3. 提交跟踪过的文件：`git commit -m "new"`

   4. 删除master分支:`git branch -D master`

   5. 重命名当前分支为master:`git branch -m master`

   6. 提交到远程master分支:`git push -f origin master`

2. 方式二：

   1. 进入本地仓库删除`.git`目录。
   2. `git init`命令初始化本地仓库。
   3. `git add -A`命令添加本地代码到仓库。

   4. `git commit`提交。
   5. `git push -f <url> master`强制提交到远程仓库。

---

##### error: RPC failed; curl 92 HTTP/2 stream 5 was not closed cleanly: CANCEL (err 8)

1. 增大Git缓冲区: 你可以尝试增加Git的HTTP缓冲区大小，运行以下命令：`git config --global http.postBuffer 524288000`
2. 分段推送: 如果你的提交包含大量文件或大文件，考虑分多次提交。可以使用以下命令将某些更改推送到远程：`git push origin master --force-with-lease`





> 待补：
>
> git config --global http.version HTTP/2
>
> git config --global http.version HTTP/1.1


