# 平板服务器 AI CLI 终端开发环境优化与使用手册

> 适用环境：安卓平板、官方 GitHub 版 Termux 0.118.3、SSH、Ubuntu 24.04 云服务器、普通开发用户 `codexdev`、tmux、Codex CLI。  
> 服务器约 2 核 2GB 内存，因此本手册采用轻量、分阶段、用户目录优先的方案。  
> 文档编写日期：2026-07-18。

---

# 第一部分：这套改造的目的

## 1. 已有的结构

```text
安卓平板
└─ Termux
   └─ SSH
      └─ 云服务器
         ├─ tmux
         ├─ Codex CLI
         ├─ Git
         ├─ Python / Node / npm
         └─ 项目代码
```

这套结构本身没有问题。

- **Termux**负责显示终端、接收语音键盘和触摸操作。
- **SSH**负责把平板连接到远程服务器。
- **服务器**是真正运行代码、测试、Git和AI CLI的远程电脑。
- **tmux**负责让服务器中的终端工作现场在断网后继续存在。
- **Codex CLI**负责读取项目、修改代码和运行验证。

我们不推翻它，而是在每一层补上当前缺少的能力。

## 2. 目前的主要痛点

### 痛点一：路径太长

每次进入项目都要输入：

```bash
cd /srv/workspaces/daily-plan
```

解决工具：

- `zoxide`：记住常用目录，以后可以输入 `z daily`。
- `sesh`：把项目目录和 tmux session 结合起来。
- `fzf`：提供模糊搜索选择界面。

### 痛点二：tmux只会最基础的操作

目前虽然有 `tablet-dev`，但不容易理解：

- session、window、pane分别是什么；
- 怎样合理给两个项目分配工作区；
- 怎样分屏；
- 服务器重启后怎样恢复布局。

解决工具：

- tmux本身的完整配置；
- TPM；
- tmux-resurrect；
- tmux-continuum；
- sesh。

### 痛点三：服务器文件不直观

纯命令行中只能频繁使用：

```bash
ls
cd
cat
sed
```

解决工具：

- `Yazi`：终端文件管理器。
- `bat`：带行号和语法高亮地查看代码。
- `Glow`：阅读 Markdown。
- `fd`：按文件名快速查找。
- `eza`：更清晰地列目录。

### 痛点四：AI改完代码后不容易审查

解决工具：

- `lazygit`：终端中的交互式Git界面。
- `delta`：改善普通 `git diff` 的显示。

### 痛点五：忘记复杂命令

解决工具：

- `Atuin`：保存带目录、时间和退出状态的命令历史。
- `just`：把项目测试、构建和启动命令写成固定任务。

### 痛点六：长任务结束时人已经切走

解决工具：

- `ntfy`：服务器任务完成后向安卓客户端发通知。

### 痛点七：提示符看不出自己在哪

解决工具：

- `Starship`：只显示当前目录、Git分支、修改状态和命令失败状态。

## 3. 安装完成后的结构

```text
安卓平板
├─ Termux
│  ├─ 自定义快捷栏
│  ├─ Termux:Widget
│  ├─ Termux:API
│  ├─ Termux:Float（可选）
│  └─ Termux:Styling（可选）
└─ SSH
   └─ 云服务器
      ├─ Bash
      │  ├─ zoxide
      │  ├─ Atuin
      │  └─ Starship
      ├─ tmux
      │  ├─ TPM
      │  ├─ tmux-resurrect
      │  ├─ tmux-continuum
      │  └─ sesh
      ├─ AI
      │  └─ Codex CLI
      ├─ 文件与阅读
      │  ├─ Yazi
      │  ├─ bat
      │  ├─ Glow
      │  ├─ fd
      │  └─ eza
      ├─ Git审查
      │  ├─ lazygit
      │  └─ delta
      ├─ 项目任务
      │  └─ just
      └─ 通知
         └─ ntfy
```

## 4. 哪些工具暂时不安装

### Termux:X11

它会引入本地图形桌面，不符合“AI CLI + 服务器为主”的轻量目标。

### 魔改Termux和Termux Monet

不明来源改版会增加签名、更新和安全风险；Termux Monet已经停止维护。

## 5. 不打架的核心原则

本手册专门采用以下规则：

1. 服务器只使用 **Bash**，不再同时引入Zsh、Fish等Shell。
2. 新工具优先安装到：

```text
~/.local/bin
```

避免覆盖系统文件。

3. `fzf`只作为选择器使用，不启用它自己的 `Ctrl-R` 历史绑定。
4. `Atuin`独占 `Ctrl-R`，但不接管方向上键。
5. `Starship`最后初始化，只负责提示符。
6. `tmux-continuum`放在tmux插件列表最后，避免状态栏插件覆盖自动保存逻辑。
7. `tmux-resurrect`只恢复tmux布局和保守程序，不承诺自动恢复同一段Codex对话。
8. 所有配置先备份，再合并，不直接覆盖。
9. 一次只安装一个阶段，验证后再继续。
10. 不让这些工具访问或修改生产目录、数据库和服务。

---

# 第二部分：完整安装与部署教程

## 0. 执行位置说明

看到：

```text
~ $
```

表示你在**平板本地Termux**。

看到：

```text
codexdev@服务器名:~$
```

表示你在**服务器普通终端**。

看到顶部写 `OpenAI Codex`，底部有 `>`，表示你在**Codex对话界面**。

本部分绝大多数命令都在服务器普通终端执行。

---

## 1. 逃课版：让服务器中的Codex逐阶段帮你部署

不要让Codex一次安装全部工具。每次只发一个阶段，检查无误后再继续。

### 通用安全提示词

在服务器的Codex中发送：

```text
我要按《平板服务器 AI CLI 终端开发环境优化与使用手册》逐步配置终端环境。

请先只调查，不修改：
1. 确认当前用户、HOME、Shell、CPU架构和Ubuntu版本；
2. 检查本阶段涉及的命令是否已经安装；
3. 检查 ~/.bashrc、~/.tmux.conf、~/.gitconfig 中是否已有相关配置；
4. 说明准备修改哪些用户目录文件；
5. 说明是否需要 sudo，以及为什么；
6. 确认不会触碰 /opt/daily-plan/current、/etc/daily-plan、/var/lib/daily-plan、/var/backups/daily-plan，也不会重启生产服务、tailscaled或mihomo；
7. 先给出安装计划和回退方法，等我确认后再执行。
```

确认后发送：

```text
方案确认。请只执行当前阶段：
- 所有配置先创建带时间戳的备份；
- 优先安装到 ~/.local/bin；
- 不更换默认Shell；
- 不覆盖整份配置文件，只追加带清晰注释的独立配置块；
- 每安装一个工具就运行版本检查；
- 完成后汇报修改文件、安装位置、版本、验证结果和回退方法；
- 不提交Git，不修改项目代码。
```

### 阶段顺序

1. 基础检查和PATH；
2. tmux配置与两个插件；
3. fzf、zoxide、sesh；
4. bat、fd、eza、Glow、Yazi；
5. lazygit、delta；
6. Atuin；
7. just；
8. Starship；
9. ntfy；
10. Termux官方插件和桌面快捷入口。

---

## 2. 安装前检查

在**服务器普通终端**运行：

```bash
whoami
echo "$HOME"
echo "$SHELL"
uname -m
cat /etc/os-release
free -h
```

解释：

- `whoami`：确认当前Linux用户，应为 `codexdev`。
- `echo "$HOME"`：确认当前用户主目录。
- `echo "$SHELL"`：确认当前Shell，本手册按Bash配置。
- `uname -m`：查看CPU架构。
- `cat /etc/os-release`：查看系统版本。
- `free -h`：查看内存和Swap。

检查已有工具：

```bash
for cmd in tmux git curl wget unzip jq less file \
           fzf zoxide sesh lazygit delta yazi ya glow \
           bat batcat fd fdfind eza atuin just starship codex; do
  printf "%-10s " "$cmd"
  command -v "$cmd" || echo "未安装"
done
```

解释：

- `for ... do ... done`：依次检查一组命令。
- `command -v`：显示命令实际位置；找不到就说明未安装或不在PATH中。

---

## 3. 创建统一备份目录

```bash
mkdir -p ~/config-backups
STAMP="$(date +%F-%H%M%S)"
```

解释：

- `STAMP=...`：把当前日期和时间保存到变量中，供备份文件命名。

