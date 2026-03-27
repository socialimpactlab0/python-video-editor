@echo off
chcp 65001 >nul
title Python Video Editor - 安裝程式

echo ================================================
echo   Python Video Editor 安裝程式
echo ================================================
echo.

echo [1/3] 檢查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python！
    echo 請到 https://www.python.org/downloads/ 下載安裝
    echo 安裝時請勾選 "Add Python to PATH"
    pause
    exit /b 1
)
python --version
echo Python 已安裝 OK

echo.
echo [2/3] 安裝 Python 套件...
pip install -r requirements.txt
if errorlevel 1 (
    echo [錯誤] 套件安裝失敗
    pause
    exit /b 1
)
echo 套件安裝完成 OK

echo.
echo [3/3] 檢查 FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo FFmpeg 尚未安裝，嘗試透過 winget 自動安裝...
    winget install --id Gyan.FFmpeg -e --silent
    if errorlevel 1 (
        echo [注意] 請手動安裝 FFmpeg：winget install Gyan.FFmpeg
    ) else (
        echo FFmpeg 安裝完成 OK
    )
) else (
    echo FFmpeg 已安裝 OK
)

echo.
echo ================================================
echo   安裝完成！請執行 run.bat 開始使用
echo ================================================
pause
