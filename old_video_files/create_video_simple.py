#!/usr/bin/env python3
"""
CIRCUIT アプリ解説動画作成（簡易版）
静止画とナレーションを組み合わせた動画を作成
"""
import os
from moviepy.editor import *
import subprocess
import tempfile

def create_circuit_video():
    print("Creating CIRCUIT explanation video...")
    
    # パス設定
    base_path = "/Users/kamechan/claude_code/circuit"
    videos_path = os.path.join(base_path, "videos")
    raw_path = os.path.join(videos_path, "raw")
    final_path = os.path.join(videos_path, "final")
    
    # ナレーションファイル
    narrations = [
        os.path.join(raw_path, "narration_1.aiff"),
        os.path.join(raw_path, "narration_2.aiff"), 
        os.path.join(raw_path, "narration_3.aiff"),
        os.path.join(raw_path, "narration_4.aiff"),
        os.path.join(raw_path, "narration_5.aiff"),
        os.path.join(raw_path, "narration_6.aiff")
    ]
    
    # BGMファイル
    bgm_file = os.path.join(raw_path, "bgm.mp3")
    
    # スクリーンショット用の画像を生成（アプリのUIをイメージした画像）
    print("Creating demonstration images...")
    create_demo_images(raw_path)
    
    # 各シーンの画像ファイル
    scene_images = [
        os.path.join(raw_path, "scene_1.png"),
        os.path.join(raw_path, "scene_2.png"),
        os.path.join(raw_path, "scene_3.png"),
        os.path.join(raw_path, "scene_4.png"), 
        os.path.join(raw_path, "scene_5.png"),
        os.path.join(raw_path, "scene_6.png")
    ]
    
    # 各シーンの動画クリップを作成
    video_clips = []
    
    for i, (image, narration) in enumerate(zip(scene_images, narrations)):
        print(f"Processing scene {i+1}...")
        
        if os.path.exists(narration):
            # ナレーションの長さを取得
            audio_clip = AudioFileClip(narration)
            duration = audio_clip.duration
            
            # 画像クリップを作成
            if os.path.exists(image):
                img_clip = ImageClip(image).set_duration(duration)
                img_clip = img_clip.set_audio(audio_clip)
                video_clips.append(img_clip)
            else:
                print(f"Warning: Image {image} not found, skipping scene {i+1}")
        else:
            print(f"Warning: Narration {narration} not found, skipping scene {i+1}")
    
    if not video_clips:
        print("Error: No video clips created. Please check image and audio files.")
        return
    
    # 全クリップを結合
    final_video = concatenate_videoclips(video_clips)
    
    # BGMを追加
    if os.path.exists(bgm_file):
        print("Adding background music...")
        bgm = AudioFileClip(bgm_file).volumex(0.3)  # BGM音量を30%に
        
        # BGMの長さを動画に合わせる
        if bgm.duration < final_video.duration:
            # BGMが短い場合はループ
            loops_needed = int(final_video.duration / bgm.duration) + 1
            bgm = concatenate_audioclips([bgm] * loops_needed)
        
        bgm = bgm.subclip(0, final_video.duration)
        
        # ナレーションとBGMを合成
        final_audio = CompositeAudioClip([final_video.audio.volumex(0.9), bgm])
        final_video = final_video.set_audio(final_audio)
    
    # 最終動画を出力
    output_file = os.path.join(final_path, "circuit_explanation_video.mp4")
    print(f"Exporting final video to: {output_file}")
    
    final_video.write_videofile(
        output_file,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile=None,
        remove_temp=True
    )
    
    print("Video creation completed successfully!")
    print(f"Final video saved at: {output_file}")
    print(f"Duration: {final_video.duration:.2f} seconds")