备份现有配置：

```bash
for file in ~/.bashrc ~/.profile ~/.tmux.conf ~/.gitconfig; do
  if [ -f "$file" ]; then
    cp -a "$file" "$HOME/config-backups/$(basename "$file").$STAMP"
  fi
done
```

解释：

- `[ -f "$file" ]`：只有文件存在时才备份。
- `cp -a`：尽量保留原文件属性。
- `basename`：只取文件名，不保留前面的目录。

查看：

```bash
ls -lh ~/config-backups
```

---

## 4. 准备用户级命令目录

```bash
mkdir -p ~/.local/bin
```

把下面配置追加到 `~/.profile`：

```bash
cat >> ~/.profile <<'EOF'

# ===== AI CLI terminal tools =====
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) export PATH="$HOME/.local/bin:$PATH" ;;
esac

case ":$PATH:" in
  *":$HOME/.atuin/bin:"*) ;;
  *) export PATH="$HOME/.atuin/bin:$PATH" ;;
esac
# ===== end AI CLI terminal tools =====
EOF
```

解释：

- `cat >> 文件 <<'EOF'`：把多行内容追加到文件末尾。
- 这段配置只在PATH中缺少目录时才加入，避免重复。

立即生效：

```bash
source ~/.profile
```

解释：

- `source`：让当前Shell重新读取配置，不必重新登录。

验证：

```bash
echo "$PATH" | tr ':' '\n' | sed -n '1,20p'
```

---

## 5. 安装基础依赖

这一步可能需要管理员权限，只安装通用命令，不修改生产服务。

```bash
sudo apt update
sudo apt install -y \
  git curl wget unzip jq less file ca-certificates \
  tmux bat fd-find
```

解释：

- `sudo`：临时以管理员权限执行；只在安装系统软件时使用。
- `apt update`：更新软件包目录，不升级整个系统。
- `apt install`：安装列出的工具。
- `-y`：对安装确认自动回答“是”。

Ubuntu中：

- `bat` 的实际命令可能叫 `batcat`；
- `fd` 的实际命令可能叫 `fdfind`。

稍后统一处理，不创建系统级覆盖。

---

## 6. 配置Bash兼容层

打开 `~/.bashrc`：

```bash
nano ~/.bashrc
```

在末尾加入：

```bash
# ===== AI CLI terminal compatibility =====

# Ubuntu把bat命名为batcat时，提供bat命令。
if ! command -v bat >/dev/null 2>&1 && command -v batcat >/dev/null 2>&1; then
  alias bat='batcat'
fi

# Ubuntu把fd命名为fdfind时，提供fd命令。
if ! command -v fd >/dev/null 2>&1 && command -v fdfind >/dev/null 2>&1; then
  alias fd='fdfind'
fi

# 常用安全查看命令。
alias ll='eza -lah --group-directories-first --git'
alias tree2='eza --tree --level=2 --group-directories-first'

# ===== end AI CLI terminal compatibility =====
```

暂时不要重新加载，等eza安装后统一验证。

---

## 7. tmux、TPM、resurrect和continuum

### 7.1 确认tmux

```bash
tmux -V
```

### 7.2 安装TPM

```bash
mkdir -p ~/.tmux/plugins
git clone https://github.com/tmux-plugins/tpm \
  ~/.tmux/plugins/tpm
```

解释：

- `git clone`：把GitHub仓库复制到指定目录。
- TPM是tmux插件管理器。

如果目录已经存在，不要重复克隆。改用：

```bash
git -C ~/.tmux/plugins/tpm pull --ff-only
```

解释：

- `git -C 目录`：在指定目录中执行Git命令。
- `pull --ff-only`：只进行安全的快进更新。

### 7.3 推荐tmux配置

如果已有 `~/.tmux.conf`，先查看：

```bash
sed -n '1,240p' ~/.tmux.conf
```

以下内容应与旧配置合并，不要盲目重复追加。

```tmux
# ===== tablet AI CLI tmux config =====

# 基础体验
set -g mouse on
set -g history-limit 20000
set -g escape-time 10
set -g status-interval 5
set -g detach-on-destroy off
set -g renumber-windows on

# 编号从1开始，更符合普通人的直觉
set -g base-index 1
setw -g pane-base-index 1

# 新窗口和新分屏继承当前目录
bind c new-window -c "#{pane_current_path}"
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# 重新加载配置
bind r source-file ~/.tmux.conf \; display-message "tmux配置已重新加载"

# 连续调整分屏大小
bind -r H resize-pane -L 5
bind -r J resize-pane -D 3
bind -r K resize-pane -U 3
bind -r L resize-pane -R 5

# 临时工具浮窗：从当前项目目录打开，退出后回到原来的Codex画面
bind-key T display-popup -h 85% -w 80% -E "sesh picker"
bind-key y display-popup -d "#{pane_current_path}" -h 90% -w 90% -E "yazi"
bind-key g display-popup -d "#{pane_current_path}" -h 90% -w 90% -E "glow -t ."

# TPM与插件
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# 每15分钟自动保存；tmux重新启动时自动恢复最后一次布局
set -g @continuum-save-interval '15'
set -g @continuum-restore 'on'

# 保存pane中可见的部分文本，方便重启后回看
set -g @resurrect-capture-pane-contents 'on'

# 必须放在配置文件最后
run '~/.tmux/plugins/tpm/tpm'

# ===== end tablet AI CLI tmux config =====
```

注意：

- continuum必须排在插件列表最后。
- `run TPM`必须位于配置末尾。
- 不配置自动恢复Codex会话ID，避免旧账号、旧路径或加密会话兼容问题。
- 插件保存的是tmux结构，不等于Git备份，也不等于Codex会话备份。

### 7.4 检查语法并加载

```bash
tmux source-file ~/.tmux.conf
```

如果当前不在tmux中也可以执行。出现错误时停止，不要继续安装插件。

### 7.5 安装插件

进入tmux：

```bash
tmux new-session -A -s tablet-dev
```

解释：

- `new-session`：创建session。
- `-A`：同名session已存在就直接连接。
- `-s tablet-dev`：session名称。

在tmux中：

```text
Ctrl-b，松开，再按大写 I
```

它会由TPM安装插件。

### 7.6 验证

手动保存：

```text
Ctrl-b，松开，再按 Ctrl-s
```

手动恢复：

```text
Ctrl-b，松开，再按 Ctrl-r
```

查看保存文件：

```bash
ls -lh ~/.tmux/resurrect/
```

---

## 8. 安装最新版fzf

不使用Ubuntu可能偏旧的fzf包，直接安装官方预编译二进制到用户目录。

```bash
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) FZF_ARCH="amd64" ;;
  aarch64|arm64) FZF_ARCH="arm64" ;;
  *) echo "暂不支持的架构：$ARCH"; return 1 2>/dev/null || exit 1 ;;
esac
```

解释：

- `case`：根据CPU架构选择对应安装包。

```bash
FZF_URL="$(
  curl -fsSL https://api.github.com/repos/junegunn/fzf/releases/latest |
  jq -r --arg arch "$FZF_ARCH" \
    '.assets[].browser_download_url |
     select(test("linux_" + $arch + "\\.tar\\.gz$"))' |
  head -1
)"
```

解释：

- GitHub API返回最新版信息。
- `jq`从中选择当前架构的Linux压缩包地址。

```bash
test -n "$FZF_URL" || { echo "没有找到fzf安装包"; exit 1; }
curl -fL "$FZF_URL" -o /tmp/fzf.tar.gz
tar -xzf /tmp/fzf.tar.gz -C /tmp
install -m 755 /tmp/fzf ~/.local/bin/fzf
fzf --version
```

这里不运行 `eval "$(fzf --bash)"`，原因是：

- fzf默认会占用 `Ctrl-R`；
- 后面让Atuin负责历史搜索；
- sesh和zoxide可以直接调用fzf，不需要全局快捷键。

---

## 9. 安装zoxide

下载官方安装脚本到本地，先查看，再执行：

```bash
curl -fsSL \
  https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh \
  -o /tmp/zoxide-install.sh
```

```bash
less /tmp/zoxide-install.sh
```

解释：

- `less`是只读分页器。
- 按 `q` 退出查看。

执行：

```bash
sh /tmp/zoxide-install.sh --bin-dir "$HOME/.local/bin"
zoxide --version
```

