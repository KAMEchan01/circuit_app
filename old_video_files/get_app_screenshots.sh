#!/bin/bash

# CIRCUITアプリの高品質スクリーンショット取得

echo "📸 Getting high-quality CIRCUIT app screenshots..."

SCREENSHOTS_DIR="/Users/kamechan/claude_code/circuit/videos/screenshots"
mkdir -p "$SCREENSHOTS_DIR"

echo "🌐 Opening CIRCUIT app in Chrome..."

# Chrome用のAppleScript
osascript << 'EOF'
tell application "Google Chrome"
    activate
    
    -- 新しいタブでデモデータ設定ページを開く
    set myTab to make new tab at end of tabs of front window
    set URL of myTab to "https://circuit-workout.com/demo_setup.html"
    delay 3
    
    -- デモデータを設定
    tell myTab to execute javascript "document.querySelector('button').click();"
    delay 2
    
    -- メインページに移動
    set URL of myTab to "https://circuit-workout.com/"
    delay 4
    
    -- ウィンドウを最大化
    tell front window to set bounds to {0, 0, 1440, 900}
    delay 2
end tell

-- 自動スクリーンショット撮影の指示
display dialog "📸 CIRCUIT アプリが開きました！

以下の手順で高品質スクリーンショットを撮影します：

1. 【ホーム画面】 - 現在の画面
2. 【ワークアウト開始】 - スタートボタンをクリック後
3. 【運動中画面】 - タイマー動作中
4. 【記録画面】 - 記録ページ

スクリーンショット撮影を開始しますか？" buttons {"キャンセル", "開始"} default button "開始"

set response to result
if button returned of response is "開始" then
    -- ホーム画面のスクリーンショット
    display dialog "1/4: ホーム画面をキャプチャーします
    
Command+Shift+4 を押して、アプリ画面全体を選択してください。
撮影後「次へ」をクリック" buttons {"次へ"}
    
    -- ワークアウト画面のスクリーンショット
    tell application "Google Chrome"
        tell front tab of front window to execute javascript "document.getElementById('startBtn').click();"
    end tell
    delay 3
    
    display dialog "2/4: ワークアウト画面をキャプチャーします
    
Command+Shift+4 を押して、カウントダウン・運動画面を撮影してください。
撮影後「次へ」をクリック" buttons {"次へ"}
    
    delay 10
    
    -- 停止してから記録画面へ
    tell application "Google Chrome"
        tell front tab of front window to execute javascript "document.getElementById('startBtn').click();"
        delay 2
        tell front tab of front window to execute javascript "window.location.href='record.html';"
    end tell
    delay 3
    
    display dialog "3/4: 記録画面をキャプチャーします
    
Command+Shift+4 を押して、記録・管理画面を撮影してください。
撮影後「次へ」をクリック" buttons {"次へ"}
    
    display dialog "4/4: モバイル表示でもう一度ホーム画面を撮影
    
1. Chromeの開発者ツール (Command+Option+I) を開く
2. デバイスツールバー（スマホアイコン）をクリック
3. iPhone 12 Pro を選択
4. https://circuit-workout.com/ に移動
5. Command+Shift+4 で撮影

完了後「終了」をクリック" buttons {"終了"}
    
end if

EOF

echo "📁 スクリーンショットの保存場所: $SCREENSHOTS_DIR"
echo ""
echo "📋 撮影したスクリーンショットを以下の名前で保存してください："
echo "  - 01_home_desktop.png     (デスクトップ版ホーム画面)"
echo "  - 02_workout_active.png   (ワークアウト実行中)"
echo "  - 03_records_page.png     (記録・管理画面)"
echo "  - 04_mobile_home.png      (モバイル版ホーム画面)"
echo ""
echo "✅ スクリーンショット撮影準備完了！"