def create_demo_images(raw_path):
    """デモ画像を作成（PIL使用）"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap
    except ImportError:
        print("PIL not available, using placeholder method")
        create_placeholder_images(raw_path)
        return
    
    # 1280x720の画像サイズ
    width, height = 1280, 720
    
    # カラーパレット（アプリのテーマ色）
    bg_color = (30, 60, 114)  # ダークブルー
    accent_color = (255, 107, 107)  # 赤
    teal_color = (78, 205, 196)  # ティール
    text_color = (255, 255, 255)  # 白
    
    scenes = [
        {
            "title": "CIRCUIT",
            "subtitle": "F1テーマの筋トレアプリ",
            "description": "たった4分で全身トレーニング\nタバタ式ワークアウト"
        },
        {
            "title": "3つの意味",
            "subtitle": "CIRCUITに込められたコンセプト",
            "description": "• サーキットトレーニング\n• F1サーキット（継続的周回）\n• 電子回路（循環システム）"
        },
        {
            "title": "タバタ式ワークアウト",
            "subtitle": "科学的に証明された効率的トレーニング",
            "description": "20秒運動 + 10秒休憩 × 8セット\n6種類のエクササイズをランダム選択\nプッシュアップ・スクワット・シットアップ他"
        },
        {
            "title": "習慣化サポート",
            "subtitle": "F1レーサーのように毎日完走を目指す",
            "description": "連続完走日数を表示\nストリーク機能でモチベーション維持\n達成感のある演出"
        },
        {
            "title": "記録・管理機能",
            "subtitle": "データで成果を実感",
            "description": "摂取・消費カロリー管理\n週間進捗グラフ\n自動カロリー記録"
        },
        {
            "title": "今すぐ始めよう",
            "subtitle": "無料でWebブラウザから利用可能",
            "description": "circuit-workout.com\n\nF1レースのように\n毎日の完走を目指そう！"
        }
    ]
    
    for i, scene in enumerate(scenes):
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            # フォント設定（システムフォントを使用）
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 72)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 36)
            desc_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 28)
        except:
            # デフォルトフォントを使用
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()
        
        # タイトル描画
        title_bbox = draw.textbbox((0, 0), scene["title"], font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) // 2, 150), scene["title"], 
                 fill=accent_color, font=title_font)
        
        # サブタイトル描画
        subtitle_bbox = draw.textbbox((0, 0), scene["subtitle"], font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        draw.text(((width - subtitle_width) // 2, 250), scene["subtitle"],
                 fill=teal_color, font=subtitle_font)
        
        # 説明文描画（複数行対応）
        y_pos = 350
        for line in scene["description"].split('\n'):
            if line.strip():
                line_bbox = draw.textbbox((0, 0), line, font=desc_font)
                line_width = line_bbox[2] - line_bbox[0]
                draw.text(((width - line_width) // 2, y_pos), line,
                         fill=text_color, font=desc_font)
                y_pos += 40
        
        # 画像を保存
        img_path = os.path.join(raw_path, f"scene_{i+1}.png")
        img.save(img_path)
        print(f"Created: {img_path}")

def create_placeholder_images(raw_path):
    """プレースホルダー画像を作成（PIL無しの場合）"""
    import subprocess
    
    scenes = [
        "CIRCUIT - F1テーマの筋トレアプリ",
        "3つの意味 - CIRCUITのコンセプト", 
        "タバタ式ワークアウト - 4分間の効率的トレーニング",
        "習慣化サポート - 連続完走でモチベーション維持",
        "記録・管理機能 - データで成果を実感",
        "今すぐ始めよう - 無料でWebブラウザから利用"
    ]
    
    for i, title in enumerate(scenes):
        img_path = os.path.join(raw_path, f"scene_{i+1}.png")
        
        # sips コマンドで単色画像を作成
        subprocess.run([
            "sips", "-c", "1280", "720", 
            "--setProperty", "format", "png",
            "-s", "format", "png",
            "/dev/null", "--out", img_path
        ], capture_output=True)
        
        print(f"Created placeholder: {img_path}")

if __name__ == "__main__":
    create_circuit_video()