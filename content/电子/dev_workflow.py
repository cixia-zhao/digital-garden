import os
import pyperclip
from pathlib import Path
import time

# 配置文件路径
DEV_LOG_PATH = Path(r"D:\code\digital-garden\content\电子\FocusCore_DevLog（开发日志）.md")
CURSOR_LOG_PATH = Path(r"D:\code\digital-garden\content\电子\curosr提示词指令开发日志.md")

# 固定的结束提示词
GEMINI_END_PROMPT = """**Gemini，今天的开发结束了。请帮我深度总结一份今天的 DevLog（开发者日志）。**
【执行要求】：请务必从我们今天对话的第一句话开始全量回溯。千万不要遗漏任何前置的准备工作、使用过的外部网站、以及特定的参数（如十六进制色号、精确分辨率等）。
请以 Markdown 格式输出，标题要求一级标题（ 内容包括且只限于 ： 年月日），包含以下五个核心模块：
1. 🎯 核心里程碑
2. 🧰 关键工具链与素材管线
3. 🕳️ 踩坑复盘与物理底层
4. 💻 终端指令与环境
5. 🧠 架构师新知与明日 TODO"""

CURSOR_END_PROMPT = """**Cursor，今天的开发即将结束。请扫描我当前工程（特别是 `main` 目录和 `CMakeLists.txt`）的最新状态，帮我生成一份《代码与指令备忘录》。**
请以 Markdown 格式输出，包含以下模块：
标题要求：一级标题（内容包括且只限于 ：年月日）
1. 📁 核心文件变更
2. 🤖 高价值 Prompt 记录
3. ⚙️ 编译与依赖状态
4. ⚠️ 悬而未决的代码债"""

def clear_screen():
    # 跨平台清屏命令，让终端保持干净
    os.system('cls' if os.name == 'nt' else 'clear')

def start_workflow():
    clear_screen()
    print("="*50)
    print("🚀 [开发启动模式] 正在为你准备环境...")
    print("="*50)
    
    # 1. 准备 Gemini 上下文 (已修改为同时合并发送两个日志)
    dev_content = DEV_LOG_PATH.read_text(encoding='utf-8') if DEV_LOG_PATH.exists() else ""
    cursor_content = CURSOR_LOG_PATH.read_text(encoding='utf-8') if CURSOR_LOG_PATH.exists() else ""
    
    if dev_content or cursor_content:
        combined_prompt = f"请读取以下开发日志及Cursor备忘录并回复OK，准备今天的开发：\n\n=== FocusCore 开发日志 ===\n{dev_content}\n\n=== Cursor 代码指令备忘录 ===\n{cursor_content}"
        pyperclip.copy(combined_prompt)
        
        print("\n✅ 【第一步完成】：FocusCore 开发日志与 Cursor 备忘录已合并复制到你的剪贴板！")
        print("🌐 正在为你自动打开 Chrome 浏览器前往 Gemini...")
        time.sleep(1)
        os.system('start chrome "https://gemini.google.com/app?hl=zh"')
        
        print("\n>>> 你的操作指引 <<<")
        print("1. 在弹出的浏览器中，展开左侧菜单，点击『皮卡丘』对话。")
        print("2. 确保模型选择了『Pro』。")
        print("3. 按下 Ctrl + V 粘贴，然后按回车发送。")
        print("4. 等待我回复 'OK'。")
        input("\n👉 完成以上步骤后，请回到这个黑框框，按【回车键】继续准备 Cursor 环境...")
    
    # 2. 准备 Cursor 上下文 (保持原样)
    if CURSOR_LOG_PATH.exists():
        content = CURSOR_LOG_PATH.read_text(encoding='utf-8')
        pyperclip.copy(f"请读取以下指令日志并回复OK：\n\n{content}")
        
        clear_screen()
        print("="*50)
        print("✅ 【第二步完成】：Cursor 指令日志已复制到你的剪贴板！")
        print("="*50)
        print("\n>>> 你的操作指引 <<<")
        print("1. 请手动打开你的 Cursor 软件。")
        print("2. 点击右上角的 '+' 号 (New Agent) 新建一个对话。")
        print("3. 在右侧输入框按下 Ctrl + V 粘贴，然后发送。")
        print("4. 等待 Cursor 回复 'OK'。")
        input("\n👉 完成后，请按【回车键】结束启动流程...")
        print("\n🎉 环境准备完毕！祝你今天敲码愉快，没有 Bug！")

def end_workflow():
    clear_screen()
    print("="*50)
    print("🛑 [开发结束模式] 正在准备下班收尾工作...")
    print("="*50)
    
    # 1. 生成 Gemini 总结
    pyperclip.copy(GEMINI_END_PROMPT)
    print("\n✅ 【第一步】：Gemini 的深度总结提示词已复制好！")
    print("\n>>> 你的操作指引 <<<")
    print("1. 切换到浏览器中的 Gemini 页面。")
    print("2. 按下 Ctrl + V 粘贴提示词并发送。")
    print("3. 等待我生成完那一大段结构化的 Markdown 开发日志。")
    print("4. 点击我回答右下角的『复制』按钮（或者手动全选复制）。")
    input("\n👉 确保你已经把我的回答【复制】了，然后回到这里按【回车键】...")
    
    gemini_response = pyperclip.paste()
    with open(DEV_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"\n\n{gemini_response}")
    print("📝 太棒了！已自动将 Gemini 的总结追加到 D 盘的 FocusCore_DevLog.md 文件末尾。")

    # 2. 生成 Cursor 总结
    input("\n👉 接下来去搞定 Cursor 的总结。按【回车键】复制 Cursor 的专属提示词...")
    pyperclip.copy(CURSOR_END_PROMPT)
    clear_screen()
    
    print("="*50)
    print("✅ 【第二步】：Cursor 的代码总结提示词已复制好！")
    print("="*50)
    print("\n>>> 你的操作指引 <<<")
    print("1. 切换到 Cursor 软件。")
    print("2. 在最下方的 Chat 对话框里，按下 Ctrl + V 粘贴提示词并发送。")
    print("3. 等待 Cursor 总结完今天的代码变更和高价值 Prompt。")
    print("4. 点击 Cursor 回答框右下角的三个点 (...) -> 选择 Copy Message。")
    input("\n👉 确保你已经把 Cursor 的回答【复制】了，然后回到这里按【回车键】...")
    
    cursor_response = pyperclip.paste()
    with open(CURSOR_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"\n\n{cursor_response}")
    print("📝 完美！已自动将 Cursor 的总结追加到 D 盘的指令日志文件末尾。")
    
    print("\n🎉 今天的开发正式结束，所有日志已安全归档。好好休息，明天见！")
    input("\n按【回车键】退出控制台...")

if __name__ == "__main__":
    clear_screen()
    print("=== FocusCore 项目开发控制台 ===")
    choice = input("请输入操作 (1: 启动开发环境, 2: 结束开发与归档): ")
    if choice == '1':
        start_workflow()
    elif choice == '2':
        end_workflow()
    else:
        print("无效输入，请重新运行。")