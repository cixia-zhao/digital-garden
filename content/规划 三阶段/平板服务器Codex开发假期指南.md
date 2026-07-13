# 平板 + 服务器 + Codex 假期开发指南

> 最后核对：2026-07-13
>
> 这是一份给“我能照着做，但不想先学完一堆 Linux”的使用指南。前半部分可以直接照抄；后半部分是给未来的你、或 AI 助手查阅的技术说明。

> 假期只带平板时：同一份指南已放在服务器 `~/tablet-codex-guide.md`。登录服务器后，可用 `sed -n '1,160p' ~/tablet-codex-guide.md` 先看前 160 行；要继续看就把范围换成 `161,320p`。不需要返回电脑才能查看。

---

## 第一部分：最常用、最重要的操作

### 先记住这张关系图

```text
安卓平板上的 Termux
        │ SSH
        ▼
阿里云服务器（真正干活的地方）
  ├─ Codex CLI
  ├─ Git / GitHub
  ├─ Python、Node、npm、项目依赖
  ├─ 服务器本机代理
  └─ tmux：断线后仍保留的开发窗口
```

**平板只是遥控器；真正下载、跑测试、让 Codex 读代码的都是服务器。**

因此，平板通常不用开代理。只要平板能 SSH 连上服务器，服务器里的 Codex、Git、npm、pip 已经会走服务器本机代理。

### 现在的服务器已经有什么

| 内容 | 当前状态 | 你需要怎么理解 |
|---|---|---|
| 阿里云服务器 | Ubuntu 24.04，2 核、约 1.6GB 内存 | 是一台一直开着的远程 Linux 电脑。 |
| Swap | 2GB，已启用 | 内存不够时的缓冲；不能把它当成真正的大内存。 |
| 开发账户 | `codexdev` | 以后日常开发只用它，不用 `root`。 |
| Codex CLI | 已登录 ChatGPT | 进入服务器后可直接运行 `codex`。 |
| 开发会话 | `tablet-dev` | 用 `tmux` 保持；断网后回来还能继续。 |
| 服务器代理 | Mihomo，已开机自启 | 只监听服务器自己，地址是 `127.0.0.1:7897`。 |
| `daily plan` 开发副本 | `/srv/workspaces/daily-plan` | 可以改、可以测试、可以 Git 提交。 |
| `xitong` 开发副本 | `/srv/workspaces/xitong` | 可以改、可以测试、可以 Git 提交。 |
| `daily plan` 生产版本 | `/opt/daily-plan/current` | **绝对不要在这里开发。** |

### 你每次开发只做这几步

#### 第 0 步：平板首次准备（只做一次）

在 Termux 安装基本工具：

```sh
pkg update
pkg install openssh git
```

看到很多镜像后面写着 `bad` 不代表失败。Termux 会先测速，再自动选一个可用镜像；只要后面出现下载进度、`Setting up openssh`、`Setting up git`，最后又回到：

```text
~ $
```

就说明安装成功了。你这次的截图正是成功状态，不需要重装。

截图中关于 `ssh-agent`、`termux-services`、`sshd` 的英文提示可以先忽略：它说的是“让平板自己当 SSH 服务器”。我们现在需要的是“平板 SSH 连接阿里云服务器”，不需要在平板开启 `sshd`，也不需要安装 `termux-services`。

如果想自己核对，运行：

```sh
ssh -V
git --version
```

创建平板自己的 SSH 钥匙：

```sh
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub
```

把最后一条命令显示的整行公钥发给 Codex 或保存好，让它加入服务器。**只发 `.pub` 公钥，绝不发送私钥。**

> 2026-07-13 已将当前平板公钥加入服务器的 `codexdev` 登录白名单。以后换平板或重新生成钥匙时，才需要重新做这一小步。

#### 第 1 步：从平板进入服务器

平板公钥加入后，在 Termux 输入：

```sh
ssh codexdev@120.55.53.215
```

第一次连接可能询问是否信任服务器，输入：

```text
yes
```

成功后看到类似下面的提示符，就已经进了服务器：

```text
codexdev@iZbp1caypnj28to5iunrhqZ:~$
```

#### 第 2 步：回到持续开发窗口

```sh
tmux attach -t tablet-dev
```

进入后请使用名为 `dev` 的窗口。这个窗口已带好服务器代理环境。

常用 tmux 按键：

| 目的 | 按键 |
|---|---|
| 暂时离开、但不关开发任务 | `Ctrl-b`，松开后按 `d` |
| 新建窗口 | `Ctrl-b`，松开后按 `c` |
| 下一个窗口 | `Ctrl-b`，松开后按 `n` |
| 上一个窗口 | `Ctrl-b`，松开后按 `p` |
| 查看窗口列表 | `Ctrl-b`，松开后按 `w` |

手机或平板断网时，**不要着急重开 Codex**。重新 SSH 后再次运行：

```sh
tmux attach -t tablet-dev
```

通常原来的 Codex 对话、测试和命令还在。

#### 第 3 步：选择项目，启动 Codex

开发 `daily plan`：

```sh
cd /srv/workspaces/daily-plan
codex
```

开发 `xitong`：

```sh
cd /srv/workspaces/xitong
codex
```

进入 Codex 后，第一句话可以直接复制：

```text
请先阅读 README.md、HANDOFF.md 和 docs/README.md，确认当前项目状态后再开始修改。先说明你理解的需求和准备改动的范围；不要修改生产服务器目录或服务配置。
```

### 服务器代理怎么用

你不需要背代理地址，也不需要开 TUN。运行：

```sh
proxyctl
```

它会给你一个小菜单：

1. 查看当前节点和分组
2. 切换手动节点
3. 测试 GitHub 是否能连通

日常最有用的是切换 `一元机场` 这个手动分组。`自动选择` 与 `故障转移` 会按节点健康状态自行选择，不需要手改。

> 服务器代理与电脑 Clash 使用的是当前相同的节点和规则副本，但它们是两份独立运行的程序。你在电脑界面切换节点，不会自动同步到服务器。

### 保存代码：每次完成一个小功能后做这四步

先确认自己位于正确项目目录，例如：

```sh
cd /srv/workspaces/daily-plan
git status
```

确认没有看不懂的改动后：

```sh
git add -A
git commit -m "用中文写一句这次做了什么"
git push
```

如果这是服务器第一次推送，GitHub 可能要求你先完成 Git 身份和授权。**不要把 GitHub 密码、令牌或私钥发到聊天里。**遇到这一步就停下，把终端提示复制给 Codex 处理。

