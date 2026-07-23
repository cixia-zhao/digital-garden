# Termux 平板快捷键配置指南

> 适用环境：官方 GitHub 版 Termux 0.118.3、安卓平板、主要使用语音虚拟键盘、通过 SSH 操作云服务器。  
> 目标：让普通虚拟键盘负责中文、字母和符号，让 Termux 底部快捷栏只补充终端真正缺少的按键。

---


虚拟键盘已经能完成：

- 中文语音输入；
- 字母、数字和常见符号；
- Shift、退格、空格和回车；
- 中英文切换。

Termux 快捷栏只需要补充普通安卓键盘不方便提供的终端按键：

- `ESC`：退出菜单、取消选择；
- `TAB`：命令和文件名补全；
- `CTRL`、`ALT`：组合键；
- `Ctrl-C`：中止正在运行的命令；
- 方向键：选择菜单、移动光标、查看历史命令；
- `PASTE`：粘贴从 ChatGPT 复制的长提示词或命令；
- `KEYBOARD`：显示或隐藏虚拟键盘；
- `HOME`、`END`：移动到当前输入行的开头和末尾；
- `PGUP`、`PGDN`：低频翻页，放在上滑功能中，不直接占位置；
- `TMUX`：一键发送 tmux 的前缀 `Ctrl-b`，后续再按字母完成 tmux 操作。

---

## 二、推荐布局

第一排：

```text
ESC | TAB | CTRL | ALT | ^C | PASTE | 键盘
```

第二排：

```text
← | ↓ | ↑ | → | HOME | END | TMUX
```

附加上滑功能：

- `HOME` 上滑：`PGUP`
- `END` 上滑：`PGDN`
- `TMUX` 上滑：发送 `Ctrl-b d`，从 tmux 暂时离开，但不关闭里面的 Codex 或任务

### 为什么这样排

第一排属于“控制类”按键，主要用于取消、补全、中止、粘贴和切换键盘。

第二排属于“导航类”按键，主要用于菜单选择、移动光标、修改长命令和 tmux 操作。

### `TMUX` 键是什么

点一下 `TMUX`，等于：

```text
Ctrl-b
```

它不会立即做任何破坏性操作，只是告诉 tmux：“下一颗按键是 tmux 命令”。

例如：

```text
点 TMUX，再按 c
```

表示新建 tmux 窗口。

上滑 `TMUX` 发送：

```text
Ctrl-b，然后 d
```

这只是暂时离开 tmux。服务器里的任务仍然运行。

---

## 三、修改前先备份

以下操作在**平板本地 Termux**中执行。看到提示符：

```text
~ $
```

说明你在正确位置。

```bash
mkdir -p ~/.termux
```

解释：

- `mkdir` 表示创建目录。
- `-p` 表示目录已经存在时不报错。
- `~/.termux` 是 Termux 的配置目录。

```bash
cp ~/.termux/termux.properties \
   ~/.termux/termux.properties.backup-$(date +%F-%H%M%S)
```

解释：

- `cp` 表示复制文件。
- 第一段是原配置文件。
- 第二段是备份文件。
- `$(date +%F-%H%M%S)` 会自动加入当前日期和时间，避免覆盖旧备份。

查看备份是否存在：

```bash
ls -lh ~/.termux/termux.properties*
```

解释：

- `ls` 表示列出文件。
- `-l` 显示详细信息，`-h` 用容易阅读的单位显示大小。
- 末尾的 `*` 表示匹配所有以 `termux.properties` 开头的文件。

---

## 四、编辑配置文件

运行：

```bash
nano ~/.termux/termux.properties
```

解释：

- `nano` 是一个适合初学者的终端文本编辑器。
- 后面的路径是要编辑的 Termux 配置文件。

移动到文件最底部，找到你原来的这一段：

```properties
extra-keys = [ \
  ['ESC', 'F9', 'F10', 'F11', 'TAB', 'HOME'], \
  ['CTRL', 'ALT', 'UP', 'DOWN', 'LEFT', 'RIGHT'] \
]
```

删除这一段，替换为：

```properties
# 平板 + 语音输入 + SSH + tmux 推荐布局
extra-keys-style = arrows-only
extra-keys-text-all-caps = false

extra-keys = [ \
  [ \
    'ESC', \
    'TAB', \
    'CTRL', \
    'ALT', \
    {macro: "CTRL c", display: "^C"}, \
    'PASTE', \
    'KEYBOARD' \
  ], \
  [ \
    'LEFT', \
    'DOWN', \
    'UP', \
    'RIGHT', \
    {key: 'HOME', popup: 'PGUP'}, \
    {key: 'END', popup: 'PGDN'}, \
    {macro: "CTRL b", display: "TMUX", popup: {macro: "CTRL b d", display: "离开"}} \
  ] \
]
```

### 配置内容解释

```properties
extra-keys-style = arrows-only
```

让方向键使用箭头符号显示，减少文字占用。

```properties
extra-keys-text-all-caps = false
```

