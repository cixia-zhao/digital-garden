@echo off
chcp 65001 > nul
title 启动发布脚本

FOR /F "tokens=2,*" %%A IN ('REG QUERY "HKLM\SOFTWARE\GitForWindows" /v "InstallPath"') DO (SET "GIT_INSTALL_PATH=%%B")
IF NOT DEFINED GIT_INSTALL_PATH FOR /F "tokens=2,*" %%A IN ('REG QUERY "HKCU\SOFTWARE\GitForWindows" /v "InstallPath"') DO (SET "GIT_INSTALL_PATH=%%B")
IF DEFINED GIT_INSTALL_PATH (IF "%GIT_INSTALL_PATH:~-1%"==" " SET "GIT_INSTALL_PATH=%GIT_INSTALL_PATH:~0,-1%")

IF NOT DEFINED GIT_INSTALL_PATH (
    echo [ERROR] Cannot find Git installation path in registry.
    pause
    exit /b
)
IF NOT EXIST "%GIT_INSTALL_PATH%\git-cmd.exe" (
    echo [ERROR] Cannot find git-cmd.exe in "%GIT_INSTALL_PATH%".
    pause
    exit /b
)

echo Git found at: %GIT_INSTALL_PATH%
echo Starting publisher script...
echo.

"%GIT_INSTALL_PATH%\git-cmd.exe" --command=usr/bin/bash.exe -l -i -c "cd \"%~dp0.\" && .//一键release.bat"

echo.
echo Script finished.
pause
