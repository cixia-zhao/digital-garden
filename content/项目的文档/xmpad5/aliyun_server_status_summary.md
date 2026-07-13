# 阿里云服务器当前状态总结 (Server Status Snapshot)

这份文档是对当前云服务器（120.55.53.215）内部环境的纯粹快照，不包含任何外部设备（电脑/平板）的操作流程，仅记录服务器本体的状态。

## 1. 基础运行环境 (Base Environment)
- **实例类型**：阿里云轻量应用服务器（杭州地域）
- **操作系统**：Ubuntu 24.04 LTS
- **网络特性**：底层 DNS 由 `systemd-resolved` 接管，当前默认的内网上游 DNS 对部分海外开源仓库（如 GitHub 及其部分代理域名）存在网络限速或拦截。

## 2. 核心服务状态 (Core Service)
- **服务名称**：`code-server` (基于开源版的 VS Code Web 架构)
- **运行身份**：`root`
- **系统级驻留**：已通过 `systemctl enable --now code-server@root` 设置为开机自启和后台常驻。
- **访问端口**：服务端本地监听 `8080` 端口（通过外部 SSH 隧道加密访问，不对公网直接暴露 8080 端口，保证极致安全）。
- **密码位置**：`~/.config/code-server/config.yaml`

## 3. 算法工作区结构 (Workspace Structure)
- **主工作区路径**：`/root/algorithm_code/`
- **代码存储路径**：`/root/algorithm_code/code/`
- **配置路径**：`/root/algorithm_code/.vscode/`
  - 包含了适配 Linux 原生 `g++` 的 `settings.json`
  - 包含了 CPH 竞赛刷题专用代码模板 `cph-template-cpp11.cpp`

## 4. 已安装的底层插件栈 (Installed Extensions)
服务器的 `code-server` 环境内已通过离线 `.vsix` 文件及内置市场安装了以下极简插件栈：
1. **`clangd`**：替代微软官方 C/C++ 插件，提供极速的 Linux 端 C++ 代码补全、高亮和跳转。
2. **`Competitive Programming Helper (cph)`**：负责自动拉取洛谷测试样例并在服务器端极速本地评测。
3. **`luogu` (洛谷)**：提供云端 IDE 内直接查看题面与一键提交功能。
4. **`Code Runner`**：提供备用的单文件一键编译运行能力。

## 5. 编译环境能力 (Compilation Engine)
- 彻底移除了原 Windows 环境的 MinGW 依赖。
- 现已全部切换为 Ubuntu 原生的 `g++` 编译器。
- **默认编译参数**：固定使用 `-std=c++11`，不默认开启 `O2` 优化，追求纯粹的竞赛环境复刻与绝对的稳定调错。

## 6. 环境定位 (Server Positioning)
该服务器当前被严格定义为**“纯粹的无头算法刷题引擎”**。
服务器上**没有任何 AI Agent**，剥离了所有繁重的自动化脚本。只负责提供最快、最稳定的 C++ 编译能力和洛谷原生接入，将算力负担 100% 留存在云端。