在 `~/.bashrc` 末尾加入：

```bash
# zoxide：智能目录跳转
if command -v zoxide >/dev/null 2>&1; then
  eval "$(zoxide init bash)"
fi
```

---

## 10. 安装sesh

sesh官方支持Go安装。先检查：

```bash
go version
```

若没有Go：

```bash
sudo apt install -y golang-go
```

安装到用户目录：

```bash
GOBIN="$HOME/.local/bin" \
go install github.com/joshmedeski/sesh/v2@latest
```

解释：

- `GOBIN=...`只对本次命令指定安装位置。
- `go install ...@latest`下载源码并编译最新版。
- 这是一次性编译，2GB服务器可能需要等待几分钟，不要重复运行。

验证：

```bash
sesh --version
```

生成用户级Bash补全：

```bash
mkdir -p ~/.local/share/bash-completion/completions
sesh completion bash \
  > ~/.local/share/bash-completion/completions/sesh
```

### sesh最小配置

```bash
mkdir -p ~/.config/sesh
nano ~/.config/sesh/sesh.toml
```

写入：

```toml
#:schema https://github.com/joshmedeski/sesh/raw/main/sesh.schema.json

[tui]
prompt = "> "
placeholder = "选择项目或tmux会话..."
show_icons = false

[[session]]
name = "daily-plan"
path = "/srv/workspaces/daily-plan"
startup_command = "git status"
preview_command = "eza -lah --git --color=always /srv/workspaces/daily-plan"

[[session]]
name = "xitong"
path = "/srv/workspaces/xitong"
startup_command = "git status"
preview_command = "eza -lah --git --color=always /srv/workspaces/xitong"
```

这里不让sesh自动启动Codex，避免误开多个AI进程。

### tmux中加入项目、文件和文档入口

在 `~/.tmux.conf` 的TPM配置之前加入：

```tmux
# 在tmux中按 Prefix + T 打开项目/session选择器
bind-key T display-popup -h 85% -w 80% -E "sesh picker"

# 在当前项目目录临时打开Yazi文件浏览器
bind-key y display-popup -d "#{pane_current_path}" -h 90% -w 90% -E "yazi"

# 在当前项目目录临时打开Glow Markdown文档库
bind-key g display-popup -d "#{pane_current_path}" -h 90% -w 90% -E "glow -t ."
```

重新加载：

```bash
tmux source-file ~/.tmux.conf
```

说明：

- `Prefix + T`：sesh项目/session选择器，适合已配置项目时使用。
- `Prefix + y`：Yazi浮窗，适合临时浏览和预览文件；它不会改变原来pane的工作目录。
- `Prefix + g`：Glow浮窗，适合浏览当前项目中的Markdown文档；按 `q`退出。

### 登录后选择已有tmux会话：`ts`

`ts`只处理**已经在运行的tmux会话**，不列目录、不自动创建项目。它用tmux提供会话和预览，用fzf提供搜索界面；适合“刚SSH登录，不记得上次在哪个会话”。

创建脚本：

```bash
cat > ~/.local/bin/tmux-session-picker <<'EOF'
#!/usr/bin/env bash
set -u

list_sessions() {
  tmux list-sessions -F $'#{session_name}\t#{session_windows}\t#{?session_attached,已连接,未连接}\t#{window_name}\t#{t:session_activity}\t#{session_activity}' 2>/dev/null \
    | sort -t $'\t' -k6,6nr \
    | awk -F $'\t' '{ printf "%s\t%s  · 当前窗口：%s · %s 个窗口 · %s · 最近 %s\n", $1, $1, $4, $2, $3, $5 }'
}

preview_session() {
  local session_name="$1"
  printf '会话：%s\n\n最近的屏幕输出：\n' "$session_name"
  tmux capture-pane -p -t "=${session_name}:" -S -80 2>/dev/null \
    || printf '\n（该会话已结束，或暂时无法读取预览。）\n'
}

delete_session() {
  local session_name="$1" answer
  if ! tmux has-session -t "=${session_name}" 2>/dev/null; then
    printf '\n会话“%s”已经不存在了。\n' "$session_name" >/dev/tty
    return 0
  fi
  printf '\n删除会话“%s”吗？其中正在运行的 Codex、Shell 和任务都会停止。输入 y 确认： ' "$session_name" >/dev/tty
  IFS= read -r answer </dev/tty || return 0
  case "$answer" in
    y|Y|yes|YES) tmux kill-session -t "=${session_name}"; printf '已删除会话“%s”。\n' "$session_name" >/dev/tty ;;
    *) printf '已取消删除。\n' >/dev/tty ;;
  esac
}

choose_session() {
  local selected session_name
  if ! tmux has-session 2>/dev/null; then
    printf '当前没有正在运行的 tmux 会话。\n' >&2
    return 0
  fi
  selected="$({ list_sessions; } | fzf \
    --no-multi --no-sort --delimiter=$'\t' --with-nth=2.. \
    --prompt='会话 › ' --border-label=' tmux 会话 ' \
    --header='直接输入名称搜索 · Enter 进入 · Ctrl-d 删除（会确认）· Esc 取消' \
    --preview="$0 --preview {1}" --preview-window='down:45%:wrap' \
    --bind="ctrl-d:execute($0 --delete {1})+reload($0 --list)+clear-query")" || return 0
  session_name="${selected%%$'\t'*}"
  [ -n "$session_name" ] || return 0
  if [ -n "${TMUX:-}" ]; then tmux switch-client -t "=${session_name}"; else tmux attach-session -t "=${session_name}"; fi
}

case "${1:-}" in
  --list) list_sessions ;;
  --preview) preview_session "${2:?缺少会话名}" ;;
  --delete) delete_session "${2:?缺少会话名}" ;;
  "") choose_session ;;
  *) printf '用法：%s\n' "$(basename "$0")" >&2; exit 2 ;;
esac
EOF
chmod 755 ~/.local/bin/tmux-session-picker
```

在 `~/.bashrc` 中加入：

```bash
# 登录后用 ts 搜索并进入已有 tmux 会话；目录切换仍使用 y（Yazi）。
ts() {
  command tmux-session-picker "$@"
}
```

加载和验证：

```bash
source ~/.bashrc
ts
```

`ts` 中直接输入部分会话名筛选，`Enter`进入，`Esc`或 `Ctrl-c`取消；`Ctrl-d`删除选中的整个会话，且必须输入 `y` 才确认。tmux外运行时它附着到目标会话，tmux内运行时它切换当前客户端，不会嵌套tmux。

---

## 11. 安装eza

```bash
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) EZA_TARGET="x86_64-unknown-linux-gnu" ;;
  aarch64|arm64) EZA_TARGET="aarch64-unknown-linux-gnu" ;;
  *) echo "暂不支持的架构：$ARCH"; return 1 2>/dev/null || exit 1 ;;
esac
```

```bash
curl -fL \
  "https://github.com/eza-community/eza/releases/latest/download/eza_${EZA_TARGET}.tar.gz" \
  -o /tmp/eza.tar.gz
mkdir -p /tmp/eza-extract
tar -xzf /tmp/eza.tar.gz -C /tmp/eza-extract
install -m 755 /tmp/eza-extract/eza ~/.local/bin/eza
eza --version
```

---

## 12. 安装Glow

官方提供Ubuntu apt仓库。为了避免编译，使用官方签名仓库：

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://repo.charm.sh/apt/gpg.key |
  sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
```

```bash
echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" |
  sudo tee /etc/apt/sources.list.d/charm.list
```

```bash
sudo apt update
sudo apt install -y glow
glow --version
```

这只添加Charm官方软件源，用于安装Glow。没有安装其他常驻服务。

---

## 13. 安装Yazi

Yazi不常驻后台，只在运行时占用资源。

```bash
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) YAZI_TARGET="x86_64-unknown-linux-gnu" ;;
  aarch64|arm64) YAZI_TARGET="aarch64-unknown-linux-gnu" ;;
  *) echo "暂不支持的架构：$ARCH"; return 1 2>/dev/null || exit 1 ;;