### Codex CLI 专用教程：像用桌面版一样开发

这一节只讲你平板上眼前这个黑色界面。先记住：**黑色界面分两层。**

```text
普通终端（提示符通常是 codexdev@...:~$）
  └─ 你在这里输入 cd、git、tmux、codex 等命令

Codex 对话界面（顶部写 OpenAI Codex，底部有 > 输入框）
  └─ 你在这里直接用中文与 Codex 对话、让它读文件和改代码
```

**先看你所在的位置，再输入命令。这是最容易混淆、也最重要的一条：**

| 屏幕上看到的提示 | 你实际在哪里 | 这里只能做什么 | 不要在这里输入什么 |
|---|---|---|---|
| `~ $` | 平板本地 Termux，说明还没进服务器，或 SSH 已断开 | `ssh codexdev@120.55.53.215`、`pkg`、平板钥匙命令 | `/model`、`codex`、`codex resume --all` |
| `codexdev@iZbp...:~$` | 服务器的普通终端 | `cd`、`tmux`、`git`、`codex`、`codex resume --all` | `/model` 这类斜杠命令 |
| 顶部有 `OpenAI Codex`，底部是 `>` 输入框 | Codex 对话界面 | 中文需求、`/model`、`/usage`、`/compact`、`/help` | `ssh`、`tmux attach` 这类终端命令 |

例如，看到 `~ $` 时，**唯一正确的下一步通常是：**

```sh
ssh codexdev@120.55.53.215
```

重新看到 `codexdev@...$` 后才输入：

```sh
tmux attach -t tablet-dev
```

而 `/model` 必须等你重新看到 `OpenAI Codex` 和 `>` 输入框后再输入。

看到顶部类似下面这三行，说明你已经在 Codex 对话界面：

```text
OpenAI Codex (v0.144.1)
model: gpt-5.5       /model to change
directory: /srv/workspaces/daily-plan
```

其中 `directory:` 最重要：它就是 Codex 当前能正常开发的项目。截图里是 `/srv/workspaces/daily-plan`，因此现在是在开发 `daily plan`，没有进错地方。

#### A. 第一次进入、开始一个新话题

先确认自己在普通终端，而不是 Codex 对话输入框。然后照抄一行：

```sh
cd /srv/workspaces/daily-plan && codex
```

开发 xitong 时改为：

```sh
cd /srv/workspaces/xitong && codex
```

进入后，点一下屏幕中间或底部以 `>` 开头的输入框，输入中文需求，最后按手机键盘的“回车/发送”。例如：

```text
我想修改今天的任务编辑流程。请先阅读 README.md、HANDOFF.md 和相关前端代码，不要修改，先用中文告诉我现状、可能涉及的文件和建议方案。
```

这一步相当于桌面版里“打开项目后，在聊天框发第一条消息”。你不需要先手动打开所有文件；先让 Codex 读，它会自己在服务器项目中查找。

#### B. 最常用的四件事：可以直接输入

下表中的内容都应在 **Codex 的 `>` 输入框** 中输入，不是在 `codexdev@...$` 提示符后输入。

| 你要做什么 | 直接输入 | 接下来怎么做 |
|---|---|---|
| 查看本版本所有可用菜单 | `/help` | 先看列表；版本升级后以这里显示的为准。 |
| 切换模型 | `/model` | 出现模型列表后，用平板的 `↑`、`↓` 选择，按回车确认。不要手输模型内部名称。 |
| 查看本账号剩余用量/重置机会 | `/usage` | 只查看，不会消耗或重置用量。 |
| 减少长对话占用、保留摘要后继续 | `/compact` | 适合已经聊很久、Codex 开始忘记前文或反应变慢时用。 |
| 新开一个空白话题、但仍在同一项目 | `/new` | 新话题不再自动记得上一段的细节；重要背景要重新说明或让它读文档。 |
| 结束 Codex，回到普通终端 | `/exit` | 之后能继续用 `codex resume --all` 找回该对话。 |

关于模型切换，最稳妥的操作是：

```text
/model
```

然后按下面做：

1. 等待列表出现；不要着急重复发送。
2. 点击 Termux 底部的 `↑` 或 `↓`（也可以用外接键盘方向键）移动高亮。
3. 选中后按键盘回车。
4. 看顶部的 `model:` 是否变成你选的名称。

模型列表只会显示你的当前账号可用的模型。**不知道怎么选时保持默认模型即可。**切模型只影响此后的回答，不会删除项目、对话、Git 记录，也不需要重新登录。

> 若某个 `/命令` 提示不存在：先输入 `/help`，不要猜命令、更不要改配置文件。不同 Codex 版本可用命令会略有不同；本指南只把日常最重要的写死。

#### C. 在 CLI 中“打开文件”和“看项目”

没有桌面文件树并不代表不能看文件。你有两种简单方式：

**方式 1：直接叫 Codex 阅读（最推荐）**

```text
请先阅读 README.md。
```

如果你已经知道文件名，也可以在对话输入框中用 `@`：

```text
请阅读 @README.md，并用三句话告诉我这个项目目前已经实现什么、还没实现什么。
```

同一次可以继续点名别的文件：

```text
再阅读 @HANDOFF.md 和 @docs/README.md。不要改代码，只告诉我这三个文件是否有互相矛盾的地方。
```

**方式 2：回到普通终端自己看（适合只想核对）**

先用 `/exit` 回到 `codexdev@...$`，然后复制下面任意一条：

```sh
pwd
```

```sh
rg --files
```

```sh
sed -n '1,160p' README.md
```

```sh
git status
```

这些命令都只读，不会改文件。`pwd` 看当前位置，`rg --files` 列出文件，`sed -n '1,160p' README.md` 看 README 前 160 行，`git status` 看是否有未提交修改。

#### D. 让 Codex 正确做事的提问方式

不要只输入“帮我优化一下”或“这里不对”。平板开发时，照下面的顺序说，效果最接近桌面版协作：

**第一句：只调查，不修改。**

```text
我想做【把这里换成你的目标】。请先只阅读相关文件，告诉我：当前逻辑在哪里、准备改哪些文件、风险是什么、怎样测试。先不要修改。
```

**第二句：确认后再实现。**

```text
方案可以。请只按刚才确认的范围实现；不要碰 /opt/daily-plan/current、生产数据库、服务配置或其他项目；改完运行相关测试，但不要提交或推送。
```

**第三句：要结果而不是猜结果。**

