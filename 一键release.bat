@echo off
chcp 65001 > nul

REM --- 这是一个一键提交和推送笔记到GitHub的脚本 ---

echo.
echo =========================================
echo      笔记自动发布脚本
echo =========================================
echo.

REM 提示用户输入提交信息
set /p commit_msg="请输入本次更新内容 (直接回车则使用默认信息): "

REM 如果用户没有输入，则使用默认信息
if "%commit_msg%"=="" set commit_msg="docs: update notes"

echo.
echo -----------------------------------------
echo [1/3] 正在添加所有文件...
git add .

echo [2/3] 正在提交更改: "%commit_msg%"
git commit -m "%commit_msg%"

echo [3/3] 正在推送到远程仓库...
git push
echo -----------------------------------------
echo.

echo.
echo  ^>_^<  所有操作已完成！你的网站正在后台更新...
echo.
pause
