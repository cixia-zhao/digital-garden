
### **最终总结：基于 Git 的跨设备 Neovim 配置同步工作流**

#### **核心理念**

将 Neovim 的配置文件 (`~/.config/nvim`) 视为一个独立的软件项目。利用 Git 对其进行版本控制，并将 GitHub 作为中央“云端硬盘”。任何设备都通过 `git push`（上传）和 `git pull`/`clone`（下载）与这个云端中心同步，从而实现配置的完全统一。

#### **阶段一：源设备（手机）- “打包 & 封存”**

**目标**：将本地的 `~/.config/nvim` 目录初始化为一个 Git 仓库，并将其推送到 GitHub。

**【第一步：初始化本地仓库】**

进入配置目录，删除可能存在的旧的 `.git` 文件夹以确保干净，然后初始化一个新的 Git 仓库。

```bash
cd ~/.config/nvim && rm -rf .git && git init
```

**【第二步：创建 `.gitignore`，定义忽略规则】**

创建一个 `.gitignore` 文件，告诉 Git 哪些文件是设备特有的、不需要同步的。最关键的是 `lazy-lock.json`，它记录了插件的版本，应该在每台设备上由 LazyVim 自动生成。

```bash
cat <<EOF > .gitignore
# LazyVim lock file - should be generated on each machine
lazy-lock.json

# Log files & session data
*.log
.DS_Store
*.swp
EOF
```

**【第三步：关联远程仓库并首次推送 (使用 SSH 协议)】**

将本地仓库与你在 GitHub 上创建的空仓库关联起来，并完成首次推送。

```bash
# 1. 关联远程仓库 (使用 SSH 地址！)
git remote add origin git@github.com:cixia-zhao/My-vim-config.git

# 2. 添加所有文件，创建首次提交
git add .
git commit -m "feat: Initial commit of my unified Neovim config v1.0"

# 3. 推送到 GitHub
git branch -M main
git push -u origin main
```
*   **关键**：`git remote add` 使用的是 `git@github.com:...` 的 SSH 地址，这会利用你系统中已经配置好的 SSH 密钥进行免密认证。

---

#### **阶段二：目标设备（平板）- “下载 & 部署”**

**目标**：在一个全新的环境中，从 GitHub 一键拉取配置，完成自动化部署。

**【第一步：安装核心依赖】**

确保新设备拥有 Git、Neovim 和 C++ 编译器。

```bash
pkg update && pkg upgrade -y && pkg install git neovim clang -y
```

**【第二步：克隆你的配置仓库】**

这是整个流程中最核心的一步。`git clone` 会自动从 GitHub 下载你的所有配置，并精准地放到 Neovim 需要的 `~/.config/nvim` 目录下。

```bash
git clone git@github.com:cixia-zhao/My-vim-config.git ~/.config/nvim
```
*   **关键**：`clone` 时同样使用 SSH 地址，前提是你的目标设备也已经配置好了访问 GitHub 的 SSH 密钥。

**【第三步：触发自动安装】**

首次启动 Neovim。LazyVim 会自动检测到插件缺失，并开始下载、安装和编译。

```bash
nvim
```
耐心等待其完成。完成后，你的 Neovim 环境就已完全同步。

---

#### **日常维护：增量同步**

当你在一台设备上修改了配置（例如，安装了新插件，修改了快捷键），只需要：

1.  **在修改的设备上（上传）**：
    ```bash
    cd ~/.config/nvim
    git add .
    git commit -m "feat: Add new plugin XYZ"  # 写清楚你做了什么
    git push
    ```

2.  **在另一台设备上（下载）**：
    ```bash
    cd ~/.config/nvim
    git pull
    ```
    然后重新打开 Neovim，LazyVim 可能会自动处理插件的更新。

---

### **额外总结：关键配置片段**

#### **1. F11 键快捷键配置 (Termux)**

这个配置**不属于 Neovim**，而是属于 Termux 终端本身。它需要被手动同步。

*   **文件位置**: `~/.termux/termux.properties`
*   **核心内容**:
    ```properties
    extra-keys = ['ESC','F9','F10','F11','=','HOME']('ESC','F9','F10','F11','=','HOME')
    ```
*   **同步方式**: 在新设备上创建该文件，并将内容复制进去，然后**彻底重启 Termux 应用**使其生效。

#### **2. C++ 编译运行工作流 (Floaterm)**

这是我们为 F11 键绑定的核心功能。

*   **文件位置**: `~/.config/nvim/lua/plugins/keymaps.lua`
*   **核心代码**:
    ```lua
    return {
      {
        "<F11>",
        function()
          -- 保存当前文件
          vim.cmd("write")
          -- 定义编译和运行的命令
          local compile_run_cmd = "g++ % -o %:r && ./%:r"
          -- 在一个新的浮动终端中执行命令
          vim.cmd("FloatermNew --autoclose=2 " .. compile_run_cmd)
        end,
        desc = "Compile & Run C++ File",
      },
      -- ... 其他快捷键 ...
    }
    ```
    *   `%` 代表当前文件名，`%:r` 代表不带扩展名的文件名。
    *   `--autoclose=2` 表示程序运行结束后，按任意键关闭终端。


