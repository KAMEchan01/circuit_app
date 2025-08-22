#!/usr/bin/env python3
"""
CIRCUIT解説動画のMP4ファイル生成
imageio-ffmpegを使用して実際のMP4を作成
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio
import tempfile
import shutil

def create_circuit_mp4():
    """CIRCUIT解説動画のMP4を作成"""
    print("🎬 Creating CIRCUIT explanation MP4 video...")
    
    # パス設定
    base_dir = "/Users/kamechan/claude_code/circuit"
    final_dir = os.path.join(base_dir, "videos", "final")
    os.makedirs(final_dir, exist_ok=True)
    
    # 動画設定
    width, height = 1280, 720
    fps = 2  # フレームレート
    duration = 60  # 総時間（秒）
    
    # 出力ファイル
    output_mp4 = os.path.join(final_dir, "circuit_explanation.mp4")
    
    print(f"📱 Video specs: {width}x{height}, {fps}fps, {duration}s")
    
    try:
        # フレームを生成
        frames = generate_video_frames(width, height, fps, duration)
        
        # MP4として保存
        print("💾 Saving MP4 file...")
        imageio.mimsave(output_mp4, frames, fps=fps, quality=8, macro_block_size=1)
        
        print(f"✅ MP4 video created successfully!")
        print(f"📁 File: {output_mp4}")
        
        # ファイル情報を表示
        if os.path.exists(output_mp4):
            file_size = os.path.getsize(output_mp4) / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.2f} MB")
        
        return output_mp4
        
    except Exception as e:
        print(f"❌ Error creating MP4: {e}")
        return None

def generate_video_frames(width, height, fps, duration):
    """動画フレームを生成"""
    
    # 色定義
    colors = {
        'bg': (30, 60, 114),      # ダークブルー
        'red': (255, 107, 107),   # メインレッド
        'teal': (78, 205, 196),   # アクセントティール
        'white': (255, 255, 255), # ホワイト
    }
    
    # シーン定義
    scenes = [
        {
            'title': 'CIRCUIT',
            'subtitle': 'F1テーマの筋トレアプリ',
            'duration': 10,  # 10秒
            'color': colors['red']
        },
        {
            'title': 'タバタ式ワークアウト',
            'subtitle': '20秒運動 + 10秒休憩 × 8セット',
            'duration': 15,  # 15秒
            'color': colors['teal']
        },
        {
            'title': '4分で全身トレーニング',
            'subtitle': '6種類のエクササイズをランダム選択',
            'duration': 15,  # 15秒
            'color': colors['red']
        },
        {
            'title': '習慣化サポート',
            'subtitle': 'F1レーサーのように毎日完走',
            'duration': 10,  # 10秒
            'color': colors['teal']
        },
        {
            'title': '今すぐ始めよう！',
            'subtitle': 'circuit-workout.com',
            'duration': 10,  # 10秒
            'color': colors['red']
        }
    ]
    
    frames = []
    total_frames = fps * duration
    
    print(f"🎞️ Generating {total_frames} frames...")
    
    # フォント設定
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 36)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # 各シーンのフレームを生成
    frame_count = 0
    
    for scene_idx, scene in enumerate(scenes):
        scene_frames = fps * scene['duration']
        
        print(f"  Scene {scene_idx + 1}: {scene['title']} ({scene_frames} frames)")
        
        for frame_in_scene in range(scene_frames):
            if frame_count >= total_frames:
                break
                
            # 画像を作成
            img = Image.new('RGB', (width, height), colors['bg'])
            draw = ImageDraw.Draw(img)
            
            # グラデーション背景
            for y in range(height):
                shade = int(50 * (1 - y / height))
                bg_color = (
                    min(255, colors['bg'][0] + shade),
                    min(255, colors['bg'][1] + shade),
                    min(255, colors['bg'][2] + shade)
                )
                draw.line([(0, y), (width, y)], fill=bg_color)
            
            # アニメーション効果（フェードイン）
            alpha = min(1.0, frame_in_scene / (fps * 2))  # 2秒でフェードイン
            
            # タイトル描画
            title_bbox = draw.textbbox((0, 0), scene['title'], font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            
            # 色にアルファを適用
            title_color = tuple(int(c * alpha) for c in scene['color'])
            
            draw.text((title_x, 250), scene['title'], 
                     fill=title_color, font=title_font)
            
            # サブタイトル描画
            subtitle_bbox = draw.textbbox((0, 0), scene['subtitle'], font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            
            subtitle_color = tuple(int(c * alpha) for c in colors['white'])
            
            draw.text((subtitle_x, 350), scene['subtitle'],
                     fill=subtitle_color, font=subtitle_font)
            
            # 進捗バー
            progress_width = int(width * 0.6)
            progress_x = (width - progress_width) // 2
            progress_y = height - 80
            
            # 背景バー
            draw.rectangle([progress_x, progress_y, progress_x + progress_width, progress_y + 10], 
                          fill=(100, 100, 100))
            
            # 進捗バー
            total_progress = frame_count / total_frames
            filled_width = int(progress_width * total_progress)
            draw.rectangle([progress_x, progress_y, progress_x + filled_width, progress_y + 10], 
                          fill=colors['teal'])
            
            # 画像をnumpy配列に変換
            frame_array = np.array(img)
            frames.append(frame_array)
            
            frame_count += 1
        
        if frame_count >= total_frames:
            break
    
    print(f"  Generated {len(frames)} frames total")
    return frames

if __name__ == "__main__":
    try:
        create_circuit_mp4()
    except ImportError as e:
        print(f"❌ Required library missing: {e}")
        print("Installing required packages...")
        import subprocess
        subprocess.run(["python3", "-m", "pip", "install", "imageio[ffmpeg]", "pillow"], check=True)
        create_circuit_mp4()