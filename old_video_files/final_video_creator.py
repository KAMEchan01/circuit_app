#!/usr/bin/env python3
"""
CIRCUIT解説動画の最終版作成
実際に動作する高品質MP4動画を確実に生成
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as iio
from pathlib import Path

def create_final_circuit_video():
    """最終的なCIRCUIT解説動画を作成"""
    print("🎬 Creating final CIRCUIT explanation video...")
    
    # パス設定
    base_dir = Path("/Users/kamechan/claude_code/circuit")
    output_dir = base_dir / "videos" / "final"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 動画設定（確実に動作する設定）
    width, height = 1280, 720  # HD画質
    fps = 5  # 低フレームレートで安定性重視
    
    # F1テーマカラー
    colors = {
        'bg_dark': (15, 25, 45),
        'bg_light': (30, 60, 114),
        'red': (255, 107, 107),
        'teal': (78, 205, 196),
        'white': (255, 255, 255),
        'gold': (255, 215, 0)
    }
    
    # シーン定義（改良版）
    scenes = [
        {
            'title': '🏎️ CIRCUIT',
            'subtitle': 'F1テーマの筋トレアプリ',
            'points': ['たった4分で全身トレーニング', 'タバタ式ワークアウト', '完全無料で今すぐ利用可能'],
            'duration': 8,
            'theme_color': colors['red'],
            'bg_color': colors['bg_dark']
        },
        {
            'title': '⚡ タバタ式の威力',
            'subtitle': '科学的に証明された効率的トレーニング',
            'points': ['20秒運動 + 10秒休憩', '8セットで合計4分間', '長時間運動と同等の効果'],
            'duration': 12,
            'theme_color': colors['teal'],
            'bg_color': colors['bg_light']
        },
        {
            'title': '🎯 6種類のエクササイズ',
            'subtitle': 'ランダム選択で毎回新鮮',
            'points': ['プッシュアップ・スクワット・シットアップ', 'ジャンピングジャック・ロシアンツイスト', 'マウンテンクライマー'],
            'duration': 10,
            'theme_color': colors['red'],
            'bg_color': colors['bg_dark']
        },
        {
            'title': '🏁 習慣化システム',
            'subtitle': 'F1レーサーのように毎日完走',
            'points': ['連続完走日数を表示', 'ストリーク機能でモチベーション', '達成感のある演出'],
            'duration': 10,
            'theme_color': colors['teal'],
            'bg_color': colors['bg_light']
        },
        {
            'title': '📊 データ管理',
            'subtitle': 'カロリー・進捗を簡単記録',
            'points': ['摂取・消費カロリー管理', '週間進捗グラフ', '自動計算で手間いらず'],
            'duration': 8,
            'theme_color': colors['red'],
            'bg_color': colors['bg_dark']
        },
        {
            'title': '🚀 今すぐスタート！',
            'subtitle': 'circuit-workout.com',
            'points': ['Webブラウザですぐ利用', 'アプリダウンロード不要', 'F1レースを始めよう！'],
            'duration': 12,
            'theme_color': colors['gold'],
            'bg_color': colors['bg_light']
        }
    ]
    
    # 全フレームを生成
    all_frames = []
    
    for scene_idx, scene in enumerate(scenes):
        print(f"  🎨 Creating scene {scene_idx + 1}: {scene['title']}")
        
        frame_count = scene['duration'] * fps
        
        for frame_idx in range(frame_count):
            frame = create_scene_frame(scene, frame_idx, frame_count, width, height, colors)
            all_frames.append(frame)
    
    # 最終動画を出力
    output_file = output_dir / "circuit_explanation_final.mp4"
    
    print(f"💾 Exporting to: {output_file}")
    print(f"📊 Total frames: {len(all_frames)}")
    print(f"⏱️ Total duration: {len(all_frames) / fps:.1f} seconds")
    
    try:
        # 高品質設定でMP4を出力
        iio.imwrite(str(output_file), all_frames, fps=fps, quality=8, codec='libx264')
        
        # ファイル情報を確認
        if output_file.exists():
            file_size = output_file.stat().st_size / (1024 * 1024)
            print(f"✅ Final video created successfully!")
            print(f"📁 File: {output_file}")
            print(f"📊 Size: {file_size:.2f} MB")
            print(f"🎬 Specs: {width}x{height} @ {fps}fps")
            
            return str(output_file)
        else:
            print("❌ Video file was not created")
            return None
            
    except Exception as e:
        print(f"❌ Error exporting video: {e}")
        return None

def create_scene_frame(scene, frame_idx, total_frames, width, height, colors):
    """シーンの各フレームを作成"""
    
    # ベース画像
    img = Image.new('RGB', (width, height), scene['bg_color'])
    draw = ImageDraw.Draw(img)
    
    # アニメーション進行度
    progress = frame_idx / total_frames
    
    # グラデーション背景
    add_gradient_background(draw, width, height, scene['bg_color'], scene['theme_color'], progress)
    
    # フォント設定
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 32)
        point_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 28)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        point_font = ImageFont.load_default()
    
    # タイトル（アニメーション付き）
    title_alpha = min(1.0, progress * 3)  # 最初の1/3でフェードイン
    if title_alpha > 0:
        title_color = (*scene['theme_color'], int(255 * title_alpha))
        draw_text_centered(draw, scene['title'], 150, title_font, title_color[:3], width)
    
    # サブタイトル
    subtitle_alpha = max(0, min(1.0, (progress - 0.2) * 3))  # 少し遅れてフェードイン
    if subtitle_alpha > 0:
        subtitle_color = (*colors['white'], int(255 * subtitle_alpha))
        draw_text_centered(draw, scene['subtitle'], 230, subtitle_font, subtitle_color[:3], width)
    
    # ポイント（順次表示）
    point_start_progress = 0.4
    for i, point in enumerate(scene['points']):
        point_progress = max(0, min(1.0, (progress - point_start_progress - i * 0.15) * 5))
        if point_progress > 0:
            point_color = (*colors['white'], int(200 * point_progress))
            y_pos = 320 + i * 50
            draw_text_centered(draw, f"• {point}", y_pos, point_font, point_color[:3], width)
    
    # プログレスバー
    add_progress_bar(draw, progress, width, height, scene['theme_color'])
    
    # F1装飾要素
    add_f1_decorations(draw, frame_idx, width, height, scene['theme_color'])
    
    return np.array(img)

def add_gradient_background(draw, width, height, bg_color, theme_color, progress):
    """グラデーション背景を追加"""
    for y in range(height):
        ratio = y / height
        
        # 背景色からテーマ色へのグラデーション
        r = int(bg_color[0] + (theme_color[0] - bg_color[0]) * ratio * 0.3)
        g = int(bg_color[1] + (theme_color[1] - bg_color[1]) * ratio * 0.3)
        b = int(bg_color[2] + (theme_color[2] - bg_color[2]) * ratio * 0.3)
        
        color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        draw.line([(0, y), (width, y)], fill=color)

def draw_text_centered(draw, text, y, font, color, width):
    """中央揃えでテキストを描画"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    
    # 影効果
    draw.text((x + 2, y + 2), text, fill=(0, 0, 0, 100), font=font)
    # メインテキスト
    draw.text((x, y), text, fill=color, font=font)