```text
请用中文汇报：改了哪些文件、每个文件改了什么、运行了哪些测试及结果、还有什么风险。然后给我 git diff 摘要，先不要提交。
```

**最后才提交代码。** 退出 Codex 后，在普通终端逐条输入：

```sh
git status
```

```sh
git diff --stat
```

```sh
git add -A
```

```sh
git commit -m "用中文写清本次完成的功能"
```

```sh
git push
```

前三条是检查和暂存；最后两条才会写入 Git 历史并上传 GitHub。对改动感到不确定时，**停在 `git diff --stat`，不要继续提交。**

#### E. 权限弹窗、命令确认与“该不该同意”

Codex 有时会显示它准备执行的命令并请求你确认。你按这个判断：

| 看到的操作 | 通常是否可以同意 |
|---|---|
| 在 `/srv/workspaces/daily-plan` 或 `/srv/workspaces/xitong` 中读取文件、运行测试、安装项目依赖 | 可以先看命令和路径，确认项目目录正确后同意。 |
| `git status`、`git diff`、`pytest`、`npm test`、`npm run build` | 正常开发检查，可以同意。 |
| `git commit`、`git push` | 只有你已经看过改动并明确决定保存/上传时才同意。 |
| 出现 `sudo`、`systemctl`、`/opt/daily-plan`、`/var/lib/daily-plan`、`/etc/daily-plan`、`rm -rf` | 不要同意，选择拒绝，并把提示发给 Codex。 |

不确定时可以直接对 Codex 输入：

```text
先不要执行这条命令。请解释它会修改哪里、能否回退、为什么这一步必要。
```

#### F. 断线、退出和找回对话

平板断网时，不要重复启动 Codex。正确顺序是：

```sh
ssh codexdev@120.55.53.215
```

```sh
tmux attach -t tablet-dev
```

如果你又看见原来的 Codex 界面，说明对话还在，直接继续输入即可。

如果你已经用 `/exit` 结束了 Codex，想找历史对话，要先决定“这次恢复后准备在哪个服务器项目里工作”。历史列表和项目代码是两件事：**历史对话可以来自任何旧电脑项目；但 Codex 实际读写的代码，必须明确指定为服务器上的项目目录。**

恢复 `daily plan` 对话时输入：

```sh
codex resume --all -C /srv/workspaces/daily-plan
```

恢复 `xitong` 对话时输入：

```sh
codex resume --all -C /srv/workspaces/xitong
```

`--all` 的意思是“把所有历史对话都列出来”，不是“把所有项目都打开”。`-C` 后面的路径才决定这次恢复的对话要在**哪个服务器项目**中工作。

列表出现后，用 `↑`、`↓` 选中以前的对话，按回车恢复。只选择与当前项目相符的记录：

| 历史列表中的来源/标题 | 可以怎样处理 |
|---|---|
| 电脑上 `daily plan` 文件夹下的旧对话 | 用第一条 `daily-plan` 命令恢复，可以继续开发。 |
| 电脑上 `错题` / xitong 相关旧对话 | 用第二条 `xitong` 命令恢复。 |
| `远程开发`、`algorithm code` 或服务器尚未部署的其他项目对话 | 可以恢复后阅读聊天内容，但不要让它执行旧 Windows 路径或修改代码；这次服务器没有对应项目副本。 |

恢复一段桌面时期的对话后，第一句话固定发送：

```text
现在我是在服务器上的 /srv/workspaces/daily-plan 开发。请不要使用旧电脑路径；先检查当前目录和 Git 状态，再继续我们原来的讨论。
```

> 2026-07-13 已把本机桌面 Codex 的 **26 份会话记录**导入服务器。它们会以终端列表的形式出现在 `codex resume --all` 中，不会像桌面版那样显示成可点击的项目卡片。迁移只包含对话和标题索引；**没有复制**电脑的项目代码、登录凭据、插件、代理设置、日志数据库或其他本机配置，因此不会影响服务器已经可用的 Codex 登录和开发环境。

#### G. 你每天真正要记住的最短流程

```sh
ssh codexdev@120.55.53.215
tmux attach -t tablet-dev
cd /srv/workspaces/daily-plan
git pull --ff-only
git status
codex
```

进入后先发：

```text
请先阅读 README.md、HANDOFF.md 和 docs/README.md。先只说明当前状态和你建议的下一步，不要修改。
```

### 把平板 CLI 当成桌面版来用

桌面版的 Codex 是“有项目卡片、文件区和历史列表的图形界面”；平板上的 Codex CLI 是“在某个项目文件夹里开一段对话”。**它们可以登录同一个 Codex / ChatGPT 账号；平板模式下，开发工作实际在服务器完成，只是你用文字命令代替了点击。**

| 桌面版里你会做的事 | 平板 CLI 对应做法 |
|---|---|
| 点开一个项目 | `cd` 到项目目录后运行 `codex` |
| 看自己在哪个项目 | 终端输入 `pwd`；或看 Codex 顶部的 `directory:` |
| 看文件树 | 输入 `rg --files`；文件太多时按扩展名缩小，例如 `rg --files -g '*.py'` |
| 打开并读一个文件 | 输入 `sed -n '1,160p' README.md`；或在 Codex 对话里写“请阅读 `README.md`” |
| 告诉 Codex 关注某个文件 | 在输入框写 `@README.md`，再补充你的问题；也可直接写文件名和需求 |
| 新开一段对话 | 在 Codex 输入 `/new`；若要回到终端，输入 `/exit` 后再运行 `codex` |
| 找回旧对话 | 运行 `codex resume --all -C /srv/workspaces/daily-plan`（或换成 xitong 路径），从列表中选择 |
| 临时离开、保留当前对话 | `Ctrl-b`，松开后按 `d`；回来后 `tmux attach -t tablet-dev` |

Termux 底部有一个 `CTRL` 虚拟按键：需要 `Ctrl-b` 时，先点一下 `CTRL`，再按字母 `b`，松开后再按下一颗字母（例如 `d`）。这不是关闭 Codex，而是 tmux 的快捷键。

#### 先分清三个“项目位置”

| 你想做什么 | 要进入的目录 | 绝不能混用的地方 |
|---|---|---|
| 开发日程应用 | `/srv/workspaces/daily-plan` | 不要去 `/opt/daily-plan/current` |
| 开发 xitong | `/srv/workspaces/xitong` | 不要用生产目录或生产数据库 |
| 只想看看服务器家目录 | `cd ~` | 这里不是项目，不要在这里运行 Codex 开始开发 |

