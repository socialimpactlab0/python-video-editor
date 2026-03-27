@echo off
chcp 65001 >nul
title Python Video Editor

:MENU
cls
echo ================================================
echo   Python Video Editor
echo ================================================
echo.
echo   [1] 剪切影片
echo   [2] 合併多個影片
echo   [3] 縮放影片尺寸
echo   [4] 加上文字字幕
echo   [5] 提取音訊
echo   [6] 替換/混合音訊
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

:TRIM
cls
echo === 剪切影片 ===
set /p INPUT="輸入影片路徑（可直接拖曳）: "
set /p OUTPUT="輸出檔案名稱（例如 output.mp4）: "
set /p START="開始時間（秒）: "
set /p END="結束時間（秒，Enter=到結尾）: "
if "%END%"=="" (
    python -m video_editor trim "%INPUT%" "%OUTPUT%" --start %START%
) else (
    python -m video_editor trim "%INPUT%" "%OUTPUT%" --start %START% --end %END%
)
pause & goto MENU

:MERGE
cls
echo === 合併影片 ===
set /p OUTPUT="輸出檔案名稱: "
set /p INPUTS="輸入所有影片路徑（空格分隔）: "
python -m video_editor merge "%OUTPUT%" %INPUTS%
pause & goto MENU

:RESIZE
cls
echo === 縮放影片 ===
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出檔案名稱: "
echo [1] 按比例  [2] 指定寬高
set /p RMODE="選擇: "
if "%RMODE%"=="1" (
    set /p SCALE="縮放比例（例如 0.5）: "
    python -m video_editor resize "%INPUT%" "%OUTPUT%" --scale %SCALE%
) else (
    set /p WIDTH="寬度: "
    set /p HEIGHT="高度: "
    python -m video_editor resize "%INPUT%" "%OUTPUT%" --width %WIDTH% --height %HEIGHT%
)
pause & goto MENU

:ADDTEXT
cls
echo === 加上文字 ===
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出檔案名稱: "
set /p TEXT="文字內容: "
set /p START="出現時間（秒）: "
set /p END="消失時間（秒，Enter=到結尾）: "
set /p POS="位置 center/top/bottom（Enter=bottom）: "
if "%POS%"=="" set POS=bottom
set /p FONTSIZE="字體大小（Enter=48）: "
if "%FONTSIZE%"=="" set FONTSIZE=48
set /p COLOR="顏色（Enter=white）: "
if "%COLOR%"=="" set COLOR=white
if "%END%"=="" (
    python -m video_editor add-text "%INPUT%" "%OUTPUT%" --text "%TEXT%" --start %START% --position %POS% --fontsize %FONTSIZE% --color %COLOR%
) else (
    python -m video_editor add-text "%INPUT%" "%OUTPUT%" --text "%TEXT%" --start %START% --end %END% --position %POS% --fontsize %FONTSIZE% --color %COLOR%
)
pause & goto MENU

:EXTRACTAUDIO
cls
echo === 提取音訊 ===
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出音訊（例如 audio.mp3）: "
python -m video_editor extract-audio "%INPUT%" "%OUTPUT%"
pause & goto MENU

:ADDAUDIO
cls
echo === 替換/混合音訊 ===
set /p INPUT="輸入影片路徑: "
set /p AUDIO="音訊檔案路徑: "
set /p OUTPUT="輸出檔案名稱: "
set /p MIX="與原音訊混合？(y/N): "
if /i "%MIX%"=="y" (
    python -m video_editor add-audio "%INPUT%" "%AUDIO%" "%OUTPUT%" --mix
) else (
    python -m video_editor add-audio "%INPUT%" "%AUDIO%" "%OUTPUT%"
)
pause & goto MENU

:SPEED
cls
echo === 調整速度 ===
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出檔案名稱: "
set /p FACTOR="速度倍率（2.0=兩倍速，0.5=半速）: "
python -m video_editor speed "%INPUT%" "%OUTPUT%" --factor %FACTOR%
pause & goto MENU

:CONVERT
cls
echo === 轉換格式 ===
set /p INPUT="輸入影片路徑: "
set /p OUTPUT="輸出檔案（副檔名決定格式）: "
python -m video_editor convert "%INPUT%" "%OUTPUT%"
pause & goto MENU

:INFO
cls
echo === 影片資訊 ===
set /p INPUT="影片路徑（可直接拖曳）: "
python -m video_editor info "%INPUT%"
pause & goto MENU
