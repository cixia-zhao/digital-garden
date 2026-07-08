

## 1. 最终架构状态 (Current State)
- **云端算力层**：阿里云轻量应用服务器 (Ubuntu 24.04)，纯作为 C++ 编译与代码存储后端。
- **本地接入层**：小米平板 5 (MIUI/HyperOS)。
- **网络连接层**：Termux 建立 SSH 端口转发隧道 (`ssh -L 8080:127.0.0.1:8080`)。
- **前端显示层**：平板 Chrome 浏览器访问 `127.0.0.1:8080`，使用开源版 `code-server`。

## 2. 踩坑与关键网络解法 (Network Pitfalls)
- **服务端 DNS 污染**：Ubuntu 24.04 强依赖 `systemd-resolved`，阿里云内网 DNS 会屏蔽 GitHub 镜像站。强改 `/etc/resolv.conf` 无效。
- **PC 端 SCP 超时**：Windows 开启 Clash/Mihomo 等代理的 TUN 虚拟网卡时，`scp` 命令常因路由冲突导致 `Connection timed out`。
- **👉 最终解法**：彻底放弃服务端直接下载和 PC 端命令行传输。**全程在平板浏览器中直接下载目标文件（离线安装包），然后通过网页端 VS Code 内部安装。**

## 3. 环境配置关键步骤 (Key Setup Steps)
### 3.1 保持后台长连接
为防止小米平板系统杀后台
1. 开启 Termux 的 `WakeLock` 唤醒锁。
2. 系统电池设置中将 Termux 设为 **无限制**。
3. 任务列表给 Termux 卡片 **加锁**。
4. 允许 Termux **自启动**。

### 3.2 VS Code 插件离线安装
由于 `code-server` 阉割了微软官方插件市场，必须通过离线 `.vsix` 文件安装专属插件：
1. 用平板浏览器直接下载离线包：`vscode-luogu`, `competitive-programming-helper`, `synthwave-vscode`, `code-runner`。
2. 在平板网页版 VS Code 扩展面板中，点击 `...` -> `Install from VSIX` 手动安装。
3. C++ 语言支持直接在商店搜 `clangd` 安装（放弃微软官方 C/C++ 插件）。

### 3.3 全局设置 (User Settings) 迁移适配
将 Windows 下的 `settings.json` 贴入云端，并做如下核心改造：
1. **清理 Windows 路径**：剔除 `C:\...`，将 CPH 存储路径改为 Linux 格式（如 `/root/algorithm_code/code`）。
2. **重置编译器**：将 CPH 和 Code Runner 的复杂 PowerShell 编译命令精简为原生的 `g++ -std=c++11`。
3. **开启自动保存**：必须加入 `"files.autoSave": "afterDelay"`，解决平板无实体键盘按 `Ctrl+S`

