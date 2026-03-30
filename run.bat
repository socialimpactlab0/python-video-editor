@echo off
chcp 65001 >nul
title Python Video Editor

:MENU
cls
echo ================================================
echo   Python Video Editor
echo ================================================
echo.
echo   [1] 剪切影片（設定開始/結束時間）
echo   [2] 合併多個影片
echo   [3] 縮放影片尺寸
echo   [4] 加上文字字幕
echo   [5] 提取音訊
echo   [6] 替換 / 混合音訊
echo   [7] 調整播放速度
echo   [8] 轉換影片格式
echo   [9] 查看影片資訊
echo   [0] 離開
echo.
set /p CHOICE="請選擇功能 (0-9): "

if "%CHOICE%"=="1" goto TRIM
if "%CHOICE%"=="2" goto MERGE
if "%CHOICE%"=="3" goto RESIZE
if "%CHOICE%"=="4" goto ADDTEXT
if "%CHOICE%"=="5" goto EXTRACTAUDIO
if "%CHOICE%"=="6" goto ADDAUDIO
if "%CHOICE%"=="7" goto SPEED
if "%CHOICE%"=="8" goto CONVERT
if "%CHOICE%"=="9" goto INFO
if "%CHOICE%"=="0" exit /b 0
goto MENU

:: ------------------------------------------------
:TRIM
cls
echo ================================================
echo   剪切影片
echo ================================================
echo.
set /p INPUT="輸入影片路徑（直接拖曳檔案進來）: "
set /p OUTPUT="輸出檔案名稱（例如 output.mp4）: "
set /p START="開始時間（秒，例如 10）: "
set /p END="結束時間（秒，例如 30，直接 Enter 代表到結尾）: "

if "%END%"=="" (
    python -m video_editor trim "%INPUT%" "%OUTPUT%" --start %START%
) else (
    python -m video_editor trim "%INPUT%" "%OUTPUT%" --start %START% --end %END%
)
echo.
pause
goto MENU

:: ------------------------------------------------
:MERGE
cls
echo ================================================
echo   合併影片
echo ================================================
echo.
set /p OUTPUT="輸出檔案名稱（例如 merged.mp4）: "
set /p INPUTS="輸入所有影片路徑（用空格分隔，可直接拖曳）: "

python -m video_editor merge "%OUTPUT%" %INPUTS%
echo.
pause
goto MENU

:: ------------------------------------------------
:RESIZE
cls
echo ================================================
echo   縮放影片
echo ================================================
echo.
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出檔案名稱: "
echo.
echo 縮放方式：
echo   [1] 按比例縮放（例如 0.5 = 縮小50%）
echo   [2] 指定寬高像素
echo.
set /p RMODE="選擇 (1 或 2): "

if "%RMODE%"=="1" (
    set /p SCALE="縮放比例（例如 0.5）: "
    python -m video_editor resize "%INPUT%" "%OUTPUT%" --scale %SCALE%
) else (
    set /p WIDTH="寬度（像素）: "
    set /p HEIGHT="高度（像素）: "
    python -m video_editor resize "%INPUT%" "%OUTPUT%" --width %WIDTH% --height %HEIGHT%
)
echo.
pause
goto MENU

:: ------------------------------------------------
:ADDTEXT
cls
echo ================================================
echo   加上文字字幕
echo ================================================
echo.
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出檔案名稱: "
set /p TEXT="文字內容: "
set /p START="出現時間（秒）: "
set /p END="消失時間（秒，直接 Enter 代表到結尾）: "
echo.
echo 位置選項: center / top / bottom / top-left / top-right / bottom-left / bottom-right
set /p POS="文字位置（直接 Enter 預設 bottom）: "
if "%POS%"=="" set POS=bottom

set /p FONTSIZE="字體大小（直接 Enter 預設 48）: "
if "%FONTSIZE%"=="" set FONTSIZE=48

set /p COLOR="文字顏色（直接 Enter 預設 white）: "
if "%COLOR%"=="" set COLOR=white

if "%END%"=="" (
    python -m video_editor add-text "%INPUT%" "%OUTPUT%" --text "%TEXT%" --start %START% --position %POS% --fontsize %FONTSIZE% --color %COLOR%
) else (
    python -m video_editor add-text "%INPUT%" "%OUTPUT%" --text "%TEXT%" --start %START% --end %END% --position %POS% --fontsize %FONTSIZE% --color %COLOR%
)
echo.
pause
goto MENU

:: ------------------------------------------------
:EXTRACTAUDIO
cls
echo ================================================
echo   提取音訊
echo ================================================
echo.
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出音訊檔案（例如 audio.mp3）: "

python -m video_editor extract-audio "%INPUT%" "%OUTPUT%"
echo.
pause
goto MENU

:: ------------------------------------------------
:ADDAUDIO
cls
echo ================================================
echo   替換 / 混合音訊
echo ================================================
echo.
set /p INPUT="輸入影片路徑: "
set /p AUDIO="音訊檔案路徑（mp3/wav...）: "
set /p OUTPUT="輸出檔案名稱: "
echo.
set /p MIX="與原音訊混合？(y/N): "

if /i "%MIX%"=="y" (
    python -m video_editor add-audio "%INPUT%" "%AUDIO%" "%OUTPUT%" --mix
) else (
    python -m video_editor add-audio "%INPUT%" "%AUDIO%" "%OUTPUT%"
)
echo.
pause
goto MENU

:: ------------------------------------------------
:SPEED
cls
echo ================================================
echo   調整播放速度
echo ================================================
echo.
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出檔案名稱: "
echo.
echo 範例：2.0 = 兩倍速，0.5 = 半速
set /p FACTOR="速度倍率: "

python -m video_editor speed "%INPUT%" "%OUTPUT%" --factor %FACTOR%
echo.
pause
goto MENU

:: ------------------------------------------------
:CONVERT
cls
echo ================================================
echo   轉換影片格式
echo ================================================
echo.
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出檔案名稱（副檔名決定格式，例如 output.avi）: "

python -m video_editor convert "%INPUT%" "%OUTPUT%"
echo.
pause
goto MENU

:: ------------------------------------------------
:INFO
cls
echo ================================================
echo   查看影片資訊
echo ================================================
echo.
set /p INPUT="影片路徑（直接拖曳檔案進來）: "

python -m video_editor info "%INPUT%"
echo.
pause
goto MENU