esac
```

```bash
YAZI_URL="$(
  curl -fsSL https://api.github.com/repos/sxyazi/yazi/releases/latest |
  jq -r --arg target "$YAZI_TARGET" \
    '.assets[].browser_download_url |
     select(endswith("yazi-" + $target + ".zip"))' |
  head -1
)"
```

```bash
test -n "$YAZI_URL" || { echo "没有找到Yazi安装包"; exit 1; }
rm -rf /tmp/yazi-extract
mkdir -p /tmp/yazi-extract
curl -fL "$YAZI_URL" -o /tmp/yazi.zip
unzip -q /tmp/yazi.zip -d /tmp/yazi-extract
find /tmp/yazi-extract -type f \( -name yazi -o -name ya \) \
  -exec install -m 755 {} ~/.local/bin/ \;
yazi --version
ya --version
```

### Yazi退出后停留在所选目录

在 `~/.bashrc` 末尾加入：

```bash
# 用 y 启动Yazi；按q退出后，Shell进入Yazi最后所在目录
function y() {
  local tmp="$(mktemp -t "yazi-cwd.XXXXXX")" cwd
  command yazi "$@" --cwd-file="$tmp"
  IFS= read -r -d '' cwd < "$tmp"
  [ "$cwd" != "$PWD" ] && [ -d "$cwd" ] && builtin cd -- "$cwd"
  command rm -f -- "$tmp"
}
```

---

## 14. 安装lazygit

使用官方发布二进制，不引入额外包管理器。

```bash
LAZYGIT_VERSION="$(
  curl -fsSL https://api.github.com/repos/jesseduffield/lazygit/releases/latest |
  jq -r '.tag_name | ltrimstr("v")'
)"
```

```bash
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) LAZYGIT_ARCH="x86_64" ;;
  aarch64|arm64) LAZYGIT_ARCH="arm64" ;;
  *) echo "暂不支持的架构：$ARCH"; return 1 2>/dev/null || exit 1 ;;
esac
```

```bash
curl -fL \
  "https://github.com/jesseduffield/lazygit/releases/download/v${LAZYGIT_VERSION}/lazygit_${LAZYGIT_VERSION}_Linux_${LAZYGIT_ARCH}.tar.gz" \
  -o /tmp/lazygit.tar.gz
mkdir -p /tmp/lazygit-extract
tar -xzf /tmp/lazygit.tar.gz -C /tmp/lazygit-extract
install -m 755 /tmp/lazygit-extract/lazygit ~/.local/bin/lazygit
lazygit --version
```

---

## 15. 安装delta

下载官方 `.deb`：

```bash
DEB_ARCH="$(dpkg --print-architecture)"
DELTA_URL="$(
  curl -fsSL https://api.github.com/repos/dandavison/delta/releases/latest |
  jq -r --arg arch "$DEB_ARCH" \
    '.assets[].browser_download_url |
     select(endswith("_" + $arch + ".deb"))' |
  head -1
)"
```

```bash
test -n "$DELTA_URL" || { echo "没有找到delta安装包"; exit 1; }
curl -fL "$DELTA_URL" -o /tmp/git-delta.deb
sudo apt install -y /tmp/git-delta.deb
delta --version
```

安全配置Git：

```bash
git config --global core.pager delta
git config --global interactive.diffFilter 'delta --color-only'
git config --global delta.navigate true
git config --global delta.dark true
git config --global merge.conflictStyle zdiff3
```

解释：

- `git config --global`修改当前用户的全局Git配置。
- delta只改变显示，不改变Git仓库内容。

---

## 16. 安装Atuin：先只使用本地模式

下载官方脚本，先查看：

```bash
curl --proto '=https' --tlsv1.2 -LsSf \
  https://setup.atuin.sh \
  -o /tmp/atuin-install.sh
less /tmp/atuin-install.sh
```

执行非交互安装：

```bash
sh /tmp/atuin-install.sh --non-interactive
```

```bash
atuin --version
```

导入现有Bash历史：

```bash
atuin import auto
```

在 `~/.bashrc` 末尾加入：

```bash
# Atuin负责Ctrl-R；保留普通方向上键；关闭Atuin AI问号快捷键
if command -v atuin >/dev/null 2>&1; then
  eval "$(atuin init bash --disable-up-arrow --disable-ai)"
fi
```

为什么这样配置：

- 不让Atuin接管 `↑`，普通上一条命令逻辑仍在。
- 让Atuin使用 `Ctrl-R`。
- 不启用Atuin内置AI，避免与Codex功能重复。
- 不注册、不登录、不自动云同步。

### 过滤可能的敏感命令

```bash
mkdir -p ~/.config/atuin
nano ~/.config/atuin/config.toml
```

加入或合并：

```toml
auto_sync = false
enter_accept = false

history_filter = [
  "^export .*TOKEN",
  "^export .*KEY",
  "^export .*SECRET",
  "^codex login",
  "^atuin login",
  "^ssh-keygen",
]
```

`enter_accept = false` 表示在Atuin中按回车时先把命令放回输入行，不立即执行，更适合初学者审查。

---

## 17. 安装just

下载官方脚本并查看：

```bash
curl --proto '=https' --tlsv1.2 -sSf \
  https://just.systems/install.sh \
  -o /tmp/just-install.sh
less /tmp/just-install.sh
```

安装到用户目录：

```bash
bash /tmp/just-install.sh --to "$HOME/.local/bin"
just --version
```

不要立即让Codex为项目随意创建justfile。先让它调查项目现有命令和README，再单独确认。

---

## 18. 安装Starship

下载官方安装脚本并查看：

```bash
curl -fsSL https://starship.rs/install.sh \
  -o /tmp/starship-install.sh
less /tmp/starship-install.sh
```

安装到用户目录：

```bash
sh /tmp/starship-install.sh -b "$HOME/.local/bin" -y
starship --version
```

在 `~/.bashrc` 最末尾加入：

```bash
# Starship必须放在zoxide和Atuin之后
if command -v starship >/dev/null 2>&1; then
  eval "$(starship init bash)"
fi
```

创建精简配置：

```bash
mkdir -p ~/.config
nano ~/.config/starship.toml
```

写入：

```toml
add_newline = false
command_timeout = 800

format = "$username$hostname$directory$git_branch$git_status$cmd_duration$status$character"

[username]
show_always = false
format = "[$user]($style)@"

[hostname]
ssh_only = true
format = "[$hostname]($style) "

[directory]
truncation_length = 2
truncate_to_repo = true
format = "[$path]($style) "

[git_branch]
format = "[$branch]($style) "

[git_status]
format = "([$all_status$ahead_behind]($style) )"
conflicted = "!"
modified = "*"
staged = "+"
untracked = "?"
deleted = "x"

[cmd_duration]
min_time = 3000
format = "[$duration]($style) "

[status]
disabled = false
format = "[$status]($style) "

[character]
success_symbol = "[❯](bold green)"
error_symbol = "[❯](bold red)"
```

如果字体不能显示箭头符号，把最后两行改成普通 `$`。

---

## 19. 配置ntfy通知

你已经安装安卓ntfy客户端，服务器不必安装ntfy程序，只需要curl。

### 19.1 生成难以猜测的主题

```bash
NTFY_TOPIC="ai-cli-$(openssl rand -hex 16)"
echo "$NTFY_TOPIC"
```

解释：

- `openssl rand -hex 16`生成随机字符串。
- 公开ntfy主题名相当于密码，不能使用简单的 `test` 或姓名。

把显示出的主题加入安卓ntfy客户端订阅。

### 19.2 把主题安全保存到服务器

```bash
mkdir -p ~/.config/ntfy
printf '%s\n' "$NTFY_TOPIC" > ~/.config/ntfy/topic
chmod 600 ~/.config/ntfy/topic
```

解释：

- `chmod 600`表示只有当前用户能读写。

### 19.3 创建通知函数

在 `~/.bashrc` 末尾加入：

```bash
notify-run() {
  if [ "$#" -eq 0 ]; then
    echo "用法：notify-run 命令 参数..."
    return 2
  fi

  local topic start end code duration
  topic="$(cat "$HOME/.config/ntfy/topic" 2>/dev/null)"
  start="$(date +%s)"

  "$@"
  code=$?

  end="$(date +%s)"
  duration=$((end - start))

  if [ -n "$topic" ]; then
    curl -fsS \
      -H "Title: 服务器任务结束" \
      -H "Cache: no" \
      -d "退出码：$code；耗时：${duration}秒；命令：$*" \
      "https://ntfy.sh/$topic" >/dev/null 2>&1 || true
  fi

  return "$code"
}
```

关键设计：

- 原命令的退出码会原样返回。
- ntfy发送失败不会让原任务被判定失败。
- `Cache: no`要求公共ntfy服务器不缓存这条消息。

使用：

```bash
notify-run .venv/bin/pytest
notify-run npm run build
```

---

## 20. 统一加载Bash配置并检查冲突

```bash
bash -n ~/.bashrc
```

解释：

- `bash -n`只检查语法，不执行文件。
- 没有输出通常代表语法通过。

重新加载：

```bash
source ~/.bashrc
```

按顺序检查：

```bash
command -v zoxide fzf sesh eza glow yazi lazygit delta atuin just starship
```

```bash
type z
type y
type bat
type fd
```

检查提示符是否正常，`Ctrl-R`是否打开Atuin，方向上键是否仍是普通上一条命令。

---

## 21. Termux官方插件

你的Termux来自GitHub，因此所有插件也必须下载GitHub Release版本，不能混装F-Droid版。

### 21.1 Termux:Widget：建议现在安装

作用：

- 在安卓桌面放置一键进入服务器的脚本。

安装：

1. 打开官方仓库：`https://github.com/termux/termux-widget/releases`
2. 下载最新稳定版GitHub APK。
3. 安装后允许它与Termux协同。
4. 在安卓设置中关闭Termux和Widget的电池优化。

