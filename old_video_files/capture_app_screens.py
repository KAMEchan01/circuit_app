#!/usr/bin/env python3
"""
CIRCUITアプリの実際のスクリーンショットを自動撮影
高品質な動画素材を作成
"""
import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import io

class CircuitAppScreenCapture:
    def __init__(self):
        self.driver = None
        self.screenshots_dir = "/Users/kamechan/claude_code/circuit/videos/screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
    def setup_browser(self):
        """ブラウザ設定（高品質スクリーンショット用）"""
        print("🌐 Setting up high-quality browser...")
        
        chrome_options = Options()
        chrome_options.add_argument("--force-device-scale-factor=2")  # Retina品質
        chrome_options.add_argument("--high-dpi-support=1")
        chrome_options.add_argument("--window-size=1440,900")  # より大きなウィンドウ
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1440, 900)
        
    def setup_demo_data(self):
        """デモデータの設定"""
        print("📊 Setting up demo data...")
        
        try:
            # デモデータ設定ページ
            self.driver.get("https://circuit-workout.com/demo_setup.html")
            time.sleep(3)
            
            # デモデータ設定ボタンをクリック
            setup_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'デモデータを設定')]"))
            )
            setup_btn.click()
            time.sleep(2)
            
            print("✅ Demo data setup completed")
            
        except Exception as e:
            print(f"⚠️  Demo data setup failed: {e}")
            
    def capture_home_screen(self):
        """ホーム画面のスクリーンショット"""
        print("📸 Capturing home screen...")
        
        try:
            self.driver.get("https://circuit-workout.com/")
            time.sleep(4)  # ページ読み込み待機
            
            # ページが完全に読み込まれるまで待機
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "startBtn"))
            )
            
            # スクリーンショット撮影
            screenshot_data = self.driver.get_screenshot_as_png()
            
            # 高品質で保存
            image = Image.open(io.BytesIO(screenshot_data))
            image.save(os.path.join(self.screenshots_dir, "01_home_screen.png"), 
                      "PNG", optimize=True, quality=95)
            
            print("✅ Home screen captured")
            
        except Exception as e:
            print(f"❌ Home screen capture failed: {e}")
            
    def capture_workout_sequence(self):
        """ワークアウト画面のシーケンス撮影"""
        print("🏋️‍♀️ Capturing workout sequence...")
        
        try:
            # スタートボタンをクリック
            start_btn = self.driver.find_element(By.ID, "startBtn")
            start_btn.click()
            time.sleep(1)
            
            # カウントダウン画面をキャプチャー
            for i in range(5):  # 5秒カウントダウン
                screenshot_data = self.driver.get_screenshot_as_png()
                image = Image.open(io.BytesIO(screenshot_data))
                image.save(os.path.join(self.screenshots_dir, f"02_countdown_{5-i}.png"), 
                          "PNG", optimize=True, quality=95)
                time.sleep(1)
            
            # ワークアウト中の画面をキャプチャー
            for i in range(10):  # 10秒間キャプチャー
                screenshot_data = self.driver.get_screenshot_as_png()
                image = Image.open(io.BytesIO(screenshot_data))
                image.save(os.path.join(self.screenshots_dir, f"03_workout_{i+1:02d}.png"), 
                          "PNG", optimize=True, quality=95)
                time.sleep(1)
            
            # 停止ボタンをクリック
            stop_btn = self.driver.find_element(By.ID, "startBtn")
            stop_btn.click()
            time.sleep(2)
            
            print("✅ Workout sequence captured")
            
        except Exception as e:
            print(f"❌ Workout capture failed: {e}")
            
    def capture_record_screen(self):
        """記録画面のスクリーンショット"""
        print("📊 Capturing record screen...")
        
        try:
            # 記録ページに移動
            record_link = self.driver.find_element(By.XPATH, "//a[@href='record.html']")
            record_link.click()
            time.sleep(3)
            
            # メイン記録画面
            screenshot_data = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot_data))
            image.save(os.path.join(self.screenshots_dir, "04_records_main.png"), 
                      "PNG", optimize=True, quality=95)
            
            # 食事記録タブ
            food_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '食事記録')]"))
            )
            food_tab.click()
            time.sleep(2)
            
            screenshot_data = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot_data))
            image.save(os.path.join(self.screenshots_dir, "05_records_food.png"), 
                      "PNG", optimize=True, quality=95)
            
            # 運動記録タブ
            exercise_tab = self.driver.find_element(By.XPATH, "//div[contains(text(), '運動記録')]")
            exercise_tab.click()
            time.sleep(2)
            
            screenshot_data = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot_data))
            image.save(os.path.join(self.screenshots_dir, "06_records_exercise.png"), 
                      "PNG", optimize=True, quality=95)
            
            # 履歴タブ
            history_tab = self.driver.find_element(By.XPATH, "//div[contains(text(), '履歴')]")
            history_tab.click()
            time.sleep(2)
            
            screenshot_data = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot_data))
            image.save(os.path.join(self.screenshots_dir, "07_records_history.png"), 
                      "PNG", optimize=True, quality=95)
            
            print("✅ Record screens captured")
            
        except Exception as e:
            print(f"❌ Record screen capture failed: {e}")
            
    def capture_mobile_view(self):
        """モバイル表示でのスクリーンショット"""
        print("📱 Capturing mobile view...")
        
        try:
            # モバイルビューに変更
            self.driver.set_window_size(375, 812)  # iPhone X サイズ
            
            # ホーム画面（モバイル）
            self.driver.get("https://circuit-workout.com/")
            time.sleep(3)
            
            screenshot_data = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot_data))
            image.save(os.path.join(self.screenshots_dir, "08_mobile_home.png"), 
                      "PNG", optimize=True, quality=95)
            
            print("✅ Mobile view captured")
            
        except Exception as e:
            print(f"❌ Mobile view capture failed: {e}")
            
    def create_summary_image(self):
        """まとめ画像を作成"""
        print("🎨 Creating summary image...")
        
        try:
            # 複数のスクリーンショットを組み合わせたコラージュを作成
            from PIL import Image, ImageDraw, ImageFont
            
            # 背景画像
            summary_img = Image.new('RGB', (1920, 1080), (30, 60, 114))
            draw = ImageDraw.Draw(summary_img)
            
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 72)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", 36)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # タイトル
            draw.text((100, 50), "CIRCUIT", fill=(255, 107, 107), font=title_font)
            draw.text((100, 150), "F1テーマの筋トレアプリ", fill=(255, 255, 255), font=subtitle_font)
            draw.text((100, 200), "たった4分で全身トレーニング", fill=(78, 205, 196), font=subtitle_font)
            
            # スクリーンショットを配置
            screenshots = [
                "01_home_screen.png",
                "03_workout_01.png",
                "04_records_main.png",
                "08_mobile_home.png"
            ]
            
            positions = [(100, 300), (600, 300), (1100, 300), (100, 700)]
            
            for i, (screenshot, pos) in enumerate(zip(screenshots, positions)):
                screenshot_path = os.path.join(self.screenshots_dir, screenshot)
                if os.path.exists(screenshot_path):
                    screenshot_img = Image.open(screenshot_path)
                    screenshot_img = screenshot_img.resize((400, 300))  # リサイズ
                    summary_img.paste(screenshot_img, pos)
            
            # アプリURL
            draw.text((100, 950), "circuit-workout.com", fill=(255, 255, 255), font=subtitle_font)
            
            summary_img.save(os.path.join(self.screenshots_dir, "00_app_summary.png"), 
                           "PNG", optimize=True, quality=95)
            
            print("✅ Summary image created")
            
        except Exception as e:
            print(f"❌ Summary image creation failed: {e}")
            
    def cleanup(self):
        """クリーンアップ"""
        if self.driver:
            self.driver.quit()
            
    def capture_all(self):
        """すべてのスクリーンショットを撮影"""
        try:
            self.setup_browser()
            self.setup_demo_data()
            
            # 各画面をキャプチャー
            self.capture_home_screen()
            self.capture_workout_sequence()
            self.capture_record_screen()
            self.capture_mobile_view()
            self.create_summary_image()
            
            print(f"\n✅ All screenshots captured successfully!")
            print(f"📁 Screenshots saved to: {self.screenshots_dir}")
            
            # 撮影したファイルを一覧表示
            screenshot_files = sorted([f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')])
            print(f"📸 Captured {len(screenshot_files)} screenshots:")
            for file in screenshot_files:
                print(f"  - {file}")
                
        except Exception as e:
            print(f"❌ Screenshot capture failed: {e}")
            
        finally:
            self.cleanup()

if __name__ == "__main__":
    capture = CircuitAppScreenCapture()
    capture.capture_all()