# 2026年04月25日上午


## 1. 📁 核心文件变更

- `batch_img_to_lvgl_c.py`（重构）
  - 实现 `icons_png` 批量转 `ui_assets`，输出 LVGL v9 `LV_COLOR_FORMAT_I1`。
  - 增加 8 Bytes 调色板头（白/黑 ARGB8888），修复 I1 显示问题。
  - 增加中文文件名处理（拼音/映射），统一英文别名（`note/read/photo/word/music`）。
  - 增加双轨预渲染：每张图生成 `64x64` 普通版 + `96x96` `*_large` 版（Nearest Neighbor）。
- `main/ui_menu.c`（重构）
  - 从“物理滚动长列表”重构为“固定 3 项虚拟窗口走马灯”。
  - 再升级为“双轨指针轮换”：上/下用 normal 图，中间用 large 图。
  - 中间选中框视觉强化（边框加粗，尺寸适配大图）。
- `main/ui_home.c`（新建）
  - 新增 400x300 Bento Box 首页骨架（状态栏 + 4 卡片）。
  - 集成主页文案（温度、日期、MEMO）和中文字体应用点。
  - 预留并接入页面路由：Home 可 `lv_screen_load()` 跳转 Menu。
- `main/ui_home.h`（新建）
  - 首页创建、路由绑定、路由触发接口声明。
- `main/ui_font_custom.c`（新建，自动生成）
  - 使用 `lv_font_conv` 生成 1bpp 裁剪中文字库（含你补充的一二三四五六日月年待办等字符）。
- `main/main.cpp`（改动）
  - 启动流程改为 Home 首屏 + Menu 目标屏。
  - 编码器/按键事件增加 Home→Menu / Menu→Home 路由分流。
- `main/CMakeLists.txt`（改动）
  - 接入 `ui_home.c`、`ui_font_custom.c`、以及 10 个图标资源（5 normal + 5 large）。

---

## 2. 🤖 高价值 Prompt 记录

今天最“高命中率”的提示词片段（非常适合沉淀为你以后和 AI 协作模板）：

- **资源转换规范明确型**
  - “生成的 C 数组必须严格符合 LVGL v9 的 `LV_COLOR_FORMAT_I1` 规范；黑像素=1，白/透明=0；每行字节数和整图大小精确约束。”
- **架构重构明确型**
  - “从长列表物理滚动改为固定 3 项无限循环虚拟窗口，保留编码器触发，使用 `lv_image_set_src()` 动态轮换 top/mid/bottom。”
- **双轨性能策略型**
  - “同一张图生成 normal + large 双轨资源，middle 绑定 large、上下绑定 normal，以预渲染换运行时性能。”

这三类 Prompt 的共同点：**约束清晰（格式/尺寸/API/状态机）、目标可验证（字节数/对象数量/路由行为）**。

---

## 3. ⚙️ 编译与依赖状态

- `main/CMakeLists.txt` 当前新增并已接入：
  - `ui_home.c`
  - `ui_font_custom.c`
  - `../ui_assets/ui_icon_note.c`
  - `../ui_assets/ui_icon_read.c`
  - `../ui_assets/ui_icon_photo.c`
  - `../ui_assets/ui_icon_word.c`
  - `../ui_assets/ui_icon_music.c`
  - `../ui_assets/ui_icon_note_large.c`
  - `../ui_assets/ui_icon_read_large.c`
  - `../ui_assets/ui_icon_photo_large.c`
  - `../ui_assets/ui_icon_word_large.c`
  - `../ui_assets/ui_icon_music_large.c`
- 字体与宏定义状态（项目是 ESP-IDF managed LVGL，走 `sdkconfig` 而非本地 `lv_conf.h`）：
  - `CONFIG_LV_FONT_MONTSERRAT_20=y`
  - `CONFIG_LV_FONT_MONTSERRAT_24=y`
  - `CONFIG_LV_FONT_MONTSERRAT_48=y`
  - `CONFIG_LV_FONT_CUSTOM_DECLARE="LV_FONT_DECLARE(ui_font_custom);"`
- 工具链状态：
  - 已安装 `pypinyin`
  - 已安装 `lv_font_conv`
  - 已生成 `main/ui_font_custom.c`

