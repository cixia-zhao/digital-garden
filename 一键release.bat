@echo off
chcp 65001 > nul

echo.
echo =========================================
echo      笔记发布脚本 [防忘记提醒版]
echo =========================================
echo.

set /p commit_msg="请输入本次更新内容 (如果已提交, 直接关闭本窗口): "

REM 如果用户只是按了回-车但没输入内容, 则退出
if "%commit_msg%"=="" (
    echo.
    echo -- 未输入内容, 操作已取消 --
    timeout /t 3
    exit
)

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

echo  ^>_^<  操作完成！
echo.
pause