每次准备开发时，先照抄这一组：

```sh
cd /srv/workspaces/daily-plan   # 如果你要做 daily plan
git pull --ff-only
git status
codex
```

做 `xitong` 时，只把第一行换成：

```sh
cd /srv/workspaces/xitong
```

`git pull --ff-only` 的意思是：只在没有冲突时把 GitHub 上已经存在的代码拿下来；它比直接 `git pull` 更保守。如果它报错，不要强行输入别的 Git 命令，把报错发给 Codex。

#### 账号、登录和权限：你只需要记住这些

| 项目 | 当前状态 | 你日常要做什么 |
|---|---|---|
| 平板 → 服务器 | 平板 SSH 钥匙已配置 | 直接 `ssh codexdev@120.55.53.215`，不需要服务器密码 |
| Codex / ChatGPT | 已在服务器的 `codexdev` 账户登录 | 正常直接运行 `codex`；不要执行 `codex logout` |
| GitHub 仓库 | 两个开发副本都已连到各自的 `origin` | 正常 `git push`；若出现网页登录/授权提示就停下处理，不要输密码到聊天中 |
| Linux 权限 | 日常用户是 `codexdev` | 开发只用这个账号；不要用 `sudo`，更不要切换 `root` |

想确认 Codex 登录还在不在，先退出 Codex 回到普通终端，然后运行：

```sh
codex login status
```

看到 `Logged in using ChatGPT` 就正常。服务器上的登录和你桌面端的登录是两份设备状态：它们使用同一 ChatGPT 账号，但一个掉线并不表示另一个也掉线。

#### 平板上的正常开发流程

1. 进入对应项目目录，运行 `git pull --ff-only` 和 `git status`。
2. 运行 `codex`。第一句先让它读项目说明、复述理解、列出准备改的文件；**没有确认需求前不要让它直接大改**。
3. 你确认方向后，明确说“请实现；改完运行相关测试；不要提交”。
4. 它完成后，先让它用中文总结：改了什么、为什么改、运行了什么测试、有没有失败。
5. 回到普通终端后检查：`git status`、`git diff --stat`。如果想看具体改动，用 `git diff`。
6. 确认无误才执行 `git add -A`、`git commit`、`git push`。每完成一个小功能就提交一次，提交信息写清楚中文。

下面这段是安全的“开工模板”，可以每次直接粘贴到 Codex：

```text
请先阅读 README.md、HANDOFF.md 和 docs/README.md，确认当前项目状态。先用中文说明：你理解的需求、准备改哪些文件、如何验证；在我确认前不要修改代码、不要提交、不要动生产目录、数据库或服务配置。
```

确认后再说：

```text
可以开始实现。请只做刚才确认的范围；完成后运行相关测试，给出修改摘要和 git diff 摘要，但不要替我提交或推送。
```

#### 断线、误关和旧对话怎么处理

- **平板网络断了**：重新 `ssh`，再 `tmux attach -t tablet-dev`。如果原来的 Codex 界面还在，就继续用，不要另开一个。
- **退出到了普通终端**：回到正确项目目录后运行 `codex` 开新对话；想接着旧话题就运行 `codex resume --all -C /srv/workspaces/daily-plan`（做 xitong 时换成 xitong 路径）。
- **不小心打开了错误项目**：在 Codex 输入 `/exit` 回到终端，`cd` 到正确目录，再启动 Codex。不要让它在 `~` 或生产目录里改代码。
- **要看当前改了什么**：先退出 Codex，运行 `git status`；不确定就把输出发给 Codex，不要直接 `git reset`、`git checkout --` 或 `rm -rf`。

---

## 第二部分：开发时必须遵守的红线

### 生产版和开发版不是同一个地方

| 类型 | 路径 | 能不能改 |
|---|---|---|
| `daily plan` 生产程序 | `/opt/daily-plan/current` | 不能直接改 |
| `daily plan` 生产数据库 | `/var/lib/daily-plan/daily_plan.db` | 不能碰 |
| `daily plan` 生产配置 | `/etc/daily-plan/daily-plan.env` | 不能看、不能复制、不能改 |
| 当前生产备份 | `/var/backups/daily-plan` | 不能删、不能覆盖 |
| 日常开发副本 | `/srv/workspaces/daily-plan` | 可以改 |
| `xitong` 开发副本 | `/srv/workspaces/xitong` | 可以改 |

不要执行下面这类命令，也不要让 AI 擅自执行：

```sh
sudo systemctl restart daily-plan
sudo systemctl stop daily-plan
sudo rm -rf /opt/daily-plan
```

也不要占用生产正在使用的端口：`8000`、`8080`，或改动 Tailscale / Funnel。

### 不要把“Git 代码”当成“用户数据备份”

- `git push` 保存的是代码、文档和配置样例。
- 你的 `daily plan` 真正使用记录在生产数据库里。
- 生产数据库已有独立备份机制；开发时不要把测试数据库和生产数据库混在一起。

一句话：**代码靠 Git 保，真实使用数据靠数据库备份保。**

### 服务器比电脑小，别强行做重活

这台服务器适合：

- 让 Codex 读代码、改代码、写文档
- 跑 Python 测试、后端测试、前端构建
- Git 提交、推送、拉取

它不适合：

- 大型 ESP-IDF 完整编译
- Chromium / Playwright 大规模浏览器渲染
- 同时开很多重型构建任务

如果终端感觉卡：先等一会儿；不要重复运行同一个安装命令，也不要同时开多个 npm / pip 安装。

---

## 第三部分：两个项目的常用命令

### `daily plan`

进入项目：

```sh
cd /srv/workspaces/daily-plan
```

查看改动：

```sh
git status
```

运行测试：

```sh
.venv/bin/pytest
```

当前已知情况：截至 2026-07-13，测试会出现 **61 通过、3 失败**。失败原因是旧测试还在断言已经被生产版本替换的页面入口，以及生产模式缺少测试用登录变量；不是服务器环境坏了。修改相关功能前，要让 Codex 判断是否该同步更新这些旧测试。

如果只想先检查代码能否启动，且不碰生产端口：

```sh
APP_RUNTIME_MODE=development .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001
```

这只用于本机测试。不要改为 `0.0.0.0`，不要用 `8000`。

### `xitong`

进入项目：

```sh
cd /srv/workspaces/xitong
```

后端测试：

```sh
cd /srv/workspaces/xitong/backend
.venv/bin/pytest
```

前端构建：

```sh
cd /srv/workspaces/xitong/frontend
npm run build
```