在平板本地Termux创建脚本：

```bash
mkdir -p ~/.shortcuts
nano ~/.shortcuts/服务器工作台
```

写入：

```bash
#!/data/data/com.termux/files/usr/bin/bash
exec ssh -t codexdev@你的服务器地址 \
  'tmux new-session -A -s tablet-dev'
```

解释：

- `ssh -t`为远程tmux分配可交互终端。
- `exec`让脚本直接被SSH进程替换。
- `tmux new-session -A`表示存在就连接，不存在就创建。

权限：

```bash
chmod 700 ~/.shortcuts/服务器工作台
```

刷新安卓桌面Widget后即可点击。

### 21.2 Termux:API：建议第二阶段安装

1. 从官方GitHub Release安装Termux:API APK。
2. 在平板Termux运行：

```bash
pkg install termux-api
```

它可用于：

- 读写剪贴板；
- 安卓本地通知；
- 电量、网络和振动；
- 分享文件和打开网址。

当前服务器ntfy通知不依赖Termux:API。

### 21.3 Termux:Float：可选

适合：

- 在ChatGPT或浏览器上方临时显示一个小终端；
- 快速复制命令、看短输出。

不适合：

- 长时间阅读Codex输出；
- 复杂tmux分屏；
- 替代主Termux窗口。

### 21.4 Termux:Styling：可选

作用：

- 调整Termux字体和颜色。
- 不增加任何开发能力。

字体选择优先保证：

- 中文可读；
- `0/O`、`1/l/I`容易区分；
- 字号不要太小。

---

# 第三部分：完整日常使用手册

> [!info] 关于本部分的折叠方式
> 下方每个工具章节都使用 Obsidian 原生可折叠 Callout。
> 标题中的 `-` 使章节在打开文档时默认折叠；点击章节标题即可展开。
> 这种写法能够在折叠内容中继续正常渲染标题、列表、表格和代码块。


## 推荐学习顺序

1. Termux、SSH、tmux和 `ts` 会话选择器；
2. Codex CLI；
3. Glow、Yazi、bat、eza、fd；
4. lazygit和delta；
5. zoxide、sesh、fzf；
6. Atuin；
7. just；
8. ntfy；
9. Starship；
10. tmux恢复插件。

## 详细介绍
---

> [!abstract]- 1. Termux、SSH和服务器：三个位置必须先分清
>
> ## 详细说明
>
> Termux是平板上的终端应用。它既能运行平板本地命令，也能通过SSH连接服务器。
>
> ### 平板本地
>
> 看到：
>
> ```text
> ~ $
> ```
>
> 这里可以执行：
>
> - `pkg`
> - `ssh`
> - 修改Termux快捷键
> - 管理平板SSH私钥
>
> 这里通常没有服务器上的Codex和项目。
>
> ### 服务器普通终端
>
> 看到：
>
> ```text
> codexdev@服务器名:~$
> ```
>
> 这里可以执行：
>
> - `tmux`
> - `cd`
> - `git`
> - `codex`
> - `yazi`
> - `lazygit`
>
> ### Codex对话
>
> 顶部显示Codex，底部是：
>
> ```text
> >
> ```
>
> 这里只输入：
>
> - 中文需求；
> - `/model`
> - `/usage`
> - `/compact`
> - `/exit`
>
> ## 高频命令
>
> ### 连接服务器
>
> ```bash
> ssh codexdev@你的服务器地址
> ```
>
> ### 直接连接tmux
>
> ```bash
> ssh -t codexdev@你的服务器地址 \
>   'tmux new-session -A -s tablet-dev'
> ```
>
> ### SSH断开后重新连接
>
> 重新执行上一条命令。不要急着重新启动Codex。
>
> ### 退出服务器
>
> ```bash
> exit
> ```
>
> 它只断开当前SSH连接，不会删除服务器文件。tmux中的任务是否继续，取决于任务是否运行在tmux内。

