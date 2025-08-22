#!/usr/bin/env python3
"""
画像リサイズツール - rbeta.py
PILライブラリを使用した高機能画像リサイズプログラム
"""

# 必要なライブラリのインポート
from PIL import Image
import os
import sys

# 設定項目
sourceFolder = "input_images"      # 入力画像フォルダ
outputFolder = "output_images"     # 出力先フォルダ
outputExtention = "png"            # 出力形式 (png または jpg)
size = 700                         # リサイズ基準サイズ（ピクセル）
mode = "resize"                    # 処理モード: "resize" または "original"


def calculate_resize_dimensions(original_width, original_height, target_size, resize_mode):
    """
    画像の縦横比を維持しながら適切なリサイズサイズを計算する
    
    Args:
        original_width (int): 元の画像の幅
        original_height (int): 元の画像の高さ
        target_size (int): 目標サイズ
        resize_mode (str): リサイズモード ("resize" または "original")
    
    Returns:
        tuple: (新しい幅, 新しい高さ)
    """
    if resize_mode == "original":
        return original_width, original_height
    
    # 縦横比を計算
    aspect_ratio = original_width / original_height
    
    if original_width > original_height:
        # 横長画像：幅を基準にリサイズ
        new_width = target_size
        new_height = int(target_size / aspect_ratio)
    else:
        # 縦長画像：高さを基準にリサイズ
        new_height = target_size
        new_width = int(target_size * aspect_ratio)
    
    return new_width, new_height


def resize_image(img, width, height):
    """
    画像を指定されたサイズにリサイズする
    
    Args:
        img (PIL.Image): PIL画像オブジェクト
        width (int): 新しい幅
        height (int): 新しい高さ
    
    Returns:
        PIL.Image: リサイズされた画像
    """
    return img.resize((width, height), Image.Resampling.LANCZOS)


# 設定値の検証
if outputExtention not in ["png", "jpg"]:
    print("エラー: 出力形式は 'png' または 'jpg' を指定してください")
    sys.exit(1)

if mode not in ["resize", "original"]:
    print("エラー: モードは 'resize' または 'original' を指定してください")
    sys.exit(1)

if size <= 0:
    print("エラー: サイズは正の整数を指定してください")
    sys.exit(1)

if not os.path.exists(sourceFolder):
    print(f"エラー: 入力フォルダ '{sourceFolder}' が存在しません")
    sys.exit(1)

# 出力フォルダの作成
try:
    os.makedirs(outputFolder, exist_ok=True)
    print(f"出力フォルダを準備しました: {outputFolder}")
except Exception as e:
    print(f"エラー: 出力フォルダの作成に失敗しました - {e}")
    sys.exit(1)

# 処理統計の初期化
processed_count = 0
error_count = 0

# 処理対象ファイルの抽出
print(f"'{sourceFolder}' フォルダ内の画像ファイルを検索中...")
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
image_files = []

for filename in os.listdir(sourceFolder):
    if any(filename.lower().endswith(ext) for ext in image_extensions):
        image_files.append(filename)

if not image_files:
    print("処理対象の画像ファイルが見つかりませんでした")
    sys.exit(0)

print(f"見つかった画像ファイル: {len(image_files)}個")

# メイン処理ループ
for filename in image_files:
    try:
        # 画像の読み込み
        input_path = os.path.join(sourceFolder, filename)
        img = Image.open(input_path)
        
        # CMYK形式の場合はRGBに変換
        if img.mode == 'CMYK':
            img = img.convert('RGB')
        
        # ファイル名から拡張子を除去
        name_without_ext = os.path.splitext(filename)[0]
        
        print(f"処理中: {filename} ({img.size[0]}×{img.size[1]})")
        
        # リサイズ後のサイズを計算
        new_width, new_height = calculate_resize_dimensions(
            img.size[0], img.size[1], size, mode
        )
        
        # 画像をリサイズ
        resized_img = resize_image(img, new_width, new_height)
        
        # 出力ファイル名の生成
        output_filename = f"{name_without_ext}.{outputExtention}"
        output_path = os.path.join(outputFolder, output_filename)
        
        # 画像の保存
        if outputExtention == "jpg":
            resized_img.save(output_path, "JPEG", quality=90)
        else:
            resized_img.save(output_path, "PNG")
        
        print(f"  ✓ 完了: {output_filename} ({new_width}×{new_height})")
        processed_count += 1
        
    except IOError as e:
        print(f"  ✗ IOエラー: {filename} - {e}")
        error_count += 1
    except Exception as e:
        print(f"  ✗ 予期しないエラー: {filename} - {e}")
        error_count += 1

# 処理結果のサマリー表示
print("\n" + "="*50)
print("処理完了サマリー")
print(f"処理成功: {processed_count}個")
print(f"エラー発生: {error_count}個")
print("="*50)