当前已知情况：截至 2026-07-13，后端测试是 **10 通过、1 失败**。失败测试把 2026-04-01 的数据放进“最近 90 天”热图，但当前日期已超过该范围；前端构建已通过。不要因为看到这一项旧测试失败，就误以为整个服务器环境坏了。

### 每次开始开发前的安全更新流程

```sh
git status
git pull --ff-only
```

只有 `git status` 干净时，才适合拉取更新。若它显示你自己的改动，先让 Codex 看清楚，不要为了更新而随便执行重置、覆盖或删除。

---

## 第四部分：出问题时按这里排查

### 1. 平板连不上服务器

先确认你输入的是：

```sh
ssh codexdev@120.55.53.215
```

常见提示：

| 看到的提示 | 大概意思 | 先怎么做 |
|---|---|---|
| `Permission denied` | 平板公钥未加入或钥匙不对 | 重新执行 `cat ~/.ssh/id_ed25519.pub`，把公钥发给 Codex。 |
| `Connection timed out` | 当前平板网络到 SSH 不通 | 换网络；若只有当前网络不通，再临时给平板开代理。 |
| `Connection refused` | 到了服务器但 SSH 服务异常 | 不要乱改，截图或复制提示给 Codex。 |

### 2. 连接中断、屏幕一关就不知道去哪了

重新 SSH 后运行：

```sh
tmux attach -t tablet-dev
```

如果提示会话不存在，说明服务器重启过或会话被关闭了；把提示发给 Codex。不要默认认为项目或代码丢了。

### 3. 下载、Git、npm、pip 或 Codex 连不上

先运行：

```sh
proxyctl
```

选择：

```text
3. 测试 GitHub
```

若失败，再选择：

```text
2. 切换手动节点
```

在 `一元机场` 分组换一个节点后，再测一次。服务器本机代理服务会自动开机启动；不要自行编辑 `/etc/mihomo/config.yaml`。

### 4. Codex 提示未登录

正常情况下它已经用 ChatGPT 登录。若以后真的显示未登录：

```sh
codex login
```

它会给出浏览器授权链接。远程服务器需要 SSH 本地端口转发才能完成回调；不要自己猜端口或把授权链接长期公开，直接让 Codex 协助处理。

### 5. Git 推送失败

先看完整提示。不要输入 GitHub 网站登录密码，也不要把令牌贴给 AI。

最常见不是代码问题，而是服务器还没有 GitHub 推送授权。把终端报错完整复制给 Codex，它会选择安全的授权方式。

### 6. 不小心进入了不该改的目录

如果看到路径开头是：

```text
/opt/daily-plan/current
```

立刻回到开发副本：

```sh
cd /srv/workspaces/daily-plan
```

不确定自己在哪时，运行：

```sh
pwd
```

### 7. 想让 AI 处理问题时怎么说

把下面这段直接贴给 Codex：

```text
我在阿里云服务器的 codexdev 开发账户中。请先确认当前目录和 git status；只能修改 /srv/workspaces 下的开发副本，不能碰 /opt/daily-plan/current、/etc/daily-plan、/var/lib/daily-plan、/var/backups/daily-plan，也不要重启 daily-plan、tailscaled 或 mihomo。请先说明你的判断，再做最小修改并运行相关验证。
```

---

## 第五部分：给 AI / 后续维护者的环境说明

### 当前服务器结构

```text
阿里云 Ubuntu 24.04
├─ 生产工作负载（不要碰）
│  ├─ /opt/daily-plan/current
│  ├─ /etc/daily-plan/daily-plan.env
│  ├─ /var/lib/daily-plan/daily_plan.db
│  ├─ /var/backups/daily-plan
│  ├─ daily-plan.service
│  ├─ daily-plan-backup.timer
│  ├─ daily-plan-dns.service
│  ├─ tailscaled / Funnel
│  └─ code-server 与 /root/algorithm_code
├─ 平板开发环境
│  ├─ 用户：codexdev
│  ├─ /srv/workspaces/daily-plan     (Git: 0bb10a8)
│  ├─ /srv/workspaces/xitong         (Git: f4772df)
│  ├─ Node 22、npm、tmux、Codex CLI
│  └─ tablet-dev tmux 会话
└─ 本机代理
   ├─ mihomo.service
   ├─ 127.0.0.1:7897 (HTTP/SOCKS)
   ├─ 127.0.0.1:9090 (仅本机控制接口)
   └─ /usr/local/bin/proxyctl
```

### 开发环境重建顺序

只有在服务器损坏、迁移或明确要求重建时才参考这一节；日常使用不需要重复执行。

1. 创建普通账户 `codexdev` 与 `/srv/workspaces`。
2. 配置 2GB Swap。
3. 安装 Git、tmux、Python、Node 22、npm 与 Codex CLI。
4. 为 `codexdev` 配置国内 npm / pip 镜像。
5. 克隆 `daily-plan` 和 `Moss_Lite` 的开发副本；绝不能复制或修改生产目录。
6. 建立项目虚拟环境，安装 Python 依赖；安装 `xitong/frontend` 的 npm 依赖。
7. 用当前 Clash 配置生成服务器专用 Mihomo 配置：关闭 TUN、关闭内置 DNS 监听、移除 Windows `interface-name`，只保留 `127.0.0.1:7897`。
8. 启用 `mihomo.service`，并为 `codexdev` 设置 Git、npm、pip 和 shell 环境代理。
9. 创建 `tablet-dev` tmux 会话，登录 Codex。
10. 验证：Mihomo 只监听回环地址；GitHub 代理测试成功；生产 `daily-plan.service` 仍为 `active`。

### Mihomo 与电脑 Clash 的区别

电脑上是 Clash Verge 图形界面，且原本使用了 TUN；服务器上是无界面的 Mihomo 服务。

- 两边使用的是同一时刻复制来的节点与规则，但不是同一个运行进程。
- 电脑切节点不会自动让服务器切节点。
- 服务器**没有启用 TUN**，也不接管系统 DNS，更不会把全服务器流量强行改道。
- 服务器只给开发工具提供本机代理，所以对现有生产服务的影响最小。
- 服务器代理配置包含节点信息，应视为敏感配置；不能提交到 Git、不能贴到聊天、不能开放 `9090` 控制端口到公网。

### 为什么要用 tmux

SSH 只是“远程屏幕连接”。平板断网、关 Termux 或切网络时，SSH 会断；如果直接在 SSH 里运行 Codex，Codex 也会一起消失。