---
### tmux
> [!abstract]- 2. tmux：服务器中的持续工作区、窗口和分屏
>
> ## 详细说明
>
> tmux结构：
>
> ```text
> tmux server
> └─ session
>    ├─ window
>    │  ├─ pane
>    │  └─ pane
>    └─ window
>       └─ pane
> ```
>
> ### tmux server
>
> tmux在服务器后台运行的总管理进程。它管理所有session。
>
> ### session
>
> 一整套持续存在的工作区。
>
> 推荐：
>
> ```text
> daily-plan
> xitong
> maintenance
> ```
>
> 一个项目对应一个session，比把所有项目塞入 `tablet-dev` 更清楚。
>
> ### window
>
> session内部的标签页，不是Android窗口。
>
> 推荐一个项目内：
>
> ```text
> 1: codex
> 2: test
> 3: git
> 4: logs
> ```
>
> ### pane
>
> window内部的分屏区域。每个pane都是独立终端。
>
> ### Codex对话
>
> Codex对话是运行在某个pane中的Codex程序内部历史，和tmux session完全不同。
>
> ### 六种容易混淆的操作
>
> | 操作 | 结果 |
> |---|---|
> | SSH断线 | tmux中的任务通常继续 |
> | `Ctrl-b d` | 只离开tmux，任务继续 |
> | Codex `/exit` | 退出Codex程序，回到pane中的Shell |
> | 在Shell输入 `exit` | 关闭当前pane中的Shell；最后一个进程结束时pane关闭 |
> | tmux关闭pane | pane内程序立即终止 |
> | tmux删除session | session内所有window、pane和程序终止 |
>
> ## tmux快捷键规则
>
> 默认前缀是：
>
> ```text
> Ctrl-b
> ```
>
> 所有快捷键都按：
>
> ```text
> Ctrl-b，松开，再按下一颗键
> ```
>
> 不是同时长按三颗键。
>
> Termux快捷栏中的 `TMUX` 已经等于 `Ctrl-b`。
>
> ## 先学这条会话工作流
>
> 不要在刚登录后直接输入裸命令 `tmux`。它会创建新的数字会话，久而久之会出现 `1`、`2`、`7` 这类难懂的工作区。
>
> 刚SSH登录、还不在tmux中时，先输入：
>
> ```bash
> ts
> ```
>
> `ts`显示所有**正在运行**的tmux会话，并按最近活动排序。直接输入 `bui` 之类的片段筛选，`Enter`进入；下半屏会显示选中会话的最近输出。`Esc`取消；`Ctrl-d`删除整个选中会话，必须输入 `y` 确认。
>
> 这解决“我不记得上次在哪个项目”的问题。目录切换是另一件事：进入一个普通Shell后使用 `y`（Yazi），不要让会话选择器混入目录。
>
> ## 每天最常用
>
> ### 创建或连接session
>
> ```bash
> tmux new-session -A -s daily-plan \
>   -c /srv/workspaces/daily-plan
> ```
>
> - `-A`：存在就连接。
> - `-s`：指定session名称。
> - `-c`：指定初始目录。
>
> ### 暂时离开
>
> ```text
> Prefix + d
> ```
>
> 即：
>
> ```text
> TMUX，再按 d
> ```
>
> ### 查看session
>
> ```bash
> tmux list-sessions
> ```
>
> 快捷键：
>
> ```text
> Prefix + s
> ```
>
> ### 查看window
>
> ```text
> Prefix + w
> ```
>
> 这是tmux原生的会话树，不只是窗口列表。进入后**不要再按Prefix**：
>
> | 按键 | 作用 |
> |---|---|
> | `↑` / `↓` | 移动选择 |
> | `Ctrl-s` | 按名称搜索会话、窗口或pane |
> | `Enter` | 进入选中项目 |
> | `x` | 删除选中的会话、窗口或pane；随后按 `y` 确认 |
> | `q` | 退出会话树 |
>
> 选中会话的顶层行时，`x`删除整个会话；选中它下面的窗口行时，只删除该窗口。删除会话会终止其中的Codex、Shell和任务。
>
> ### 新建window
>
> ```text
> Prefix + c
> ```
>
> 推荐随后重命名：
>
> ```text
> Prefix + ,
> ```
>
> ### 关闭当前window
>
> 最自然的方法是在其中的普通Shell输入：
>
> ```bash
> exit
> ```
>
> 若当前运行Codex，先在Codex中 `/exit` 或按 `Ctrl-c`，再 `exit`。也可以使用 `Prefix + &`，tmux会询问确认并关闭整个当前window。
>
> ### 切换window
>
> ```text
> Prefix + n    下一个
> Prefix + p    上一个
> Prefix + 1    第1个窗口
> Prefix + 2    第2个窗口
> ```
>
> ### 左右分屏
>
> 本配置使用：
>
> ```text
> Prefix + |
> ```
>
> ### 上下分屏
>
> ```text
> Prefix + -
> ```
>
> ### 在pane之间切换
>
> ```text
> Prefix + 方向键
> ```
>
> ### 暂时放大当前pane
>
> ```text
> Prefix + z
> ```
>
> 再次执行恢复分屏。
>
> ## 偶尔使用
>
> ### 重命名session
>
> ```text
> Prefix + $
> ```
>
> ### 重命名window
>
> ```text
> Prefix + ,
> ```
>
> ### 关闭当前pane
>
> 先确保pane中没有未保存任务：
>
> ```text
> Prefix + x
> ```
>
> tmux会询问确认。
>
> ### 调整pane大小
>
> 本配置中：
>
> ```text
> Prefix + H    向左扩展
> Prefix + J    向下扩展
> Prefix + K    向上扩展
> Prefix + L    向右扩展
> ```
>
> 由于设置了 `bind -r`，按一次前缀后可以连续按大写字母调整。
>
> ### 交换pane
>
> ```text
> Prefix + {
> Prefix + }
> ```
>
> ### 把当前pane变成新window
>
> ```text
> Prefix + !
> ```
>
> ### 显示pane编号
>
> ```text
> Prefix + q
> ```
>
> ## 查看历史输出
>
> 进入复制模式：
>
> ```text
> Prefix + [
> ```
>
> 之后可以：
>
> - 方向键滚动；
> - `PGUP`、`PGDN`翻页；
> - `q`或`ESC`退出。
>
> 也可以用手指在Termux中向上滑查看终端滚动历史，但复制模式更稳定。
>
> ## 查看所有快捷键
>
> ```text
> Prefix + ?
> ```
>
> 按 `q`退出帮助。
>
> ## 重新加载配置
>
> ```text
> Prefix + r
> ```
>
> ### 当前项目的文档和文件浮窗
>
> ```text
> Prefix + g    打开Glow Markdown文档库
> Prefix + y    打开Yazi文件浏览器
> ```
>
> 两者都从当前pane所在项目目录打开；在浮窗中按 `q`退出，立刻回到Codex。它们用于临时查看，不会替换当前Codex，也不会改变原pane的目录。
>
> ## session命令
>
> ### 创建但不连接
>
> ```bash
> tmux new-session -d -s daily-plan \
>   -c /srv/workspaces/daily-plan
> ```
>
> `-d`表示后台创建。
>
> ### 连接
>
> ```bash
> tmux attach -t daily-plan
> ```
>
> ### 切换
>
> 在tmux内：
>
> ```bash
> tmux switch-client -t xitong
> ```
>
> ### 删除session：危险
>
> ```bash
> tmux kill-session -t daily-plan
> ```
>
> 它会终止里面所有程序。初期尽量通过正常退出程序和window处理。
>
> ## 推荐项目结构
>
> ### daily-plan
>
> ```text
> session: daily-plan
> ├─ window 1: codex
> ├─ window 2: test
> ├─ window 3: git
> └─ window 4: logs
> ```
>
> ### xitong
>
> ```text
> session: xitong
> ├─ window 1: codex
> ├─ window 2: backend
> ├─ window 3: frontend
> └─ window 4: git
> ```
>
> 不要同时在两个window中启动指向同一项目的多个Codex，除非明确知道它们不会同时修改同一文件。
>
> ## tmux-resurrect
>
> 手动保存：
>
> ```text
> Prefix + Ctrl-s
> ```
>
> 手动恢复：
>
> ```text
> Prefix + Ctrl-r
> ```
>
> 它主要恢复：
>
> - session、window、pane；
> - 目录；
> - 布局；
> - 部分保守程序；
> - 可选pane文本。
>
> 它不会可靠保存：
>
> - 正在运行进程的内存；
> - 未保存的编辑器缓冲；
> - ChatGPT账号权限；
> - 同一段Codex对话的云端可用性；
> - GitHub远端代码。
>
> ## tmux-continuum
>
> 默认每15分钟调用resurrect保存一次。
>
> 自动恢复只发生在tmux server启动时。重新读取 `.tmux.conf` 不会触发一次完整自动恢复。

---
### codex cli
> [!abstract]- 3. Codex CLI：在正确项目中与AI协作
>
> ## 详细说明
>
> Codex应在服务器项目目录中启动。
>
> ### 开新对话
>
> ```bash
> cd /srv/workspaces/daily-plan
> codex
> ```
>
> ### 恢复旧对话
>
> ```bash
> codex resume --all -C /srv/workspaces/daily-plan
> ```
>
> ### 和tmux的关系
>
> ```text
> tmux pane
> └─ Codex程序
>    └─ Codex对话
> ```
>
> 关闭tmux pane会终止Codex进程。
>
> tmux detach不会终止Codex。
>
> Codex `/exit`会退出程序，但历史通常仍保存在 `~/.codex`。
>
> ## 推荐开工模板
>
> ```text
> 请先阅读 README.md、HANDOFF.md 和 docs/README.md。
> 先说明当前状态、准备调查的文件和验证方式。
> 现在不要修改、不要提交、不要触碰生产目录或服务。
> ```
>
> ## 完成后验收
>
> ```text
> 请列出改动文件、每项改动、测试命令和结果、剩余风险，
> 并给出 git diff 摘要。不要提交或推送。
> ```

---
### yazi
> [!abstract]- 4. Yazi：终端中的文件管理器
>
> ## 详细说明
>
> Yazi相当于终端中的文件资源管理器。
>
> 三栏通常表示：
>
> ```text
> 左栏：父目录
> 中栏：当前目录
> 右栏：当前文件或目录预览
> ```
>
> 启动建议使用：
>
> ```bash
> y
> ```
>
> 而不是直接 `yazi`。因为 `y`包装函数会让你退出后停留在Yazi最后所在目录。
>
> 这里的“普通Shell”是看到 `codexdev@服务器名:路径$` 的命令提示符，不是Codex对话输入框，也不是 `Prefix + y` 浮窗。实用流程是：在普通Shell输入 `y`，进入目标项目目录后按 `q`，当前Shell就已经位于该目录；随后在这里运行 `codex`。
>
> `Prefix + y` 与直接输入 `y` 的区别：前者是临时浏览浮窗，退出后不改变原pane目录；后者运行在当前Shell内，退出后会自动 `cd` 到Yazi最后所在目录。
>
> ## 每天最常用
>
> | 按键 | 作用 |
> |---|---|
> | `↑` / `k` | 上一个文件 |
> | `↓` / `j` | 下一个文件 |
> | `→` / `l` | 进入目录 |
> | `←` / `h` | 返回父目录 |
> | `Enter` | 打开文件或目录 |
> | `q` | 退出，并让Shell进入当前目录 |
> | `Q` | 退出，但不改变Shell目录 |
> | `F1`或`~` | 打开帮助 |
> | `.` | 显示或隐藏点文件 |
> | `Tab` | 查看文件信息 |
>
> ## 搜索
>
> ```text
> f
> ```
>
> 按当前文件名过滤。
>
> ```text
> /
> ```
>
> 查找下一个匹配文件。
>
> ```text
> s
> ```
>
> 通过fd按文件名搜索。
>
> ```text
> S
> ```
>
> 通过ripgrep按文件内容搜索。
>
> ## 预览
>
> 选中文本、Markdown或代码文件时，右侧自动预览。
>
> ```text
> J / K
> ```
>
> 在右侧预览中向下或向上移动。
>
> ## 初期禁止使用
>
> | 按键 | 风险 |
> |---|---|
> | `D` | 永久删除 |
> | `P` | 覆盖粘贴 |
> | `x` | 剪切文件 |
> | `r` | 批量重命名 |
> | `d` | 移入回收站，仍然可能造成误操作 |
>
> 初期只使用浏览、预览、进入目录和搜索。

