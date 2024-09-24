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

   1. 进入本地存放代码的目录删除`.git`隐藏目录
   2. 执行`git init`命令初始化本地目录为一个git仓库
   3. 执行`git add -A`命令添加本地代码到仓库

   6. 执行`git commit`命令提交本地代码到仓库
   7. 执行`git push -f`命令强制提交到远程仓库