---

## 4. ⚠️ 悬而未决的代码债（明日待接入）

以下为当前“写死 Mock 数据/测试配置”，建议明天接真实数据源：

- `main/ui_home.c` `ui_home_create()`
  - `温度: 24.5°C`（固定温度）
  - `[Wi-Fi] [BAT] 97%`（固定电量/图标占位）
  - `21:51`（固定时钟）
  - `4月25日`、`2026年`（固定日期）
  - `[Avatar]`（头像占位）
  - `21:48 洗澡 / 22:10 整理桌面 / 23:00 复盘`（固定待办文本）
- `main/main.cpp` `WifiStatusTimerCb()`
  - `start_test_download("http://192.168.40.192:8080/test.bin")`（写死测试 URL）
  - `WiFi: Connecting/Connected/Error`（英文固定状态文案，可后续本地化+状态机抽象）
- `main/ui_menu.c`
  - 图标顺序与数据源映射目前写死在数组，后续可改为配置表驱动（便于扩展菜单项）。
- `batch_img_to_lvgl_c.py`
  - 英文别名映射字典（`ENGLISH_ALIAS_MAP`）是手工维护，后续可抽离成外部配置文件。

如果你愿意，我明天可以先从“**Home 页时间/日期和电量接入实时数据**”开始，优先把可视数据从 Mock 改成真实输入。

# 2026年04月25日下午

## 1. 📁 核心文件变更

- `main/ui_home.c`
  - 完成 Home Bento 布局微调：上半区时钟/日期卡片去边框，日期区三段文案按 `TOP_MID / CENTER / BOTTOM_MID` 重排。
  - 日期中间文本（`4月25日`）显式切换到 `ui_font_date_large`。
  - 下半区完成左右交换与 60/40 宽度分配：左侧为“待办”大区，右侧为 `Avatar`。
  - 修复“待办”方块字问题：为标题 `todo_title` 显式绑定 `ui_font_custom`。
- `main/ui_menu.c`
  - 采用固定 3 槽位虚拟窗口（top/mid/bottom）+ 无限索引轮换。
  - 双轨图标策略已落地：中间使用 `*_large`，上下使用 normal。
- `main/main.cpp`
  - 启动路径为 Home 首屏，Menu 作为目标页。
  - 编码器/返回键路由分流：Home 可进 Menu，非 Home 可回 Home。
  - 保留 Wi-Fi 状态与下载显示逻辑（当前仍含测试路径与硬编码内容）。
- `main/CMakeLists.txt`
  - `SRCS` 已包含 `ui_font_date_large.c`、`ui_font_custom.c`、`ui_home.c`、`ui_menu.c` 及 10 个图标资源（5 normal + 5 large）。
- `main/ui_font_custom.c`、`main/ui_font_date_large.c`
  - 字体已生成并可用，且 include 已统一为 `#include "lvgl.h"`（适配 managed LVGL）。
- `gen_lvgl_fonts.py`（新增）
  - 封装 `lv_font_conv` 字体生成流程。
  - 生成后自动规范化 include，避免再次回退为 `lvgl/lvgl.h`。
  - `ui_font_custom` 默认 symbols 已纳入 `°C℃`。

## 2. 🤖 高价值 Prompt 记录

- **问题定位型（高复现率）**
  - “报错在链接阶段/编译阶段分别检查：声明、定义、CMake 注册三者是否一致。”
- **LVGL 字体强约束型**
  - “对中文 label 强制绑定字体：`lv_obj_set_style_text_font(label, &ui_font_custom, 0);`，不要依赖继承。”
- **工程化防回归型**
  - “把一次性修复变成生成后自动后处理（脚本化），避免手工改完又被工具覆盖。”
- **布局改造可验证型**
  - “给出明确 API 和目标状态：对齐枚举、宽度比例、对象数量、路由不变，便于快速验收。”

## 3. ⚙️ 编译与依赖状态

- **工程组件状态**
  - `main` 目录关键文件齐全：`ui_home.*`、`ui_menu.*`、`main.cpp`、`ui_font_custom.c`、`ui_font_date_large.c`、`CMakeLists.txt`。