---
### 查看查找优化
> [!abstract]- 5. bat、Glow、eza、fd：安全查看和查找
>
> ## bat
>
> 作用：带行号和语法高亮地查看文件。
>
> ```bash
> bat README.md
> bat app/main.py
> ```
>
> 只读，不修改文件。
>
> 只显示指定范围：
>
> ```bash
> bat --line-range 1:160 README.md
> ```
>
> ## Glow
>
> 作用：格式化阅读Markdown。
>
> ```bash
> glow README.md
> glow -w 80 HANDOFF.md
> ```
>
> - `-w 80`限制显示宽度，适合平板。
> - Glow中通常按 `q`退出，按 `?`看帮助。
>
> 已在tmux中时，优先使用：
>
> ```text
> Prefix + g
> ```
>
> 它在当前项目目录启动Glow的Markdown文档库。已知文件名时也可在普通Shell中直接阅读：
>
> ```bash
> glow -p README.md
> glow -p HANDOFF.md
> ```
>
> ## eza
>
> 作用：替代 `ls`，显示更清晰。
>
> ```bash
> eza
> eza -lah
> eza -lah --git
> eza --tree --level=2
> ```
>
> 本手册提供别名：
>
> ```bash
> ll
> tree2
> ```
>
> ## fd
>
> 作用：按文件名查找。
>
> ```bash
> fd README
> fd '\.py$'
> fd -t d docs
> ```
>
> - `-t d`只查目录。
> - 正则 `\.py$`表示以 `.py`结尾。
>
> 这些命令默认只查找，不修改文件。

---
### git
> [!abstract]- 6. lazygit和delta：审查AI对代码的修改
>
> ## 详细说明
>
> delta只改善普通Git输出。
>
> lazygit是交互式Git界面。
>
> ### delta日常使用
>
> 安装配置后，普通命令自动经过delta：
>
> ```bash
> git diff
> git show
> git log -p
> ```
>
> delta中：
>
> ```text
> n
> ```
>
> 跳到下一个diff区域。
>
> ```text
> N
> ```
>
> 跳到上一个区域。
>
> ```text
> q
> ```
>
> 退出。
>
> ### lazygit界面
>
> 在Git项目中：
>
> ```bash
> lazygit
> ```
>
> 主要面板：
>
> 1. 状态；
> 2. 文件；
> 3. 分支；
> 4. 提交；
> 5. stash。
>
> ## 每天最常用
>
> | 按键 | 作用 |
> |---|---|
> | `1`到`5` | 切换面板 |
> | `Tab` | 下一个面板 |
> | `↑`、`↓` | 移动 |
> | `Enter` | 打开详情 |
> | `Space` | 暂存或取消暂存文件 |
> | `?` | 当前面板帮助 |
> | `/` | 过滤 |
> | `q` | 退出 |
>
> ### 安全提交流程
>
> 1. 进入文件面板；
> 2. 查看每个文件diff；
> 3. `Space`只暂存确认过的文件；
> 4. 按 `c`写提交信息；
> 5. 不确定时退出，再使用普通 `git status`检查。
>
> ## 初期不要使用
>
> - Discard；
> - Reset；
> - Rebase；
> - Force push；
> - 删除分支；
> - 清空stash。
>
> 尤其不要凭直觉按大写快捷键。按 `?`先看当前面板说明。

---
### 快捷进入优化
> [!abstract]- 7. zoxide、sesh和fzf：快速进入项目和tmux会话
>
> ## 先分清三者的职责
>
> - `ts`：只找回**正在运行**的tmux会话。刚SSH登录、不知道上次在哪时优先用它。
> - `y`（Yazi）：在当前普通Shell中浏览目录；退出后把这个Shell带到选中的目录。
> - `sesh`：管理已登记项目、常用目录和tmux会话的较高层工具；它可用，但不是日常找回旧会话的必经入口。
> - `fzf`：只是一种“输入几字过滤、回车选择”的界面；`ts`正是用它来搜索tmux会话。
>
> ## zoxide
>
> 它会根据使用频率记住目录。
>
> ### 最常用
>
> ```bash
> z daily
> z xitong
> ```
>
> 第一次安装后还没有数据，可以手动加入：
>
> ```bash
> zoxide add /srv/workspaces/daily-plan
> zoxide add /srv/workspaces/xitong
> ```
>
> 交互选择：
>
> ```bash
> zi
> ```
>
> 它会调用fzf。
>
> ## fzf
>
> fzf是通用模糊选择器。
>
> 简单测试：
>
> ```bash
> printf '%s\n' daily-plan xitong maintenance | fzf
> ```
>
> 输入部分文字，方向键选择，回车确认，ESC取消。
>
> 本手册不启用fzf的Ctrl-R快捷键，它只被zoxide、sesh等工具调用。
>
> ## sesh
>
> sesh把目录、已配置项目和tmux session结合起来。它更适合“我想从项目目录新开或连接工作区”；若只是恢复正在运行的会话，优先使用 `ts`，列表更干净，也不会把目录混进来。
>
> ### 查看项目与session
>
> ```bash
> sesh list
> ```
>
> ### 连接daily-plan
>
> ```bash
> sesh connect daily-plan
> ```
>
> 如果session不存在，sesh会在配置目录中创建。
>
> ### 打开内置选择器
>
> ```bash
> sesh picker
> ```
>
> 在tmux中：
>
> ```text
> Prefix + T
> ```
>
> 打开弹出选择器。
>
> ### 最近两个session之间切换
>
> ```bash
> sesh last
> ```
>
> ### 管理window
>
> 查看当前session的window：
>
> ```bash
> sesh window
> ```
>
> 切换到指定window：
>
> ```bash
> sesh window git
> ```
>
> 初期只使用配置好的 `daily-plan` 和 `xitong`，不要使用 `sesh mkdir`随意创建新项目目录。

---
### Atuin
> [!abstract]- 8. Atuin：搜索以前成功运行过的命令
>
> ## 详细说明
>
> 普通Shell历史只保存命令文字。Atuin还保存：
>
> - 当时所在目录；
> - 执行时间；
> - 命令耗时；
> - 退出码；
> - 当前session。
>
> 本手册只使用本地SQLite数据库：
>
> ```text
> ~/.local/share/atuin/history.db
> ```
>
> 不注册、不登录、不云同步。
>
> ## 每天最常用
>
> 打开搜索：
>
> ```text
> Ctrl-R
> ```
>
> 输入关键词，例如：
>
> ```text
> pytest
> ```
>
> ### 选择命令
>
> - 方向键移动；
> - `Tab`或右方向键：把命令放回输入行，先修改；
> - 因为配置了 `enter_accept = false`，回车也不会直接盲目执行；
> - `ESC`退出。
>
> ### 导入旧历史
>
> ```bash
> atuin import auto
> ```
>
> ### 查看统计
>
> ```bash
> atuin stats
> ```
>
> ## 敏感命令
>
> 不要在命令行中直接写Token。优先让需要密码的程序交互式询问。
>
> 临时不想记录某条命令时，可在命令前加一个空格；但Bash和某些钩子的细节可能不同，敏感信息仍应避免直接出现在命令文本中。
>
> ## 以后开启同步前
>
> 必须先备份Atuin加密密钥。密钥丢失后，官方也无法恢复同步数据。

