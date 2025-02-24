> 关于 git 使用部分的笔记实际在语雀上，暂时不打算迁移。这篇笔记主要是在 git 基础上进一步记录一些使用过程中遇到的问题。



#### 合并

##### fetch和pull

| 命令        | 作用                                                      | 是否修改本地代码 | 典型使用场景                 |
| ----------- | --------------------------------------------------------- | ---------------- | ---------------------------- |
| `git fetch` | 仅从远程仓库下载最新提交记录，不自动合并到本地分支。      | 否               | 查看远程更新内容，暂不合并。 |
| `git pull`  | `git fetch` + `git merge`(默认)，即下载并自动合并到本地。 | 是               | 快速同步远程更新到本地。     |

```bash
# 查看远程更新但不修改本地代码
git fetch origin

# 查看远程分支和本地分支的差异（假设远程分支为 origin/main）
git log main..origin/main

# 确认无误后手动合并
git merge origin/main
```





##### rebase和no-rebase

两个选项用于控制 git pull 的合并策略：

| 选项        | 作用                                               | 提交历史效果     | 适用场景                           |
| ----------- | -------------------------------------------------- | ---------------- | ---------------------------------- |
| --rebase    | 将本地提交“变基”到远程最新提交之后，保持线性历史。 | 干净、线性       | 个人分支、希望历史整洁时使用。     |
| --no-rebase | 使用默认的合并策略（merge），生成一个合并提交。    | 保留分支合并痕迹 | 团队协作、需要明确合并记录时使用。 |

```bash
# 使用 rebase 方式拉取并合并（推荐个人使用）
git pull --rebase origin main

# 使用默认的 merge 方式拉取并合并
git pull --no-rebase origin main
```

为了更好地理解上述过程，我们不妨举个例子，假设我们存在下面这样一个情况:本地和远程分别基于 A 节点进行修改得到 B 、X 。

```bash
   本地提交 B
   /
A → 远程提交 X
```

`--rebase`将本地提交“嫁接”到远程最新提交之后,形成如下线性分支结构：

```bash
A → X → B'（B 的哈希值改变，将本地提交 B 的修改重新应用到 X 之后，生成新提交 B'）
```

`--no-rebase`保留本地和远程的分叉历史，生成一个合并提交的节点：

```bash
     B → Merge Commit
    /          ↗
A → X
```

无论哪种方式，修改记录都不会丢失，并且需要注意的是这是在本地进行合并，最后结果还是需要上述到远程仓库。后续的 git rabase 操作应该也是这样理解的。





##### pull合并策略

1. git pull 的默认合并策略取决于 Git 配置中的 pull.rebase：

   1. `pull.rebase = false`即 `git pull = git fetch + git merge`(default)
   2. `pull.rebase = true`即`git pull = git fetch + git rebase`

2. 修改默认策略：

   ```bash
   # 设置全局默认使用 rebase
   git config --global pull.rebase true
   
   # 恢复为默认的 merge
   git config --global pull.rebase false
   ```





##### 对比

| 场景             | `git fetch`            | `git pull`（默认 merge）       | `git pull --rebase`          |
| ---------------- | ---------------------- | ------------------------------ | ---------------------------- |
| **同步远程更新** | 仅下载，不修改本地代码 | 下载并自动合并（生成合并提交） | 下载并变基（线性历史）       |
| **提交历史效果** | 无影响                 | 保留分支合并痕迹               | 历史线性，无额外合并提交     |
| **冲突处理**     | 无冲突                 | 合并时可能需解决冲突           | 变基时可能需逐提交解决冲突   |
| **适用场景**     | 需先审查远程更新再合并 | 团队协作分支                   | 个人分支或希望历史整洁的情况 |

我们假设本地和远程分支均有新提交，使用 `git pull --rebase`时：

```bash
git pull --rebase origin main

# 若有冲突：
git add .
git rebase --continue # 继续 rebase 
git push origin main
```

> **效果**：本地提交“附加”到远程提交之后，历史为一条直线。

使用 `git pull --no-rebase`时：

```bash
git pull origin main

# 若有冲突：
git add .
git commit -m "合并冲突"
git push origin main
```

> **效果**：生成一个合并提交，保留分支历史。





##### 注意事项

1. `git rebase` 风险：
   - 会重写提交历史，公共分支（如团队主分支）慎用。
   - 若已推送过本地提交，强制推送（`git push -f`）可能影响他人。
2. `git merge` 优点：保留完整合并记录，适合需要追踪协作历史的场景。
3. 优先使用 `git fetch`：先通过 `git fetch` 查看远程更新，再决定是否合并或变基，更安全。

> - `git fetch`：只下载，不合并。
> - `git pull`：下载 + 合并（默认用 `merge`）。
> - `--rebase`：合并时“改写历史”保持线性。
> - `--no-rebase`：合并时保留分支痕迹。
>
> 根据需求选择策略，个人分支推荐 `rebase`，团队分支建议 `merge`(其实按照上述描述就相当于 `--no-rebase`)