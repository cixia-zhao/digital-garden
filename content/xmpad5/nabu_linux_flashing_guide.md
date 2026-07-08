# 小米平板 5 (nabu) 原生 Linux 刷机及双系统部署指南

本指南旨在指导你将小米平板 5（代号：`nabu`）刷入原生 Linux（推荐使用 Ubuntu/Arch Linux ARM），实现 Linux 单系统或与 Android 双系统共存，以便在没有台式电脑的暑假期间进行计算机学习。

> [!CAUTION]
> **风险提示**：刷机涉及解锁 Bootloader 和重新划分 UFS 闪存分区，**会清除平板上的所有数据**。请务必在操作前备份重要数据。如果操作失误，可能面临变砖风险。

---

## 阶段一：解锁 Bootloader (BL)

解锁 BL 是所有刷机操作的前提。由于你的系统是澎湃OS 1.0（HyperOS 1.0），官方的解锁政策非常严格（需要小米社区等级 5 级并答题）。

对此，玩机圈的大佬“莫离然然”提供了一个非常巧妙的**免解锁降级曲线救国方案**：

### 核心绕过逻辑 (曲线解锁)
> [!NOTE]
> 运行原生 Linux（UEFI）要求处理器必须放行未签名的镜像，这在硬件级别**强绑定 Bootloader 解锁状态**。因此，没有任何方法可以“在锁 BL 的状态下直接运行 Linux”。
> 但你可以使用莫离然然开发的 **“小米QC免解工具”**，在**锁定 BL** 的状态下，利用高通（QC）的底层漏洞强制将平板**降级回 MIUI 14**。
> 回到 MIUI 14 后，解锁限制会大大降低（不需要社区 5 级和答题），你可以直接在开发者选项绑定并使用官方 Mi Flash Unlock 工具进行解锁。

### 具体步骤：

#### 步骤 1. 利用莫离然然工具免解降级
1. 访问莫离然然的资源博客（[moliranran.com](https://www.moliranran.com)），下载 **“小米QC免解工具”** 及其配套的 **小米平板 5 MIUI 14 工程包或降级引导文件**。
2. 按照其博客中的《Xiaomi免解BL工具-降级教程》进行操作：
   * 工具通常利用高通漏洞将设备引导进 EDL（9008）模式，或通过临时提权注入 SELinux 宽容。
   * 写入降级镜像后，在 FastbootD 模式下挂载动态分区并清除 AVB（Android验证启动）防回滚计数。
   * 强刷回底包，使平板顺利开机进入 **MIUI 14**。

#### 步骤 2. 在 MIUI 14 下直接申请解锁
1. 平板开机进入 MIUI 14 后，登录你的小米账号。
2. 进入 **设置 -> 更多设置 -> 开发者选项 -> 设备解锁状态**，点击“绑定账号和设备”。
3. 此时不需要答题或 5 级社区号，会直接显示绑定成功。
4. 在电脑上下载官方 [小米官方解锁工具 (Mi Flash Unlock)](https://reameizu.github.io/mi-flash-unlock/)。
5. 等待规定的 **168小时 (7天)** 倒计时结束后，连接电脑一键解锁 BL。


---

## 阶段二：准备刷机工具与镜像 (在 PC 上下载)

在等待解锁的 7 天内，你可以在台式机上下载好以下所有必需的资源：

1. **ADB 与 Fastboot 命令行工具**：
   * 下载官方 [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools?hl=zh-cn)。
2. **小米平板 5 专用 Recovery**：
   * 推荐使用 **OrangeFox Recovery** 或 **TWRP** 镜像。
3. **`parted` 分区工具二进制文件**：
   * 用于在平板上进行 UFS 重新分区的工具（[下载地址参考 Linux on Nabu 官网](https://linux-on-nabu.github.io/)）。
4. **UEFI (EDK2) 引导镜像**：
   * 用于引导非安卓系统（Linux/Windows）启动的 UEFI 固件。
5. **Linux 系统镜像 (Rootfs)**：
   * 推荐：[map220v/ubuntu-xiaomi-nabu](https://github.com/map220v/ubuntu-xiaomi-nabu) 构建的 Ubuntu 镜像。

---

## 阶段三：重新分区与部署系统 (解锁后操作)

> [!WARNING]
> 以下步骤将永久调整你平板的存储结构，确保你已经备份好数据！

### 1. 临时引导至 Recovery
手机进入 Fastboot 模式连接电脑，在电脑终端运行：
```bash
fastboot boot orangefox-nabu.img
```
*进入 Recovery 后，在平板上格式化 Data 分区以解除加密。*

### 2. 重新划分分区
1. 将 `parted` 工具推送到平板：
   ```bash
   adb push parted /tmp/
   adb shell chmod 755 /tmp/parted
   ```
2. 进入平板的 Shell：
   ```bash
   adb shell
   ```
3. 运行 `parted` 查看当前分区：
   ```bash
   /tmp/parted /dev/block/sda
   # 打印当前分区表，记住 userdata 分区（通常是最后一个，序号为 31）的起点
   print
   ```
4. 调整 `userdata` 大小（假设为 Android 保留 30GB，其余给 Linux）：
   ```bash
   # 删除旧的 userdata 分区
   rm 31
   # 重建较小的 userdata 分区
   mkpart userdata ext4 <原起点> <新终点>
   # 创建 Linux 分区 (例如命名为 rootfs)
   mkpart rootfs ext4 <Linux起点> <UFS总大小>
   # 创建 ESP (EFI系统分区，约 512MB) 用于存放 UEFI 引导文件
   mkpart esp fat32 <ESP起点> <ESP终点>
   ```
5. 格式化新分区并写入对应的 Linux 系统 rootfs 镜像。

### 3. 部署 UEFI 引导
* 将 UEFI 的 `boot.img` 写入平板的备用启动分区，或者通过特定脚本在每次开机时选择引导。
* 部署完成后，平板开机将先进入 UEFI 界面，你可以在其中选择进入原生 Ubuntu 桌面，或者引导回原生的 Android 系统。

---

## 阶段四：暑假离线学习建议

1. **外设准备**：
   * **USB 拓展坞**：小米平板 5 只有一个 Type-C 接口，你需要一个支持充电、USB 接口的拓展坞，用来外接键盘、鼠标或 U 盘。
   * **蓝牙键鼠**：原生的 Ubuntu 和 Arch Linux 完美支持蓝牙，连接蓝牙键盘和鼠标能最大程度减少线缆干扰。
2. **离线资源**：
   * 如果暑假期间网络环境不佳，建议在有台式机（有宽带）时，提前把需要学习的教程、PDF、离线编译器包下载到平板的 UFS 存储中。