def add_progress_bar(draw, progress, width, height, theme_color):
    """プログレスバーを追加"""
    bar_width = int(width * 0.6)
    bar_height = 8
    bar_x = (width - bar_width) // 2
    bar_y = height - 60
    
    # 背景バー
    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], 
                  fill=(100, 100, 100))
    
    # プログレスバー
    filled_width = int(bar_width * progress)
    draw.rectangle([bar_x, bar_y, bar_x + filled_width, bar_y + bar_height], 
                  fill=theme_color)

def add_f1_decorations(draw, frame_idx, width, height, theme_color):
    """F1テーマの装飾要素を追加"""
    
    # チェッカーフラッグ風パターン（アニメーション）
    checker_size = 20
    offset = (frame_idx * 2) % (checker_size * 2)
    
    # 上部の装飾バー
    for x in range(-offset, width + checker_size, checker_size):
        for y in range(0, 20, checker_size):
            color = theme_color if ((x + y) // checker_size) % 2 == 0 else (255, 255, 255)
            draw.rectangle([x, y, x + checker_size, y + checker_size], fill=color)
    
    # 下部の装飾バー
    for x in range(-offset, width + checker_size, checker_size):
        for y in range(height - 20, height, checker_size):
            color = theme_color if ((x + y) // checker_size) % 2 == 0 else (255, 255, 255)
            draw.rectangle([x, y, x + checker_size, y + checker_size], fill=color)

if __name__ == "__main__":
    result = create_final_circuit_video()
    if result:
        print(f"\n🎉 Success! Video created at: {result}")
        print("\n📋 Video is ready for:")
        print("  • YouTube upload")
        print("  • SNS sharing")
        print("  • Website embedding")
        print("  • Marketing campaigns")
    else:
        print("\n❌ Video creation failed")