不强制把所有标签显示为全大写。

```properties
{macro: "CTRL c", display: "^C"}
```

点击 `^C` 时直接发送 `Ctrl-C`。常用于：

- 停止临时开发服务器；
- 中断卡住的命令；
- 退出某些选择菜单；
- 中止 Codex 当前正在执行的终端过程。

```properties
{key: 'HOME', popup: 'PGUP'}
```

点按是 `HOME`，向上滑是 `PGUP`。

```properties
{macro: "CTRL b", display: "TMUX"}
```

点击后发送 tmux 前缀 `Ctrl-b`。

```properties
popup: {macro: "CTRL b d", display: "离开"}
```

从 `TMUX` 按键向上滑，发送 `Ctrl-b d`，暂时离开 tmux。

---

## 五、保存并退出 nano

在 nano 中：

1. 按 `Ctrl-O` 保存；
2. 底部询问文件名时按回车确认；
3. 按 `Ctrl-X` 退出。

你的 Termux 底部已经有 `CTRL` 按键。操作方式是：

```text
点一下 CTRL，再按字母 o
```

不是必须同时按住。

---

## 六、重新加载配置

```bash
termux-reload-settings
```

解释：

- 这条命令让 Termux 重新读取 `termux.properties`。
- 不需要重启平板。

如果快捷栏没有立刻变化：

1. 从安卓最近任务中彻底关闭 Termux；
2. 重新打开；
3. 仍然异常时再检查配置文件是否有漏掉逗号、引号或反斜杠。

---

## 七、验证每个按键

依次测试：

### 测试方向键

输入：

```bash
echo first
echo second
```

随后按 `↑`，应该能调出上一条历史命令。

### 测试 TAB

输入：

```bash
cd /sr
```

按 `TAB`。在服务器中使用时，如果路径唯一，通常会自动补全。

### 测试 HOME 和 END

输入一条较长命令：

```bash
echo this-is-a-long-command
```

按 `HOME`，光标应移动到当前输入行开头。

按 `END`，光标应移动到当前输入行末尾。

### 测试 Ctrl-C

输入：

```bash
sleep 30
```

解释：

- `sleep 30` 表示等待 30 秒。

随后点击 `^C`，命令应立即停止并回到提示符。

### 测试 TMUX

只有已经 SSH 进入服务器、并且在 tmux 中时测试。

点击：

```text
TMUX
```

再按：

```text
w
```

应该打开 tmux 窗口列表。

按 `ESC` 返回。

---

## 八、出现问题时如何恢复

### 方法一：用最新备份恢复

查看备份：

```bash
ls -1t ~/.termux/termux.properties.backup-* | head
```

解释：

- `-t` 按时间排序。
- `head` 只显示最前面的几项，最新备份通常在第一行。

复制最新备份路径，然后执行：

```bash
cp 最新备份文件 ~/.termux/termux.properties
termux-reload-settings
```

把“最新备份文件”替换为真实路径。

### 方法二：Termux 普通界面无法启动

打开安卓应用列表中的：

```text
Termux: Failsafe
```

Failsafe 是 Termux 的最低限度恢复环境。它不会正常加载你写坏的 Bash 启动配置，适合修复：

- `~/.bashrc`
- `~/.profile`
- `~/.termux/termux.properties`
- 错误的默认 Shell 配置

在 Failsafe 中恢复备份后，重新打开普通 Termux。

---

## 九、日常按键速查

| 目的 | 操作 |
|---|---|
| 取消当前菜单 | `ESC` |
| 补全命令或路径 | `TAB` |
| 停止命令 | `^C` |
| 粘贴长内容 | `PASTE` |
| 调出上一条命令 | `↑` |
| 调出下一条命令 | `↓` |
| 移动输入光标 | `←`、`→` |
| 跳到当前行开头 | `HOME` |
| 跳到当前行末尾 | `END` |
| 显示或隐藏虚拟键盘 | `KEYBOARD` |
| 发送 tmux 前缀 | `TMUX` |
| 暂时离开 tmux | 上滑 `TMUX` |
| tmux 新建窗口 | `TMUX`，再按 `c` |
| tmux 窗口列表 | `TMUX`，再按 `w` |
| tmux 下一个窗口 | `TMUX`，再按 `n` |
| tmux 上一个窗口 | `TMUX`，再按 `p` |

---

## 十、不要这样做

- 不要删除整个 `~/.termux` 目录。
- 不要卸载 Termux 来解决快捷键配置错误；卸载可能同时删除平板本地 SSH 私钥。
- 不要把 `F1` 到 `F12` 全部塞入快捷栏，它们对当前工作流价值很低。
- 不要给每个 tmux 操作都制作宏，否则快捷栏会重新变得拥挤。
- 不要复制别人整份 `termux.properties` 覆盖自己的配置；不同输入法和设备需求不同。

---

## 官方资料

- Termux App：`https://github.com/termux/termux-app`
- Termux extra keys 相关说明：Termux 仓库中的 Terminal Settings / Extra Keys 文档
