#!/usr/bin/env python3
"""
CIRCUIT アプリ解説動画作成スクリプト
"""
import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import numpy as np
from moviepy.editor import *
import tempfile

class CircuitVideoCreator:
    def __init__(self):
        self.driver = None
        self.video_clips = []
        self.audio_clips = []
        self.temp_dir = tempfile.mkdtemp()
        
    def setup_browser(self):
        """ブラウザの設定"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--force-device-scale-factor=1")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1280, 720)
        
    def setup_demo_data(self):
        """デモデータの設定"""
        print("Setting up demo data...")
        
        # デモデータ設定ページを開く
        self.driver.get("https://circuit-workout.com/demo_setup.html")
        time.sleep(2)
        
        # デモデータ設定ボタンをクリック
        setup_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'デモデータを設定')]")
        setup_btn.click()
        time.sleep(2)
        
        print("Demo data setup complete!")
        
    def capture_scene_1_opening(self):
        """シーン1: オープニング (0:00-0:15)"""
        print("Capturing Scene 1: Opening...")
        
        # メインページに移動
        self.driver.get("https://circuit-workout.com/")
        time.sleep(3)
        
        # 15秒間のキャプチャー
        screenshots = []
        for i in range(45):  # 45フレーム（15秒×3fps）
            screenshot = self.driver.get_screenshot_as_png()
            screenshots.append(screenshot)
            time.sleep(1/3)
            
        self.save_scene_video(screenshots, "scene_1_opening.mp4", fps=3)
        
    def capture_scene_2_workout(self):
        """シーン2: ワークアウト実演 (0:45-2:30)"""
        print("Capturing Scene 2: Workout...")
        
        # スタートボタンをクリック
        start_btn = self.driver.find_element(By.ID, "startBtn")
        start_btn.click()
        
        screenshots = []
        # カウントダウン（5秒）
        for i in range(15):
            screenshot = self.driver.get_screenshot_as_png()
            screenshots.append(screenshot)
            time.sleep(1/3)
            
        # ワークアウト中（30秒程度）
        for i in range(90):
            screenshot = self.driver.get_screenshot_as_png()
            screenshots.append(screenshot)
            time.sleep(1/3)
            
        # 停止ボタンをクリック
        stop_btn = self.driver.find_element(By.ID, "startBtn")
        stop_btn.click()
        
        self.save_scene_video(screenshots, "scene_2_workout.mp4", fps=3)
        
    def capture_scene_3_records(self):
        """シーン3: 記録機能 (3:00-3:30)"""
        print("Capturing Scene 3: Records...")
        
        # 記録ページに移動
        record_link = self.driver.find_element(By.XPATH, "//a[@href='record.html']")
        record_link.click()
        time.sleep(3)
        
        screenshots = []
        
        # 記録ページの表示（10秒）
        for i in range(30):
            screenshot = self.driver.get_screenshot_as_png()
            screenshots.append(screenshot)
            time.sleep(1/3)
            
        # タブ切り替え
        food_tab = self.driver.find_element(By.XPATH, "//div[contains(text(), '食事記録')]")
        food_tab.click()
        time.sleep(2)
        
        for i in range(15):
            screenshot = self.driver.get_screenshot_as_png()
            screenshots.append(screenshot)
            time.sleep(1/3)
            
        # 運動タブ
        exercise_tab = self.driver.find_element(By.XPATH, "//div[contains(text(), '運動記録')]")
        exercise_tab.click()
        time.sleep(2)
        
        for i in range(15):
            screenshot = self.driver.get_screenshot_as_png()
            screenshots.append(screenshot)
            time.sleep(1/3)
            
        self.save_scene_video(screenshots, "scene_3_records.mp4", fps=3)
        
    def save_scene_video(self, screenshots, filename, fps=3):
        """スクリーンショットから動画を作成"""
        temp_images = []
        
        for i, screenshot in enumerate(screenshots):
            img_path = os.path.join(self.temp_dir, f"frame_{i:04d}.png")
            with open(img_path, 'wb') as f:
                f.write(screenshot)
            temp_images.append(img_path)
        
        # MoviePyで動画作成
        clip = ImageSequenceClip(temp_images, fps=fps)
        video_path = os.path.join("/Users/kamechan/claude_code/circuit/videos/raw", filename)
        clip.write_videofile(video_path, codec='libx264')
        
        # 一時ファイルをクリーンアップ
        for img_path in temp_images:
            os.remove(img_path)
            
        self.video_clips.append(video_path)
        
    def create_narration_audio(self):
        """ナレーション音声を生成（テキスト読み上げ）"""
        print("Creating narration audio...")
        
        narrations = [
            "こんにちは！今日は筋トレ初心者でも続けやすい、F1テーマの筋トレアプリ『CIRCUIT』をご紹介します。たった4分で効果的な全身トレーニングができる、タバタ式ワークアウトアプリです。",
            "CIRCUITという名前には3つの意味が込められています。タバタ式サーキットトレーニング、F1サーキットのような継続的な周回、そして運動→食事→記録の循環する仕組み。F1レースのように、毎日のトレーニングを楽しく続けられるよう設計されています。",
            "メインとなるタバタワークアウトは、20秒の運動と10秒の休憩を8セット、合計4分間で行います。プッシュアップ、スクワット、シットアップなど6種類のエクササイズがランダムで選ばれ、飽きることなく全身を鍛えることができます。",
            "継続こそが筋トレ成功の鍵。CIRCUITでは連続完走日数を大きく表示し、F1レーサーのように毎日完走を目指すモチベーションを維持できます。",
            "食事と運動の記録も簡単。摂取カロリーと消費カロリーを管理し、週間の進捗もグラフで確認できます。タバタ完了時には自動で50kcalの消費カロリーが記録されます。",
            "時間がない現代人でも、たった4分で効果的なトレーニングができるCIRCUIT。F1レースのように毎日の完走を目指して、楽しく健康的な体作りを始めてみませんか？アプリはWebブラウザですぐに利用できます。"
        ]
        
        # macOSの`say`コマンドを使用してナレーションを生成
        audio_files = []
        for i, text in enumerate(narrations):
            audio_file = f"/Users/kamechan/claude_code/circuit/videos/raw/narration_{i+1}.aiff"
            subprocess.run(["say", "-v", "Kyoko", "-r", "150", "-o", audio_file, text])
            audio_files.append(audio_file)
            
        self.audio_clips = audio_files
        
    def combine_video_audio(self):
        """動画と音声を結合して最終動画を作成"""
        print("Combining video and audio...")
        
        # 全ての動画クリップを結合
        video_clips = [VideoFileClip(path) for path in self.video_clips]
        final_video = concatenate_videoclips(video_clips)
        
        # ナレーション音声を結合
        audio_clips = [AudioFileClip(path) for path in self.audio_clips]
        final_audio = concatenate_audioclips(audio_clips)
        
        # BGMを追加（アプリ内のBGMを使用）
        try:
            bgm = AudioFileClip("/Users/kamechan/claude_code/circuit/sounds/CIRCUIT.mp3").volumex(0.3)
            # BGMをループして動画の長さに合わせる
            if bgm.duration < final_video.duration:
                bgm = afx.audio_loop(bgm, duration=final_video.duration)
            bgm = bgm.subclip(0, final_video.duration)
            
            # ナレーションとBGMをミックス
            final_audio = CompositeAudioClip([final_audio.volumex(0.8), bgm])
        except:
            print("BGM not found, using narration only")
            
        # 動画に音声を追加
        final_video = final_video.set_audio(final_audio)
        
        # 最終動画を出力
        output_path = "/Users/kamechan/claude_code/circuit/videos/final/circuit_explanation.mp4"
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        print(f"Final video saved to: {output_path}")
        
    def cleanup(self):
        """クリーンアップ"""
        if self.driver:
            self.driver.quit()
        
        # 一時ディレクトリを削除
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def create_video(self):
        """メイン処理：動画作成の全工程"""
        try:
            self.setup_browser()
            self.setup_demo_data()
            
            # 各シーンをキャプチャー
            self.capture_scene_1_opening()
            self.capture_scene_2_workout()
            self.capture_scene_3_records()
            
            # ナレーション作成
            self.create_narration_audio()
            
            # 動画と音声を結合
            self.combine_video_audio()
            
            print("Video creation completed successfully!")
            
        except Exception as e:
            print(f"Error during video creation: {e}")
            
        finally:
            self.cleanup()

if __name__ == "__main__":
    creator = CircuitVideoCreator()
    creator.create_video()