---
### just
> [!abstract]- 9. just：把复杂项目命令变成固定短命令
>
> ## 详细说明
>
> `just`是命令运行器。
>
> 项目根目录中的：
>
> ```text
> justfile
> ```
>
> 保存常用任务。
>
> 例如daily-plan：
>
> ```make
> default:
>     @just --list
>
> status:
>     git status
>
> test:
>     .venv/bin/pytest
>
> dev:
>     APP_RUNTIME_MODE=development .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001
> ```
>
> 以后只需：
>
> ```bash
> just test
> just dev
> ```
>
> ## 最常用
>
> 查看任务：
>
> ```bash
> just --list
> ```
>
> 运行任务：
>
> ```bash
> just test
> ```
>
> 检查justfile：
>
> ```bash
> just --summary
> ```
>
> 显示将执行什么：
>
> ```bash
> just --dry-run test
> ```
>
> ## 与其他脚本的关系
>
> - just可以调用 `pytest`；
> - just可以调用 `npm run build`；
> - just不会替代npm或Python；
> - just只是把复杂命令统一登记。
>
> 为项目创建justfile前，先让Codex读取README和现有脚本，不要重复发明已有命令。

---
### ntfy
> [!abstract]- 10. ntfy：任务完成后通知平板
>
> ## 使用
>
> ```bash
> notify-run .venv/bin/pytest
> ```
>
> 结束后安卓ntfy收到：
>
> ```text
> 退出码：0
> 耗时：...
> 命令：...
> ```
>
> ### 退出码
>
> - `0`通常表示成功；
> - 非0表示命令失败或被中断。
>
> 通知失败不会改变原命令退出码。
>
> ### 适合
>
> - pytest；
> - npm build；
> - 较长的安装；
> - 数据处理；
> - Codex要求你等待的独立终端命令。
>
> ### 不适合
>
> - 在Codex交互界面外面包一层 `notify-run codex`；
> - 含密码或Token的命令；
> - 高频几秒钟小命令。

---
###  starship
> [!abstract]- 11. Starship：精简提示符和路径防呆
>
> ## 详细说明
>
> Starship不是终端，也不是Shell。
>
> 它只改变提示符，例如：
>
> ```text
> server daily-plan main * ❯
> ```
>
> 你可以从中判断：
>
> - 是否正在SSH服务器；
> - 当前项目目录；
> - Git分支；
> - 是否有未提交修改；
> - 上一条命令是否失败。
>
> ## 日常使用
>
> 不需要单独运行。
>
> 查看当前配置：
>
> ```bash
> starship config
> ```
>
> 临时关闭Starship排查问题：
>
> ```bash
> bash --noprofile --norc
> ```
>
> 这会打开不读取用户配置的干净Bash。输入 `exit`返回。
>
> 如果提示符太长，修改：
>
> ```text
> ~/.config/starship.toml
> ```
>
> 不要安装大量图标主题。平板上信息密度比美观更重要。

---

> [!abstract]- 12. Termux官方插件：平板侧增强
>
> ## Termux:Widget
>
> 最有价值。
>
> 点击安卓桌面图标即可：
>
> ```text
> 连接SSH
> → 创建或接入tablet-dev
> ```
>
> 脚本放在：
>
> ```text
> ~/.shortcuts/
> ```
>
> ## Termux:API
>
> 需要时再学：
>
> ```bash
> termux-clipboard-get
> termux-clipboard-set "文字"
> termux-notification --title "标题" --content "内容"
> termux-battery-status
> ```
>
> 这些命令只在平板本地Termux中有效，不在服务器中有效。
>
> ## Termux:Float
>
> 用于临时小窗口，不作为主开发界面。
>
> ## Termux:Styling
>
> 只处理字体和颜色，不影响服务器环境。

---

# 第四部分：日常最短工作流

## 进入服务器并找回工作现场

```text
服务器工作台
```

登录服务器后，先在普通Shell输入：

```bash
ts
```

输入会话名的一部分筛选，回车进入上次留下的tmux工作现场。只有明确知道目标时，才直接使用 `tmux attach -t 会话名`。

## 临时查看文档或文件

在tmux中：

```text
Prefix + g    查看当前项目的Markdown文档
Prefix + y    临时浏览当前项目文件
```

若要让普通Shell真正进入某个目录，再直接输入：

```bash
y
```

## 启动Codex

```bash
codex
```

## AI完成后审查

```bash
git status
git diff --stat
lazygit
```

## 运行测试并接收通知

```bash
notify-run just test
```

如果项目还没有justfile：

```bash
notify-run .venv/bin/pytest
```

## 暂时离开

```text
上滑Termux快捷栏中的TMUX
```

或：

```text
Prefix + d
```

任务继续在服务器运行。

---

# 第五部分：故障和回退

## Bash一打开就报错

使用：

```bash
bash --noprofile --norc
```

然后恢复：

```bash
cp ~/config-backups/.bashrc.某个时间 ~/.bashrc
```

## tmux配置出错

```bash
tmux -L clean -f /dev/null new
```

解释：

- 创建一个不读取原配置的独立干净tmux实例。

恢复配置备份后：

```bash
tmux source-file ~/.tmux.conf
```

## Starship导致提示符异常

在 `~/.bashrc` 中注释：

```bash
eval "$(starship init bash)"
```

## Atuin快捷键异常

在 `~/.bashrc` 中注释Atuin初始化行，重新打开Shell。Atuin数据库不会因此删除。

## delta显示异常

```bash
git config --global --unset core.pager
git config --global --unset interactive.diffFilter
```

这只恢复Git默认显示。

## Yazi异常

直接使用：

```bash
cd
ls
```

Yazi不是系统依赖，删除 `~/.local/bin/yazi` 和 `ya`即可卸载。

## `ts` 会话选择器异常

重新加载Bash后再试：

```bash
source ~/.bashrc
ts
```

若提示没有会话，先检查：

```bash
tmux list-sessions
```

`ts`只是选择和附着层；原生回退方式始终可用：

```bash
tmux attach -t 会话名
```

若脚本本身被删，可按第二部分“登录后选择已有tmux会话：`ts`”重建 `~/.local/bin/tmux-session-picker`，然后执行 `chmod 755 ~/.local/bin/tmux-session-picker`。

## sesh异常

仍然可以使用原生：

```bash
tmux list-sessions
tmux attach -t session名称
```

sesh只是辅助管理层。

---

# 第六部分：长期备份

至少备份：

```text
~/.bashrc
~/.profile
~/.tmux.conf
~/.config/sesh/
~/.config/starship.toml
~/.config/atuin/
~/.local/share/atuin/
~/.local/bin/tmux-session-picker
~/.config/ntfy/
~/.termux/termux.properties
~/.shortcuts/
~/.codex/
```

敏感内容：

- `~/.config/ntfy/topic`
- Atuin未来可能产生的同步密钥；
- `~/.codex/auth.json`
- SSH私钥

不能上传到公开GitHub。

建议建立私人dotfiles仓库时排除所有凭据，只保存不敏感配置模板。

---

# 官方资料索引

- Termux：`https://github.com/termux/termux-app`
- Termux:Widget：`https://github.com/termux/termux-widget`
- Termux:API：`https://github.com/termux/termux-api`
- Termux:Float：`https://github.com/termux/termux-float`
- Termux:Styling：`https://github.com/termux/termux-styling`
- tmux：`https://github.com/tmux/tmux/wiki`
- TPM：`https://github.com/tmux-plugins/tpm`
- tmux-resurrect：`https://github.com/tmux-plugins/tmux-resurrect`
- tmux-continuum：`https://github.com/tmux-plugins/tmux-continuum`
- sesh：`https://github.com/joshmedeski/sesh`
- zoxide：`https://github.com/ajeetdsouza/zoxide`
- fzf：`https://github.com/junegunn/fzf`
- lazygit：`https://github.com/jesseduffield/lazygit`
- delta：`https://dandavison.github.io/delta/`
- Yazi：`https://yazi-rs.github.io/`
- Glow：`https://github.com/charmbracelet/glow`
- bat：`https://github.com/sharkdp/bat`
- fd：`https://github.com/sharkdp/fd`
- eza：`https://github.com/eza-community/eza`
- Atuin：`https://docs.atuin.sh/`
- just：`https://just.systems/man/`
- Starship：`https://starship.rs/`
- ntfy：`https://docs.ntfy.sh/`
