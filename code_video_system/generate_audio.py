#!/usr/bin/env python3
"""
Generate audio files for each scene using macOS say command
"""

import os
import subprocess
import time

# Define the narration text for each scene
scenes = [
    {
        'id': 'scene01',
        'text': '''このプログラムは、PILライブラリを使用した画像リサイズツールです。
必要なライブラリとして、PILのImageモジュール、osモジュール、sysモジュールをインポートしています。'''
    },
    {
        'id': 'scene02',
        'text': '''設定項目では、プログラムの動作をカスタマイズできます。
sourceFolderで入力画像のフォルダを指定し、outputFolderで出力先を設定します。
outputExtentionでは、pngまたはjpg形式を選択できます。
sizeは、リサイズ時の基準となるピクセル数で、デフォルトは700ピクセルです。
modeでは、リサイズするか元のサイズを維持するかを選択できます。'''
    },
    {
        'id': 'scene03',
        'text': '''calculate_resize_dimensions関数は、画像の縦横比を維持しながら適切なリサイズサイズを計算します。
リサイズモードの場合、横長画像は幅を基準に、縦長画像は高さを基準にサイズを調整します。
これにより、画像の変形を防ぎながら、指定されたサイズに収まるように処理します。
オリジナルモードでは、元の画像サイズをそのまま返します。'''
    },
    {
        'id': 'scene04',
        'text': '''resize_image関数は、実際に画像をリサイズする処理を行います。
PILのresize メソッドを使用して、指定された幅と高さに画像を変更します。
この関数はシンプルですが、プログラムの中核となる処理です。'''
    },
    {
        'id': 'scene05',
        'text': '''プログラムの安全性を確保するため、設定値の検証を行います。
出力形式がpngまたはjpgであることを確認し、
処理モードがresizeまたはoriginalであることをチェックします。
サイズが正の整数であることも検証し、
入力フォルダが存在することを確認します。
エラーがある場合は、分かりやすいメッセージを表示して終了します。'''
    },
    {
        'id': 'scene06',
        'text': '''出力フォルダが存在しない場合は、自動的に作成します。
エラーハンドリングにより、フォルダ作成に失敗した場合も適切に処理します。'''
    },
    {
        'id': 'scene07',
        'text': '''処理した画像数とエラー数をカウントする変数を初期化します。
入力フォルダ内のファイルリストを取得し、
jpg、jpeg、png、bmp、gif形式の画像ファイルのみを処理対象とします。'''
    },
    {
        'id': 'scene08',
        'text': '''各画像ファイルに対して以下の処理を実行します。
まず、画像を読み込み、CMYK形式の場合はRGB形式に変換します。
ファイル名から拡張子を除去し、処理中であることを表示します。
calculate_resize_dimensions関数でリサイズ後のサイズを計算し、
resize_image関数で実際にリサイズを実行します。
最後に、指定された形式で画像を保存し、品質は90に設定しています。'''
    },
    {
        'id': 'scene09',
        'text': '''画像処理中に発生する可能性のあるエラーを適切に処理します。
IOErrorは画像の読み込みや保存に関するエラーを、
その他の例外は予期しないエラーをキャッチします。
エラーが発生しても、他の画像の処理は継続されます。'''
    },
    {
        'id': 'scene10',
        'text': '''すべての処理が完了したら、結果のサマリーを表示します。
処理に成功した画像数と、エラーが発生した画像数を報告し、
ユーザーが処理結果を一目で確認できるようにしています。'''
    }
]

# Japanese voice options for macOS say command
# Available voices: Kyoko, Otoya
voice = 'Kyoko'  # Female Japanese voice
rate = 225  # Speech rate (words per minute) - 1.5x faster than default 150

print(f"Using voice: {voice}")
print(f"Speech rate: {rate} words per minute\n")

# Generate audio for each scene
for scene in scenes:
    output_file = f"audio/{scene['id']}_narration.aiff"
    
    print(f"Generating audio for {scene['id']}...")
    
    # Create the say command
    cmd = [
        'say',
        '-v', voice,
        '-r', str(rate),
        '-o', output_file,
        scene['text']
    ]
    
    try:
        # Execute the command
        subprocess.run(cmd, check=True)
        print(f"  ✓ Saved to {output_file}")
        
        # Get file info
        file_size = os.path.getsize(output_file) / 1024 / 1024  # MB
        print(f"  File size: {file_size:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error generating audio: {e}")
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")

print("\nConverting AIFF files to MP3...")

# Convert AIFF to MP3 for smaller file size
for scene in scenes:
    aiff_file = f"audio/{scene['id']}_narration.aiff"
    mp3_file = f"audio/{scene['id']}_narration.mp3"
    
    if os.path.exists(aiff_file):
        print(f"Converting {scene['id']}...")
        cmd = [
            'ffmpeg',
            '-i', aiff_file,
            '-acodec', 'mp3',
            '-ab', '128k',
            mp3_file,
            '-y'  # Overwrite output file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✓ Converted to {mp3_file}")
            
            # Remove the original AIFF file
            os.remove(aiff_file)
            print(f"  ✓ Removed {aiff_file}")
            
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error converting to MP3: {e}")
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")

print("\nAll audio files generated successfully!")

# Calculate duration of each audio file
print("\nAudio file durations:")
for scene in scenes:
    mp3_file = f"audio/{scene['id']}_narration.mp3"
    if os.path.exists(mp3_file):
        # Get duration using ffprobe
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            mp3_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            duration = float(result.stdout.strip())
            print(f"  {scene['id']}: {duration:.1f} seconds")
        except:
            print(f"  {scene['id']}: Unable to get duration")