- **字体与 LVGL 配置**
  - `sdkconfig.defaults` 包含：
    - `CONFIG_LV_FONT_MONTSERRAT_20=y`
    - `CONFIG_LV_FONT_MONTSERRAT_24=y`
    - `CONFIG_LV_FONT_MONTSERRAT_48=y`
    - `CONFIG_LV_FONT_CUSTOM_DECLARE="LV_FONT_DECLARE(ui_font_custom);"`
- **今日关键故障与现状**
  - 反复报错根因已确认：直接运行 `lv_font_conv` 会重写头部为 `lvgl/lvgl.h`，导致 ESP-IDF managed LVGL 找不到头文件。
  - 当前修复路径：使用 `python gen_lvgl_fonts.py` 生成字体，自动改回 `lvgl.h`。
- **运行态观测**
  - 串口监视器正在运行，日志显示系统可启动到应用层（ESP-IDF v6.0，项目 `09_LVGL_V9_Test`，PSRAM 初始化通过）。
- **外部依赖工具**
  - 已使用并可用：`lv_font_conv`、Python 运行环境（Espressif venv）。

## 4. ⚠️ 悬而未决的代码债

- `main/ui_home.c`
  - Home 仍大量使用 Mock 文案（时间、日期、温度、电量、待办内容），未接实时数据源。
- `main/main.cpp`
  - `WifiStatusTimerCb()` 内仍有测试下载地址：`http://192.168.40.192:8080/test.bin`。
  - Wi-Fi 状态文本与流程为硬编码，尚未本地化/状态机抽象。
  - 图片渲染路径中存在“动态分配后不释放”注释与实现（`malloc` 后长期持有），需明确生命周期策略并评估长期运行风险。
- `main/ui_menu.c`
  - 菜单项与图标映射仍为静态数组写死，后续可改配置表驱动以便扩展。
- 字体生成流程
  - 若绕过 `gen_lvgl_fonts.py` 直接跑 `lv_font_conv`，仍有回归风险；建议统一团队流程只走脚本。
- 构建验证
  - 建议做一次“从干净构建目录”的全量构建与烧录回归，确认字体脚本流程与 UI 改动在 CI/新环境下也稳定。

# 2026-04-26 上午

## 1. 📁 核心文件变更

- `main/pcf85063.c`（新增）
  - 新增 PCF85063 RTC 驱动，地址 `0x51`，复用已有 I2C 总线。
  - 实现 `pcf85063_init()`、`pcf85063_read_time()`、`pcf85063_set_time()`、`pcf85063_sync_system_time()`。
  - 增加 BCD 编解码与 OS 标志恢复逻辑：当检测到振荡停止标志（OS）时，自动用系统时间或编译时间回种 RTC，再同步系统时钟。
- `main/pcf85063.h`（新增）
  - 暴露 RTC 初始化/读写/系统时间同步接口。
- `main/shtc3.c`（持续演进）
  - 仅温度读取流程稳定：`Wakeup -> 延时 -> Measure -> 延时 -> Read -> Sleep`。
  - 温度加入软件补偿偏移：减 `3.0°C`。
  - 已开启 I2C 内部上拉，并补充唤醒后延时。
- `main/shtc3.h`（改动）
  - 新增 `shtc3_i2c_get_bus_handle()`，用于给 RTC 设备复用同一 I2C master bus。
- `main/battery_monitor.c` / `main/battery_monitor.h`（新增）
  - 基于 `adc_oneshot + curve_fitting` 实现电压读取与百分比换算。
  - 10 次采样去极值平均，按分压比恢复电池电压，线性映射 3.3V~4.2V。
- `main/ui_home.c`（重构升级）
  - 状态栏接入动态温度/电量/时钟刷新。
  - 温度显示从 `%f` 改为整数拼接（`%d.%d`），规避 LVGL 浮点格式化依赖问题；异常显示 `--.-°C`。
  - 对温度 Label 每次更新前重绑 `ui_font_custom`（防样式覆盖）。
  - 新增 RTC 时钟 1s 刷新与冒号闪烁（`HH:MM` / `HH MM`）。
  - RTC 读取失败时保留上一次正确时间（并用本地秒递增兜底），避免时间跳变。
