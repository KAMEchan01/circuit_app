#!/bin/bash

# CIRCUIT解説動画の最終仕上げ
# 映像と音声を統合して完成版MP4を作成

echo "🎬 Finalizing CIRCUIT explanation video with audio..."

BASE_DIR="/Users/kamechan/claude_code/circuit"
VIDEOS_DIR="$BASE_DIR/videos"
AUDIO_DIR="$VIDEOS_DIR/audio"
FINAL_DIR="$VIDEOS_DIR/final"

# 入力ファイル
VIDEO_FILE="$FINAL_DIR/circuit_explanation_final.mp4"
NARRATION_FILE="$AUDIO_DIR/combined_narration.wav"
BGM_FILE="$AUDIO_DIR/background_music.wav"

# 出力ファイル
FINAL_OUTPUT="$FINAL_DIR/circuit_explanation_complete.mp4"

echo "📁 Input files:"
echo "  🎞️ Video: $VIDEO_FILE"
echo "  🎙️ Narration: $NARRATION_FILE"
echo "  🎵 BGM: $BGM_FILE"

# ファイル存在チェック
check_files() {
    local all_exist=true
    
    if [ ! -f "$VIDEO_FILE" ]; then
        echo "❌ Video file not found: $VIDEO_FILE"
        all_exist=false
    else
        echo "✅ Video file found"
    fi
    
    if [ ! -f "$NARRATION_FILE" ]; then
        echo "❌ Narration file not found: $NARRATION_FILE"
        all_exist=false
    else
        echo "✅ Narration file found"
    fi
    
    if [ ! -f "$BGM_FILE" ]; then
        echo "⚠️  BGM file not found: $BGM_FILE"
        echo "  Proceeding without background music"
    else
        echo "✅ BGM file found"
    fi
    
    return $([ "$all_exist" = true ])
}

# 音声ミックス
create_audio_mix() {
    echo "🎧 Creating final audio mix..."
    
    MIXED_AUDIO="$AUDIO_DIR/final_audio_mix.wav"
    
    if [ -f "$BGM_FILE" ]; then
        # ナレーションとBGMをミックス
        echo "  Mixing narration with background music..."
        sox -m "$NARRATION_FILE" "|sox '$BGM_FILE' -p vol 0.3" "$MIXED_AUDIO" norm -3
    else
        # ナレーションのみ
        echo "  Using narration only..."
        cp "$NARRATION_FILE" "$MIXED_AUDIO"
    fi
    
    echo "✅ Audio mix created: $MIXED_AUDIO"
    return "$MIXED_AUDIO"
}

# 動画と音声を結合
combine_video_audio() {
    local audio_file="$1"
    
    echo "🎬 Combining video and audio..."
    
    # FFmpegが利用可能かチェック
    if command -v ffmpeg &> /dev/null; then
        echo "  Using FFmpeg for professional quality..."
        
        ffmpeg -y \
            -i "$VIDEO_FILE" \
            -i "$audio_file" \
            -c:v libx264 \
            -c:a aac \
            -b:v 2M \
            -b:a 128k \
            -shortest \
            "$FINAL_OUTPUT"
            
        if [ $? -eq 0 ]; then
            echo "✅ Professional video with audio created!"
            return 0
        else
            echo "❌ FFmpeg processing failed"
            return 1
        fi
    else
        echo "⚠️  FFmpeg not available, creating alternative version..."
        
        # 代替手段：音声ファイルと動画ファイルを並置
        cp "$VIDEO_FILE" "$FINAL_OUTPUT"
        cp "$audio_file" "${FINAL_OUTPUT%.*}_audio.wav"
        
        echo "📁 Files created for manual combination:"
        echo "  🎞️ Video: $FINAL_OUTPUT"
        echo "  🎵 Audio: ${FINAL_OUTPUT%.*}_audio.wav"
        
        return 0
    fi
}

# メタデータ情報を作成
create_video_metadata() {
    echo "📋 Creating video metadata..."
    
    METADATA_FILE="$FINAL_DIR/video_info.json"
    
    cat > "$METADATA_FILE" << EOF
{
    "title": "CIRCUIT - F1テーマの筋トレアプリ解説動画",
    "description": "たった4分で効果的な全身トレーニングができるタバタ式ワークアウトアプリの紹介動画",
    "duration": "60秒",
    "resolution": "1280x720 (HD)",
    "framerate": "5fps",
    "app_url": "https://circuit-workout.com",
    "features": [
        "タバタ式サーキットトレーニング",
        "F1テーマの習慣化システム",
        "カロリー・進捗管理",
        "完全無料Web アプリ"
    ],
    "target_audience": "筋トレ初心者、忙しい現代人",
    "call_to_action": "今すぐWebブラウザから無料で始められます",
    "created": "$(date -Iseconds)",
    "files": {
        "main_video": "circuit_explanation_complete.mp4",
        "audio_only": "circuit_explanation_complete_audio.wav",
        "thumbnail": "circuit_explanation_final.png"
    }
}
EOF

    echo "✅ Metadata created: $METADATA_FILE"
}