tmux 是服务器里的“可持续终端窗口”。它留在服务器上运行，所以你回来重新连接后还能接上同一个工作现场。

### 为什么生产与开发必须分开

生产 `daily plan` 有真实数据库、真实登录配置、自动备份和公开入口。直接在生产目录改代码有三个风险：

1. 一次失误会影响你日常正在使用的网站。
2. 测试可能碰到真实数据。
3. 未提交的临时改动很难追溯和回退。

开发副本的意义是：先改、先测、先提交，再由明确的部署流程决定是否更新生产。当前文档不授权直接部署。

---

## 第六部分：技术词的通俗解释

| 词 | 你可以把它理解成 |
|---|---|
| 服务器 | 一台放在远处、长期不关机的电脑。 |
| SSH | 用终端远程进入这台电脑的方式。 |
| `codexdev` | 你的日常开发身份；比直接用管理员 `root` 更安全。 |
| `root` | 服务器管理员，权限很大；日常开发不要用。 |
| tmux | 服务器里的持续终端窗口；断线不等于任务停止。 |
| Codex CLI | 在服务器终端中工作的 Codex。它不是本地大模型，主要负责理解、修改和验证代码。 |
| Git | 代码的版本记录本；能知道什么改过、何时改过、怎么回退。 |
| GitHub | 远程保存代码版本的地方。 |
| 虚拟环境 `.venv` | 某个 Python 项目自己的依赖小盒子，避免两个项目互相污染。 |
| Node / npm | 前端和 JavaScript 工具常用的运行环境与包管理器。 |
| systemd | Linux 的后台服务管理员；负责开机启动、崩溃重启和状态查询。 |
| Mihomo / Clash | 代理客户端；决定网络请求经哪个节点出去。 |
| TUN | 一种接管系统整体网络流量的代理方式。服务器当前没有使用它。 |
| Swap | 磁盘划出的一块“慢速备用内存”。能防止部分任务直接被杀，但不会让机器变快。 |
| Funnel | 当前 `daily plan` 的 HTTPS 对外入口；不是开发副本。 |

## 最后一页：只记住这十句话

1. 平板只是入口，真正开发在服务器。
2. 先 SSH，再 `tmux attach -t tablet-dev`，再进 `dev` 窗口。
3. `daily plan` 只在 `/srv/workspaces/daily-plan` 改。
4. `xitong` 只在 `/srv/workspaces/xitong` 改。
5. `/opt/daily-plan/current` 是生产目录，不碰。
6. 代理有问题就运行 `proxyctl`，不要手改配置文件。
7. 断网后先回 tmux，不要急着重开 Codex。
8. 做完小功能就测试、提交、推送。
9. Git 保存代码，不等于备份真实使用数据。
10. 不确定时，先停下，把 `pwd`、`git status` 和完整报错发给 Codex。

---

## 第七部分：命令速查、逐词解释与“我现在该按什么”

这一部分故意写得很细。以后只要忘记某一步，先找“你看到的画面”，再复制对应代码；**不要凭印象把命令输到另一个界面。**

### 0. 三个画面，一张判断卡

| 你看到什么 | 名字 | 现在能输入什么 | 最常见误操作 |
|---|---|---|---|
| 黑底，最后一行是 `~ $` | 平板本地 Termux | `ssh ...`、`pkg ...`、查看平板钥匙 | 把 `codex`、`/model`、`codex resume ...` 输在这里。它们都不在平板本地。 |
| 黑底，最后一行是 `codexdev@iZbp...:~$` 或类似文字 | 服务器普通终端 | `cd`、`pwd`、`tmux`、`git`、`codex`、`proxyctl` | 把 `/model` 输在这里。斜杠命令只属于 Codex 对话。 |
| 顶部有 `OpenAI Codex`，底部有灰色 `>` 输入框 | Codex 对话界面 | 中文需求、`/model`、`/usage`、`/compact`、`/new`、`/exit` | 把 `ssh`、`cd`、`tmux attach` 输在这里。它们属于普通终端。 |

**万能规则：**

- 想“连服务器” → 必须先回到 `~ $` 或普通终端。
- 想“选择项目、运行 Git、恢复历史” → 必须在服务器普通终端。
- 想“和 AI 说话、选模型” → 必须在灰色 `>` 输入框。

### 1. 每天从零开始：两种正确入口

#### 入口 A：新建一段 `daily plan` 对话（最常用）

在平板本地 `~ $` 中，一条一条输入：

```sh
ssh codexdev@120.55.53.215
```

这条的关键词：

- `ssh`：Secure Shell，意思是“通过加密终端连接远程电脑”。
- `codexdev`：服务器上的日常开发账号，不是管理员。
- `@`：读作“在……上”。`codexdev@...` 就是“以 codexdev 身份进入后面的服务器”。
- `120.55.53.215`：服务器公网地址。地址不会因为断线而自动变成别的地址。

登录成功后，看到 `codexdev@...$`，继续输入：

```sh
tmux attach -t tablet-dev
```

关键词：

- `tmux`：服务器中持续存在的终端工作台。
- `attach`：接回、重新连接一个已经存在的工作台。
- `-t`：后面紧跟“目标名称”。
- `tablet-dev`：已为平板准备好的工作台名字；不要自行改名或删除。

如果画面已经回到 Codex，直接在灰色 `>` 框里聊天即可；如果是服务器普通终端，则输入：

```sh
cd /srv/workspaces/daily-plan
```

```sh
git pull --ff-only
```

```sh
git status
```

```sh
codex
```

这四条的意思：

- `cd` = change directory，切换当前位置。后面的 `/srv/workspaces/daily-plan` 是开发副本的完整地址。
- `/` 开头表示“从服务器最顶层开始找”，不是电脑的 `C:` 盘。
- `git pull` = 从 GitHub 取回远端已存在的代码。
- `--ff-only` = 只允许“能安全直接接上”的更新；发现冲突就停下，不偷偷合并。
- `git status` = 只检查状态，不改文件。它会告诉你当前在哪个分支、是否有未提交改动。
- `codex` = 在当前项目目录启动一段**新** Codex 对话。因此必须先 `cd` 到正确项目。

#### 入口 B：选择一段旧对话继续

先进入服务器普通终端；如果你当前在 Codex 灰色输入框，先输入：

```text
/exit
```

然后针对项目输入下面两条中的一条：

```sh
codex resume --all -C /srv/workspaces/daily-plan
```

```sh
codex resume --all -C /srv/workspaces/xitong
```

逐词解释：

