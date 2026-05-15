import os
import pyperclip
from pathlib import Path
import time

# ================= 配置文件路径 (严格使用绝对路径) =================
# 1. 宏观开发日志 (皮卡丘/Gemini 专属，存放在外部笔记库)
DEV_LOG_PATH = Path(r"D:\code\digital-garden\content\电子\FocusCore_DevLog（开发日志）.md")

# 2. 微观执行日志 (ds 专属，存放在 ESP32 工程根目录)
# 绝对路径已根据你的截图校准，确保 .bat 运行时不会路径错乱
DS_LOG_PATH = Path(r"D:\ESP32-S3-RLCD-4.2-Demo\ESP32-S3-RLCD-4.2-Demo\02_ESP-IDF\09_LVGL_V9_Test\ds_memo_log.md")

# ================= 固定的提示词模板 =================
# 皮卡丘 (Gemini) 的深度总结指令
GEMINI_END_PROMPT = """**皮卡丘，今天的开发结束了。请帮我深度总结一份今天的 DevLog（开发者日志）。**

【执行要求】：请务必从我们今天对话的第一句话开始全量回溯。千万不要遗漏任何前置的准备工作、使用过的外部网站、以及特定的参数（如十六进制色号、精确分辨率等）。

不要有任何其他内容，这次回复只有以 Markdown 格式输出的DevLog，标题要求一级标题（ 内容包括且只限于 ： 年月日），包含以下五个核心模块：

1. 🎯 核心里程碑
2. 🧰 关键工具链与素材管线
3. 🕳️ 踩坑复盘与物理底层
4. 💻 终端指令与环境
5. 🧠 架构师新知与明日 TODO"""

# ds (Claude Code 插件) 的自动归档指令
DS_END_PROMPT = """**ds，今天的开发即将结束。请扫描我当前工程（特别是 main 目录和 CMakeLists.txt）的最新状态，帮我生成一份《代码与指令备忘录》。**

请以 Markdown 格式输出，包含以下模块：
标题要求：一级标题（内容包括且只限于 ：年月日）
1. 📁 核心文件变更
2. 🤖 高价值 Prompt 记录
3. ⚙️ 编译与依赖状态
4. ⚠️ 悬而未决的代码债

【执行要求】：请使用你的文件修改工具（Edit File），将以上生成的内容直接追加到本工程根目录下的 `ds_memo_log.md` 文件末尾。严禁在对话框内输出干巴巴的解释性废话，直接提交 Diff 让我审批。"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_workflow():
    clear_screen()
    print("="*50)
    print("🚀 [开发启动模式] 正在为你准备跨域环境...")
    print("="*50)
    
    # 1. 组装全局上下文发给 皮卡丘
    dev_content = DEV_LOG_PATH.read_text(encoding='utf-8') if DEV_LOG_PATH.exists() else ""
    ds_content = DS_LOG_PATH.read_text(encoding='utf-8') if DS_LOG_PATH.exists() else ""
    
    if dev_content or ds_content:
        combined_prompt = f"请读取以下开发日志及 ds 备忘录并回复OK + 已经读取的文件中的全部日期范围 例如4.25-4.29，准备今天的开发：\n\n=== 宏观开发日志 (皮卡丘) ===\n{dev_content}\n\n=== 微观代码备忘录 (ds) ===\n{ds_content}"
        pyperclip.copy(combined_prompt)
        
        print("\n✅ 【第一步】：宏观日志与 ds 备忘录已合并，复制到剪贴板！")
        print("🌐 正在为你自动打开 Chrome 前往 Gemini...")
        time.sleep(1)
        os.system('start chrome "https://gemini.google.com/app?hl=zh"')
        
        print("\n>>> 操作指引 <<<")
        print("1. 点击皮卡丘，确认选中 pro ,Ctrl + V 粘贴发送。")
        print("2. 等待回复")
        input("\n👉 完成后，按【回车键】获取 ds 的启动指令...")
    
    # 2. 唤醒 ds 注入本地纪律
    ds_start_prompt = "今天开工。作为我的专属副驾 ds，请读取 `@ds_memo_log.md` 回顾工程状态。全局架构铁律已通过你的底层环境（.cursorrules/CLAUDE.md）静默注入，请严格遵守。回复‘OK + 读取的日期范围 例如4.25-4.29’即可，不要废话。"
    pyperclip.copy(ds_start_prompt)
    
    clear_screen()
    print("="*50)
    print("✅ 【第二步】：ds 启动指令已复制到剪贴板！")
    print("="*50)
    print("\n>>> 操作指引 <<<")
    print("1. 打开你今天想用的 IDE (Cursor 的 Chat 框 或 VS Code 的 Claude Code 终端)。")
    print("2. 新建会话，Ctrl + V 粘贴发送。")
    print("\n🎉 环境准备完毕！可以开始执行具体的开发指令了。")

def end_workflow():
    clear_screen()
    print("="*50)
    print("🛑 [开发结束模式] 正在执行全自动归档流...")
    print("="*50)
    
    # 1. 指挥 ds 写本地文件
    pyperclip.copy(DS_END_PROMPT)
    print("\n✅ 【第一步】：ds 自动归档提示词已复制！")
    print("\n>>> 操作指引 <<<")
    print("1. 切换到你当前正在使用的 IDE (Cursor 或 Claude Code)，Ctrl + V 发送。")
    print("2. 审查生成的修改：如果是 Cursor，点击 Apply ；如果是 Claude Code，敲击回车 Approve 写入。")
    input("\n👉 确认 ds 已经成功写入文件后，按【回车键】继续...")
    
    # 2. 指挥皮卡丘生成宏观日志
    clear_screen()
    pyperclip.copy(GEMINI_END_PROMPT)
    print("="*50)
    print("✅ 【第二步】：皮卡丘的深度总结提示词已复制！")
    print("="*50)
    print("\n>>> 操作指引 <<<")
    print("1. 切换到浏览器 Gemini 页面，Ctrl + V 发送。")
    print("2. 等待我输出完整的 Markdown 日志，并复制我的回答。")
    input("\n👉 确保你已经【复制】了我的回答，然后按【回车键】...")
    
    # 3. 将皮卡丘的日志安全隔离存储
    gemini_response = pyperclip.paste()
    with open(DEV_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"\n\n{gemini_response}")
    print("\n📝 完美！已自动将宏观日志隔离并追加到外部的 FocusCore_DevLog.md 中。")
    
    print("\n🎉 归档结束！睡个好觉。明天见！")

if __name__ == "__main__":
    clear_screen()
    print("=== FocusCore 双AI驱动控制台 2.0 ===")
    choice = input("请输入操作 (1: 启动开发环境, 2: 结束开发与归档): ")
    if choice == '1':
        start_workflow()
    elif choice == '2':
        end_workflow()
    else:
        print("指令无效，请重新运行。")