

### **Linux 命令行核心笔记 **

#### **一、文件系统导航与识别**

**1. 核心导航命令 (“四大天王”)**

*   `pwd` (Print Working Directory): **我在哪？** -> 显示当前完整路径。
*   `ls -al` (List All Long): **这里有啥？** -> 显示所有文件（含隐藏）的详细列表。
    *   **强烈建议**：养成使用 `ls -al` 的习惯，信息最全。
*   `cd` (Change Directory): **去别的地方**。
    *   `cd 文件夹名`: 进入子文件夹 (相对路径)。
    *   `cd ..`: 返回上一级 (相对路径)。
    *   `cd ~` 或 `cd`: 一键回家 (绝对路径起点)。
*   **`Tab` 键**: **自动补全**命令或文件名，是命令行的灵魂，必须多用。

**2. 解读 `ls -al` 的输出**

*   **文件类型 (第一个字母)**:
    *   `d`: 文件夹 (Directory)，通常显示为**蓝色**。
    *   `-`: 普通文件 (File)，通常显示为**白色**。
*   **文件权限**:
    *   `r`: 可读 (Read)
    *   `w`: 可写 (Write)
    *   `x`: 可执行 (Execute)，拥有 `x` 权限的文件通常显示为**绿色**。
*   **核心理念**: Linux不靠后缀名判断文件类型，而是靠文件属性。**绿色代表“可执行”**，蓝色代表“文件夹”。

**3. 路径的两种寻址方式**

*   **相对路径 (Relative Path)**: 基于**当前位置**的导航。
    *   示例: `cd my_project`, `cd ../notes`
    *   优点: 简洁，适合在附近移动。
*   **绝对路径 (Absolute Path)**: 从**根目录 (`/`)** 或**家目录 (`~`)** 开始的完整地址。
    *   示例: `cd /etc/nginx`, `cd ~/.config/nvim`
    *   优点: 精准、无歧义，无论当前在哪都能成功跳转。

#### **二、文件操作与管理 (“四件套”)**

*   `touch 文件名`: **创建**一个空的普通文件。
*   `mkdir 文件夹名`: **创建**一个新文件夹。
*   `cp 源文件 目标位置`: **复制**文件。
    *   `cp -r 源文件夹 目标位置`: 复制整个文件夹。
    *   **备份技巧**: `cp main.cpp main.backup.cpp`
*   `mv 源文件 目标位置`: **移动**文件。
    *   **重命名技巧**: `mv old_name.txt new_name.txt`
*   `rm 文件名`: **删除**文件。
    *   `rm -r 文件夹名`: **删除**整个文件夹。
    *   **【最高警告】**: `rm` 命令没有回收站，删除前请用 `pwd` 确认位置！

#### **三、补充的“神级”命令**

*   `cat 文件名`: 在终端里快速**查看**一个文件的全部内容，适合看短小的配置文件。
*   `grep "关键词" 文件名`: 在文件中**搜索**包含特定关键词的行。
    *   示例: `grep "include" main.cpp` (在main.cpp中查找所有包含"include"的行)
*   `history`: 查看你输入过的所有历史命令。
*   `clear` 或 `Ctrl + L`: **清空**终端屏幕，还你一个干净的界面。

#### **四、Git：关联远程仓库 (必备技能)**

当你本地有一个项目（比如 `MyNewProject`），并且在GitHub或Gitee上创建了一个空的远程仓库后，你需要用以下命令将它们“连接”起来。

**场景：本地已有项目，需要推送到新的远程仓库**

```bash
# 1. 进入你的本地项目文件夹
cd MyNewProject

# 2. 初始化本地仓库 (如果还没做过)
git init

# 3. 将所有文件添加到暂存区
git add .

# 4. 提交一次本地更改
git commit -m "Initial commit"

# 5. 【核心】关联远程仓库
# git remote add origin <你的远程仓库URL>
# URL 示例: git@github.com:YourName/YourRepo.git (SSH)
#           https://github.com/YourName/YourRepo.git (HTTPS)
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 6. 【核心】将本地的 main 分支推送到远程仓库
git push -u origin main
```
*   `origin`: 是你给远程仓库起的一个默认别名。
*   `-u`: 会将本地的 `main` 分支与远程的 `main` 分支关联起来，以后你只需要输入 `git push` 就能推送了。