- `codex`：启动 Codex 程序。
- `resume`：恢复以前保存的对话，而不是开新对话。
- `--all`：把所有历史对话都列出。这里的“所有”只是对话列表范围，**不是**把所有项目代码混在一起。
- `-C`：指定本次恢复后 Codex 的工作目录（C 代表 directory 的命令行缩写）。
- `/srv/workspaces/daily-plan`：让这段对话只在 daily plan 的服务器开发副本里工作。

历史选择器中每个按键的含义，以屏幕底部提示为准；当前版本你主要会用到：

| 选择器显示的提示 | 你要怎么按 | 会发生什么 |
|---|---|---|
| `↑/↓ browse` | 点 Termux 底部的 `↑` 或 `↓` | 上下移动到另一段历史。 |
| `enter resume` | 手机键盘回车 | 恢复当前高亮的对话。 |
| `ctrl+c quit` | 点 `CTRL`，再按 `c` | 放弃选择，回到普通终端；适合发现选错项目时。 |
| `esc new` | 点 `ESC` | 不恢复旧对话，直接新开一段对话。 |
| `←/→ option` | 点左右方向键 | 切换列表上的筛选/排序选项；看不懂时不用碰。 |

恢复旧电脑时期的对话后，先把这段发给 Codex，防止它沿用旧 Windows 路径：

```text
提醒：我现在通过平板在服务器的 /srv/workspaces/daily-plan 中开发。请先运行 pwd 和 git status 确认当前位置；不要使用旧电脑的 C:\ 路径，不要修改生产目录或服务配置。确认后再继续这段对话。
```

### 2. Codex 对话框里的每一个常用操作

以下内容全部输入到有灰色 `>` 的 Codex 对话框。输入后按回车。

| 目的 | 复制这行 | 说明 |
|---|---|---|
| 看当前版本支持哪些斜杠命令 | `/help` | 最权威的本机菜单。升级后命令有变化，以它为准。 |
| 切换模型 | `/model` | 先出现模型列表，再用 `↑`、`↓` 和回车选择。 |
| 查看用量 | `/usage` | 只看用量和重置机会，不会扣除额度。 |
| 长对话整理 | `/compact` | 把很长的已聊内容压缩成摘要；适合上下文太长时。 |
| 新话题 | `/new` | 仍在同一个项目，但上一段对话不再自动带入。 |
| 退出到服务器终端 | `/exit` | 对话会保留在历史中，可用 `codex resume` 恢复。 |
| 让 Codex 看一个文件 | `请阅读 @README.md，先不要修改。` | `@文件名` 是把文件明确指给 Codex 的简写。 |

#### 模型怎么选

1. 在灰色 `>` 框输入：

```text
/model
```

2. 等待菜单出现；它只会列出当前账号真正可用的模型。
3. 点屏幕底部 `↑`、`↓` 移动高亮，按手机键盘回车。
4. 看底部或顶部 `model:` 后面的名称是否改变。

不知道选哪个时，就使用菜单默认模型。模型越偏“high / 高思考”，通常越愿意仔细推理，但也可能更慢、更耗用量；这不代表它能绕过项目规则或自动知道你的需求。

#### 怎样让 Codex 读代码而不是立刻乱改

第一条总是用“调查模式”：

```text
我想做【把目标写在这里】。请只阅读和调查：指出当前实现在哪些文件、解释现有逻辑、列出准备修改的文件和验证方法。现在不要改代码、不要执行提交或推送。
```

你确认方案后再输入：

```text
方案确认。请只实现刚才说的范围；不要碰 /opt/daily-plan/current、/etc/daily-plan、/var/lib/daily-plan、/var/backups/daily-plan，也不要执行 sudo 或重启服务。完成后运行相关测试，给我中文摘要和 git diff 摘要；不要提交或推送。
```

完成后要求它自查：

```text
请停在提交之前：列出改动文件、解释每项改动、给出测试命令和结果，并指出仍未解决的风险。
```

这三段分别解决“先理解”“再动手”“最后验收”三个阶段。手机屏幕小，分阶段比一条长指令更不容易失控。

### 3. 文件、目录和项目：不会点文件树也能开发

在服务器普通终端中，这些命令都可以安全查看信息：

```sh
pwd
```

`pwd` = print working directory，打印“我目前在哪个目录”。它是确认路径的第一工具。

```sh
ls
```

`ls` = list，列出当前目录中的文件和子目录。

```sh
rg --files
```

`rg` 是 `ripgrep`，专门快速搜索文件。`--files` 表示只列文件，不搜索文字内容。

```sh
rg "关键词"
```

它会在当前项目中找包含“关键词”的代码和文档。双引号把关键词包起来，方便输入中文或带空格的内容。

```sh
sed -n '1,160p' README.md
```

这是只读查看：

- `sed`：一个文本查看工具。
- `-n`：不要默认把整份文件全输出。
- `'1,160p'`：只打印第 1 到第 160 行（p 是 print）。
- `README.md`：要看的文件名。

如果看完还想继续看第 161 行以后，把范围改成：

```sh
sed -n '161,320p' README.md
```

常用项目目录再次集中列出：

```text
/srv/workspaces/daily-plan   可开发的 daily plan Git 副本
/srv/workspaces/xitong       可开发的 xitong Git 副本
/opt/daily-plan/current      正在服务真实用户的生产程序，不能开发
/var/lib/daily-plan          真实用户数据库所在位置，不能碰
/etc/daily-plan              生产密钥与服务配置所在位置，不能碰
```

### 4. Git：把代码安全地保存到 GitHub

Git 不是自动保存。它像一个“有签名的版本相册”：你先挑选本次改动，再写一句说明，最后才上传。

每次提交前，在**服务器普通终端且已经 `cd` 到正确项目**后，依次输入：

```sh
git status
```

看有没有不认识的文件或改动。`status` 不会修改任何东西。

```sh
git diff --stat
```

`diff` = difference，比较“当前文件”和“最近一次提交”；`--stat` 只显示每个文件改了多少行，适合手机先快速扫一眼。

```sh
git diff
```

这会显示具体每一行的改动。前缀 `+` 通常是新增，前缀 `-` 通常是删除；看不懂就先不要提交，发给 Codex 问。

确认后才输入：

```sh
git add -A
```

- `add`：把改动放入“准备提交区”。
- `-A`：本项目内所有新增、修改、删除都包含进去。所以只有在你确认没有无关文件时才用它。

```sh
git commit -m "用中文描述本次做了什么"
```

