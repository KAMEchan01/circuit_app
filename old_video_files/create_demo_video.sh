#!/bin/bash

# CIRCUIT アプリデモ動画作成スクリプト（FFmpegベース）

cd /Users/kamechan/claude_code/circuit
BASE_DIR="/Users/kamechan/claude_code/circuit"
RAW_DIR="$BASE_DIR/videos/raw"
FINAL_DIR="$BASE_DIR/videos/final"

echo "Creating CIRCUIT demo video..."

# FFmpegがインストールされているかチェック
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg..."
    brew install ffmpeg
fi

# 各ナレーションファイルの長さを取得
echo "Getting audio durations..."

# ナレーション1の長さ
duration1=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$RAW_DIR/narration_1.aiff")
duration2=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$RAW_DIR/narration_2.aiff")
duration3=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$RAW_DIR/narration_3.aiff")
duration4=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$RAW_DIR/narration_4.aiff")
duration5=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$RAW_DIR/narration_5.aiff")
duration6=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$RAW_DIR/narration_6.aiff")

echo "Duration 1: $duration1 seconds"
echo "Duration 2: $duration2 seconds"
echo "Duration 3: $duration3 seconds"
echo "Duration 4: $duration4 seconds"
echo "Duration 5: $duration5 seconds"
echo "Duration 6: $duration6 seconds"

# スクリーンショットを撮影（手動で指示）
echo "==================================="
echo "MANUAL STEPS REQUIRED:"
echo "==================================="
echo "1. Open https://circuit-workout.com/demo_setup.html"
echo "2. Click 'デモデータを設定' button"
echo "3. Open https://circuit-workout.com/"
echo "4. Take screenshot and save as: $RAW_DIR/scene_1.png"
echo "5. Click start button and take screenshot during workout as: $RAW_DIR/scene_2.png"
echo "6. Navigate to record page and take screenshot as: $RAW_DIR/scene_3.png"
echo ""
echo "Press Enter when screenshots are ready..."
read -r

# シンプルなスライドショー動画を作成
echo "Creating video with available resources..."

# 単色背景画像を作成（スクリーンショットがない場合）
create_background_image() {
    local filename=$1
    local text=$2
    local color=$3
    
    ffmpeg -f lavfi -i "color=c=$color:s=1280x720:d=1" -vf "drawtext=text='$text':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" -frames:v 1 -y "$filename"
}

# 背景画像を作成（実際のスクリーンショットがない場合のフォールバック）
if [ ! -f "$RAW_DIR/scene_1.png" ]; then
    create_background_image "$RAW_DIR/scene_1.png" "CIRCUIT\\nF1テーマ筋トレアプリ" "1e3c72"
fi

if [ ! -f "$RAW_DIR/scene_2.png" ]; then
    create_background_image "$RAW_DIR/scene_2.png" "タバタ式ワークアウト\\n4分間で効果的トレーニング" "ff6b6b"
fi

if [ ! -f "$RAW_DIR/scene_3.png" ]; then
    create_background_image "$RAW_DIR/scene_3.png" "記録・管理機能\\nデータで成果を実感" "4ecdc4"
fi

# 実際のアプリスクリーンショットを撮影（Webブラウザから）
take_app_screenshots() {
    echo "Taking app screenshots..."
    
    # Chromeでページを開く
    osascript << EOF
tell application "Google Chrome"
    activate
    open location "https://circuit-workout.com/demo_setup.html"
    delay 3
    
    -- デモデータ設定
    tell active tab of front window to execute javascript "document.querySelector('button').click();"
    delay 2
    
    -- メインページへ移動
    open location "https://circuit-workout.com/"
    delay 3
end tell

-- スクリーンショットを撮影
tell application "System Events"
    keystroke "4" using {command down, shift down}
    delay 1
    -- 画面の一部を選択してスクリーンショット撮影
    -- ユーザーが手動で範囲選択
end tell
EOF
}