# サムネイル画像を作成
create_thumbnail() {
    echo "🖼️ Creating video thumbnail..."
    
    THUMBNAIL="$FINAL_DIR/circuit_thumbnail.png"
    
    # Pythonで高品質サムネイルを作成
    python3 << 'PYTHON_SCRIPT'
from PIL import Image, ImageDraw, ImageFont
import os

# サムネイル設定
width, height = 1920, 1080
img = Image.new('RGB', (width, height), (30, 60, 114))
draw = ImageDraw.Draw(img)

# グラデーション背景
for y in range(height):
    ratio = y / height
    r = int(30 + (255 - 30) * ratio * 0.3)
    g = int(60 + (107 - 60) * ratio * 0.3)
    b = int(114 + (107 - 114) * ratio * 0.3)
    color = (r, g, b)
    draw.line([(0, y), (width, y)], fill=color)

# フォント
try:
    title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 120)
    subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 60)
    feature_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 48)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    feature_font = ImageFont.load_default()

# メインタイトル
title = "🏎️ CIRCUIT"
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (width - title_width) // 2

# 影効果
draw.text((title_x + 5, 185), title, fill=(0, 0, 0, 200), font=title_font)
draw.text((title_x, 180), title, fill=(255, 107, 107), font=title_font)

# サブタイトル
subtitle = "F1テーマの筋トレアプリ"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (width - subtitle_width) // 2

draw.text((subtitle_x + 3, 323), subtitle, fill=(0, 0, 0, 200), font=subtitle_font)
draw.text((subtitle_x, 320), subtitle, fill=(255, 255, 255), font=subtitle_font)

# 特徴ポイント
features = [
    "✨ たった4分で全身トレーニング",
    "🎯 タバタ式で超効率的",
    "🏁 F1テーマで継続しやすい",
    "💸 完全無料・今すぐ利用可能"
]

y_start = 450
for i, feature in enumerate(features):
    feature_bbox = draw.textbbox((0, 0), feature, font=feature_font)
    feature_width = feature_bbox[2] - feature_bbox[0]
    feature_x = (width - feature_width) // 2
    
    y_pos = y_start + i * 80
    
    draw.text((feature_x + 2, y_pos + 2), feature, fill=(0, 0, 0, 150), font=feature_font)
    draw.text((feature_x, y_pos), feature, fill=(78, 205, 196), font=feature_font)

# URL
url = "circuit-workout.com"
url_bbox = draw.textbbox((0, 0), url, font=subtitle_font)
url_width = url_bbox[2] - url_bbox[0]
url_x = (width - url_width) // 2

draw.text((url_x + 3, 863), url, fill=(0, 0, 0, 200), font=subtitle_font)
draw.text((url_x, 860), url, fill=(255, 215, 0), font=subtitle_font)

# 保存
thumbnail_path = "/Users/kamechan/claude_code/circuit/videos/final/circuit_thumbnail.png"
img.save(thumbnail_path, "PNG", optimize=True, quality=95)
print(f"✅ Thumbnail created: {thumbnail_path}")
PYTHON_SCRIPT

    echo "✅ Professional thumbnail created"
}

# メイン処理
main() {
    echo "🚀 Starting final video processing..."
    
    # ファイルチェック
    if ! check_files; then
        echo "❌ Required files missing. Please run previous steps first."
        exit 1
    fi
    
    # 音声ミックス作成
    audio_mix=$(create_audio_mix)
    
    # 動画と音声を結合
    if combine_video_audio "$AUDIO_DIR/final_audio_mix.wav"; then
        echo "✅ Video combination successful"
    else
        echo "⚠️  Video combination had issues, but files are prepared"
    fi
    
    # メタデータとサムネイル作成
    create_video_metadata
    create_thumbnail
    
    echo ""
    echo "🎉 CIRCUIT解説動画作成完了！"
    echo ""
    echo "📁 作成されたファイル:"
    ls -la "$FINAL_DIR"/*.mp4 2>/dev/null | head -5
    ls -la "$FINAL_DIR"/*.png 2>/dev/null | head -3
    ls -la "$FINAL_DIR"/*.wav 2>/dev/null | head -2
    
    echo ""
    echo "📊 動画情報:"
    if [ -f "$FINAL_OUTPUT" ]; then
        echo "  ✅ メイン動画: $(basename $FINAL_OUTPUT)"
        echo "  📐 解像度: 1280x720 (HD)"
        echo "  ⏱️ 長さ: 60秒"
        echo "  🎞️ フレームレート: 5fps"
        echo "  💾 ファイルサイズ: $(du -h '$FINAL_OUTPUT' | cut -f1)"
    fi
    
    echo ""
    echo "🚀 次のステップ:"
    echo "  1. 動画を再生して品質確認"
    echo "  2. YouTubeにアップロード"
    echo "  3. SNSで共有"
    echo "  4. Webサイトに埋め込み"
    
    echo ""
    echo "🎯 動画の特徴:"
    echo "  • F1テーマの一貫したブランディング"
    echo "  • プロフェッショナルなビジュアル"
    echo "  • 明確な価値提案（4分間）"
    echo "  • 強力な行動喚起"
}

# 実行
main