- `main/main.cpp`（改动）
  - 启动阶段接入 `shtc3_i2c_init()` 与 `pcf85063_sync_system_time()`。
  - 保持 Home 首屏路径、输入事件路由与 Wi-Fi 下载逻辑。
  - 图片内存治理已落地：先解除 LVGL 引用再释放动态资源，避免泄漏和野指针。
- `main/CMakeLists.txt`（改动）
  - `SRCS` 现已包含：`shtc3.c`、`pcf85063.c`、`battery_monitor.c`、`ui_home.c`、`ui_menu.c`、`main.cpp`、字体和 icon 资源。

---

## 2. 🤖 高价值 Prompt 记录

- **外设驱动约束型**
  - “必须使用 ESP-IDF v6 新 API（`driver/i2c_master.h` / `esp_adc/adc_oneshot.h`），禁止旧接口。”
- **时序闭环型**
  - “严格按器件协议执行完整流程（Wakeup→Measure→Read→Sleep），并补足唤醒延时。”
- **嵌入式容错型**
  - “失败返回特殊值（如 `-999.0f`），UI 侧按异常占位显示，不做危险跳变。”
- **运行态可验证型**
  - “UI 更新同时打 `ESP_LOGI`，保证界面失败时仍可从串口验证硬件链路。”
- **资源生命周期强约束型**
  - “释放顺序必须是先断开 LVGL 对象引用，再 free 动态内存，防野指针。”
- **低依赖显示策略型**
  - “避免 `%f` 格式化依赖，改成整数拼接显示，提升嵌入式稳定性。”

---

## 3. ⚙️ 编译与依赖状态

- **组件注册状态**
  - `main/CMakeLists.txt` 当前已注册 `shtc3.c / pcf85063.c / battery_monitor.c / ui_home.c / main.cpp` 及字体与图标资源。
- **I2C 外设状态**
  - SHTC3 与 PCF85063 共享同一 I2C bus（SDA13/SCL14）。
  - RTC 地址 `0x51`，SHTC3 地址 `0x70`。
- **显示链路状态**
  - 温度 UI 已从浮点格式化切换为整数格式化，且单位恢复为 `°C`。
  - 温度、时钟、电量均有定时刷新逻辑。
- **运行日志侧观察（最近）**
  - 温度采样有有效值（约 `24.x C`）；
  - 电池读数仍约 `1.82V / 0%`（待硬件侧确认是否接电池）；
  - RTC 出现过 `oscillator stop flag`，代码已补 OS 恢复写回逻辑。
- **构建工具链**
  - 项目仍为 ESP-IDF v6.0 路线；
  - 字体生成链（`gen_lvgl_fonts.py` + `lv_font_conv`）在工程内可用。

---

## 4. ⚠️ 悬而未决的代码债

- `main/ui_home.c`
  - 主页文本仍有较多 Mock 内容（待办、日期卡等）未全部接真实数据源。
- `main/main.cpp`
  - Wi-Fi 下载地址仍为测试 URL：`http://192.168.40.192:8080/test.bin`。
  - Wi-Fi 状态文案与流程尚未做本地化与状态机抽象。
- `main/pcf85063.c`
  - OS 恢复目前回种“系统时间/编译时间”，尚未接入网络授时后的“高可信回写 RTC”闭环。
- `main/ui_home.c`
  - 时钟当前秒级兜底通过本地递增，若长期 RTC 读失败，时间会漂移（建议叠加故障标识与重试策略）。
- `main/battery_monitor.c`
  - 电池百分比仍为线性模型，未做分段放电曲线校准（显示会与真实 SOC 有偏差）。
- 串口与烧录流程
  - 曾出现 `COM3` 被占用导致烧录失败；建议固化“先关 monitor 再 flash”的流程脚本化。

📊 嵌入式资源审计预估

本次累计预估增加 RAM 占用：约 `1~2 KB`（新增 RTC 状态缓存、驱动句柄、定时器回调状态）  
本次累计预估增加 Flash 占用：约 `8~16 KB`（RTC/SHTC3/电池驱动逻辑、日志字符串、UI 刷新分支）  
架构师警告：无重大新增泄漏风险；动态图片内存释放链路已补齐，但 Wi-Fi 下载与 RTC/NTP 仍建议做更系统化的错误恢复与状态抽象。