# 全ナレーションを結合
echo "Combining narrations..."
ffmpeg -i "$RAW_DIR/narration_1.aiff" -i "$RAW_DIR/narration_2.aiff" -i "$RAW_DIR/narration_3.aiff" -i "$RAW_DIR/narration_4.aiff" -i "$RAW_DIR/narration_5.aiff" -i "$RAW_DIR/narration_6.aiff" \
-filter_complex "[0:a][1:a][2:a][3:a][4:a][5:a]concat=n=6:v=0:a=1[outa]" \
-map "[outa]" -y "$RAW_DIR/combined_narration.aiff"

# BGMの準備
if [ -f "$RAW_DIR/bgm.mp3" ]; then
    echo "Preparing background music..."
    # BGMの長さを取得
    bgm_duration=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$RAW_DIR/bgm.mp3")
    narration_duration=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$RAW_DIR/combined_narration.aiff")
    
    # BGMをループして必要な長さまで延長
    ffmpeg -stream_loop -1 -i "$RAW_DIR/bgm.mp3" -t "$narration_duration" -y "$RAW_DIR/extended_bgm.mp3"
    
    # ナレーションとBGMをミックス
    ffmpeg -i "$RAW_DIR/combined_narration.aiff" -i "$RAW_DIR/extended_bgm.mp3" \
    -filter_complex "[0:a]volume=0.9[narr];[1:a]volume=0.3[bgm];[narr][bgm]amix=inputs=2[out]" \
    -map "[out]" -y "$RAW_DIR/final_audio.wav"
else
    # BGMなしの場合、ナレーションのみ
    ffmpeg -i "$RAW_DIR/combined_narration.aiff" -y "$RAW_DIR/final_audio.wav"
fi

# 最終動画を作成（シンプルなスライドショー）
echo "Creating final video..."

# 3つのシーンを表示する動画を作成
ffmpeg -loop 1 -i "$RAW_DIR/scene_1.png" -t "$duration1" -pix_fmt yuv420p -y "$RAW_DIR/video_1.mp4"

if [ -f "$RAW_DIR/scene_2.png" ]; then
    ffmpeg -loop 1 -i "$RAW_DIR/scene_2.png" -t 30 -pix_fmt yuv420p -y "$RAW_DIR/video_2.mp4"
else
    # フォールバック：単色背景
    ffmpeg -f lavfi -i "color=c=ff6b6b:s=1280x720:d=30" -pix_fmt yuv420p -y "$RAW_DIR/video_2.mp4"
fi

if [ -f "$RAW_DIR/scene_3.png" ]; then
    ffmpeg -loop 1 -i "$RAW_DIR/scene_3.png" -t 30 -pix_fmt yuv420p -y "$RAW_DIR/video_3.mp4"
else
    # フォールバック：単色背景
    ffmpeg -f lavfi -i "color=c=4ecdc4:s=1280x720:d=30" -pix_fmt yuv420p -y "$RAW_DIR/video_3.mp4"
fi

# 動画を結合
ffmpeg -i "$RAW_DIR/video_1.mp4" -i "$RAW_DIR/video_2.mp4" -i "$RAW_DIR/video_3.mp4" \
-filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]" \
-map "[outv]" -y "$RAW_DIR/combined_video.mp4"

# 音声を追加
ffmpeg -i "$RAW_DIR/combined_video.mp4" -i "$RAW_DIR/final_audio.wav" \
-c:v copy -c:a aac -shortest -y "$FINAL_DIR/circuit_explanation_demo.mp4"

echo "==================================="
echo "Demo video creation completed!"
echo "Output: $FINAL_DIR/circuit_explanation_demo.mp4"
echo "==================================="

# ファイル情報を表示
if [ -f "$FINAL_DIR/circuit_explanation_demo.mp4" ]; then
    echo "Video info:"
    ffprobe -v quiet -show_format -show_streams "$FINAL_DIR/circuit_explanation_demo.mp4"
fi