- `commit`：创建一个本地版本记录。
- `-m`：后面跟本次记录的说明文字（message）。
- 引号里的字可以替换，例如：`"修正今日任务编辑按钮"`。

```sh
git push
```

`push`：把已经提交在服务器本地 Git 中的版本上传到 GitHub。它上传的是代码历史，不上传生产数据库。

如果 `git status` 显示不干净、`git pull --ff-only` 报错、或 `git push` 要求授权：停下，复制完整报错给 Codex；**不要**用 `git reset --hard`、`git checkout -- .`、`git clean -fd` 来“试试看”。它们可能抹掉未提交工作。

### 5. 测试和启动：每条命令实际做什么

#### daily plan

```sh
cd /srv/workspaces/daily-plan
.venv/bin/pytest
```

- `.venv`：这个项目自己的 Python 依赖盒子。
- `/bin/pytest`：虚拟环境里安装的测试执行器。
- `pytest`：自动运行项目的 Python 测试。

当前已知有 3 条旧测试失败；看到“61 passed, 3 failed”不等于你刚改坏了环境。要让 Codex 判断这些失败是否与本次改动有关。

仅在要本机试启动、且 Codex 明确建议时使用：

```sh
APP_RUNTIME_MODE=development .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001
```

- `APP_RUNTIME_MODE=development`：只对这一次命令声明“开发模式”。
- `uvicorn`：运行 Python Web 服务的程序。
- `app.main:app`：`app/main.py` 文件中的 `app` 对象。
- `--host 127.0.0.1`：只允许服务器自己访问，外网看不到。
- `--port 8001`：用测试端口。不要改成生产使用的 `8000`。

停止这个临时服务时，按 `Ctrl-c`；只在它正在运行且屏幕不断显示日志时这样按。这个 `Ctrl-c` 和 tmux 的 `Ctrl-b d` 完全不同。

#### xitong

```sh
cd /srv/workspaces/xitong/backend
.venv/bin/pytest
```

先切到后端，再调用该后端自己的 Python 测试。

```sh
cd /srv/workspaces/xitong/frontend
npm run build
```

- `npm`：Node/前端依赖和脚本工具。
- `run`：运行项目在 `package.json` 中登记的脚本。
- `build`：构建前端的正式产物；它不等于部署，不会自动上线。

### 6. 网络代理：什么时候该用 `proxyctl`

你不需要在平板 Termux 内设置 Clash，也不需要在服务器开 TUN。服务器已经有独立的 Mihomo 代理，Codex、Git、npm、pip 默认会通过它访问外网。

只有在服务器中的下载、GitHub、npm、pip 或 Codex 明确报“网络连接失败 / 超时”时，才在服务器普通终端输入：

```sh
proxyctl
```

菜单中：

```text
1 = 看当前节点与分组
2 = 切换手动节点
3 = 用代理测试 GitHub
0 = 退出
```

最安全顺序是先选 `3` 测试；失败才选 `2`，在 `一元机场` 手动分组中换节点，再选 `3` 重测。不要手动编辑 `/etc/mihomo/config.yaml`、不要打开 `9090` 端口、不要试图在服务器上开启 TUN。

### 7. 常见报错翻译：看见一句就知道下一步

| 终端提示 | 它真正表示什么 | 现在怎么做 |
|---|---|---|
| `Software caused connection abort` / `Broken pipe` | 平板与服务器的 SSH 网络断了；服务器未必坏了。 | 回到平板 `~ $`，重新 `ssh`，再 `tmux attach -t tablet-dev`。 |
| `bash: /model: No such file` | 你把 Codex 对话命令输入到了普通终端。 | 回到 Codex 灰色 `>` 框再输入 `/model`。 |
| `Command 'codex' not found`，且提示符为 `~ $` | 你在平板本地，不是服务器。 | 输入 `ssh codexdev@120.55.53.215`。 |
| `no sessions`，且提示符为 `~ $` | 你在平板本地查 tmux，本地当然没有服务器会话。 | 先 SSH；再在服务器里 `tmux attach -t tablet-dev`。 |
| `Permission denied`（SSH） | 平板钥匙未被服务器接受。 | 不要反复猜密码；把 `cat ~/.ssh/id_ed25519.pub` 输出的公钥发给维护者。 |
| `Connection timed out` | 当前网络到服务器不通，未必是服务器宕机。 | 换网络或临时给平板开代理；不要重启服务器。 |
| `Already inside tmux` / 画面已在 tmux | 你已经接入服务器工作台。 | 不需要再 `tmux attach`，直接按当前画面操作。 |
| `git pull --ff-only` 报错 | 服务器或远端有改动不能安全自动合并。 | 停下，把 `git status` 和完整报错发给 Codex。 |

### 8. 手机 ChatGPT 和服务器 Codex 如何配合

手机 ChatGPT 很适合：解释概念、帮你把需求说清楚、翻译报错、根据截图告诉你下一步输入什么。

服务器 Codex 很适合：阅读服务器里的真实项目文件、执行命令、修改代码、运行测试、给出 Git diff。

最稳的配合方式：

1. 先在手机 ChatGPT 想清楚“想做什么、不要做什么”。
2. 把整理好的需求复制到服务器 Codex 灰色 `>` 框。
3. Codex 做完后，把它的摘要、测试结果或终端报错截图发到手机 ChatGPT 解释。
4. 最终提交前，在服务器查看 `git status` 和 `git diff --stat`。

手机 ChatGPT 默认看不到你的服务器文件、服务器终端或 Git 状态；不要假定它已经知道实际项目进展。给它截图、报错或 Codex 的总结，它才能准确帮助你。

### 9. 不要做的事：比记命令更重要

以下命令即使 AI 建议，也先拒绝并求助：

```sh
sudo systemctl restart daily-plan
sudo systemctl stop daily-plan
sudo rm -rf /opt/daily-plan
git reset --hard
git checkout -- .
git clean -fd
```

关键词解释：

- `sudo`：临时取得管理员权限。它不是“让命令更有效”，而是会绕过日常保护。
- `systemctl restart/stop`：重启或停止正在提供服务的网站。
- `rm -rf`：递归、强制删除；其中 `-r` 是连文件夹内部都删，`-f` 是不再询问。
- `reset --hard`、`checkout -- .`、`clean -fd`：都可能让你尚未提交的代码无法恢复。

当你不知道某个命令是什么时，不要执行，直接把它复制给 Codex 并问：

```text
不要执行。请逐词解释这条命令会做什么、会改哪些文件、会不会影响生产、如何回退。
```
