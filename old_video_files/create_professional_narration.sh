#!/bin/bash

# CIRCUIT解説動画用プロフェッショナルナレーション作成

echo "🎙️ Creating professional narration for CIRCUIT video..."

BASE_DIR="/Users/kamechan/claude_code/circuit"
AUDIO_DIR="$BASE_DIR/videos/audio"
mkdir -p "$AUDIO_DIR"

echo "📝 Creating enhanced narration scripts..."

# 改良されたナレーション台本（より自然で魅力的）
create_narration_scripts() {

# シーン1: オープニング（15秒）
cat > "$AUDIO_DIR/narration_01_script.txt" << 'EOF'
忙しい毎日で運動が続かない...そんなあなたに朗報です！

今日ご紹介するのは、わずか4分で全身を鍛える革新的なフィットネスアプリ「CIRCUIT」。

F1レースのスリルと科学的に証明されたタバタ式トレーニングを組み合わせた、全く新しい筋トレ体験をお届けします。
EOF

# シーン2: コンセプト説明（20秒）
cat > "$AUDIO_DIR/narration_02_script.txt" << 'EOF'
「CIRCUIT」という名前には特別な意味があります。

サーキットトレーニングの「サーキット」、F1サーキットの「継続的な周回」、そして電子回路のように運動・食事・記録が循環する仕組み。

毎日のトレーニングを、まるでF1レースのように楽しく継続できるよう設計されています。
EOF

# シーン3: タバタ式ワークアウト（45秒）
cat > "$AUDIO_DIR/narration_03_script.txt" << 'EOF'
CIRCUITの核となるのは、科学的に効果が実証されたタバタ式ワークアウトです。

20秒の全力運動と10秒の休憩を8セット繰り返す、合計4分間の集中トレーニング。

プッシュアップ、スクワット、シットアップなど6種類のエクササイズがランダムに選ばれるため、毎回新鮮な気持ちで取り組めます。

短時間なのに、長時間の有酸素運動と同等の効果を得ることができる、まさに現代人のためのトレーニング方法です。
EOF

# シーン4: 習慣化機能（15秒）
cat > "$AUDIO_DIR/narration_04_script.txt" << 'EOF'
運動の成功は「継続」にあります。

CIRCUITでは、あなたの連続完走日数を大きく表示。F1レーサーのように、毎日のレースを完走することで達成感を積み重ね、自然と習慣が身につきます。

三日坊主はもう卒業です。
EOF

# シーン5: 記録機能（15秒）  
cat > "$AUDIO_DIR/narration_05_script.txt" << 'EOF'
食事と運動の記録もとっても簡単。

摂取カロリーと消費カロリーを手軽に管理でき、週間の進捗もグラフで一目瞭然。

タバタワークアウト完了時には、自動で50キロカロリーの消費カロリーが記録されるので、成果を実感できます。
EOF

# シーン6: クロージング（15秒）
cat > "$AUDIO_DIR/narration_06_script.txt" << 'EOF'
時間がない現代人でも、たった4分で効果的なトレーニングができるCIRCUIT。

F1レースのように毎日の完走を目指して、楽しく健康的な体作りを始めませんか？

アプリは完全無料。今すぐWebブラウザから利用を開始できます。

circuit-workout.com で、あなたの新しいフィットネス体験をスタートしましょう！
EOF

echo "✅ Enhanced narration scripts created"
}

# より自然な音声合成のためのパラメーター調整
create_professional_audio() {
    echo "🎵 Creating professional audio with enhanced settings..."
    
    # 音声合成設定
    VOICE="Kyoko"       # 日本語の自然な音声
    RATE="140"          # 読み上げ速度（やや遅め、聞き取りやすい）
    OUTPUT_FORMAT="WAVE"
    
    # 各ナレーションを生成
    for i in {1..6}; do
        echo "  Processing narration ${i}..."
        
        script_file="$AUDIO_DIR/narration_$(printf "%02d" $i)_script.txt"
        audio_file="$AUDIO_DIR/narration_$(printf "%02d" $i).wav"
        
        if [ -f "$script_file" ]; then
            # より高品質な音声合成
            say -v "$VOICE" -r "$RATE" -o "$audio_file" --data-format=LEF32@44100 -f "$script_file"
            
            # 音声後処理（ノーマライゼーション）
            if command -v sox &> /dev/null; then
                echo "    Applying audio enhancement..."
                sox "$audio_file" "${audio_file%.wav}_enhanced.wav" norm -3 compand 0.3,1 6:-70,-60,-20 -5 -90 0.2
                mv "${audio_file%.wav}_enhanced.wav" "$audio_file"
            fi
        fi
    done
    
    echo "✅ Professional narration audio created"
}

# BGM音楽の準備・編集
prepare_background_music() {
    echo "🎶 Preparing background music..."
    
    BGM_SOURCE="$BASE_DIR/sounds/CIRCUIT.mp3"
    BGM_OUTPUT="$AUDIO_DIR/background_music.wav"
    
    if [ -f "$BGM_SOURCE" ]; then
        # BGMをWAV形式に変換し、音量を調整
        if command -v sox &> /dev/null; then
            sox "$BGM_SOURCE" "$BGM_OUTPUT" vol 0.3 norm -6
        else
            # afconvert を使用（macOS標準）
            afconvert "$BGM_SOURCE" "$BGM_OUTPUT" -d LEI16@44100 -f WAVE
        fi
        
        echo "✅ Background music prepared"
    else
        echo "⚠️  BGM source file not found: $BGM_SOURCE"
    fi
}

# 最終音声ミックス
create_final_audio_mix() {
    echo "🎧 Creating final audio mix..."
    
    FINAL_AUDIO="$AUDIO_DIR/final_mixed_audio.wav"
    
    # 全ナレーションを結合
    NARRATION_FILES=""
    for i in {1..6}; do
        audio_file="$AUDIO_DIR/narration_$(printf "%02d" $i).wav"
        if [ -f "$audio_file" ]; then
            NARRATION_FILES="$NARRATION_FILES $audio_file"
        fi
    done
    
    if [ ! -z "$NARRATION_FILES" ]; then
        # soxを使用してファイルを結合
        if command -v sox &> /dev/null; then
            sox $NARRATION_FILES "$AUDIO_DIR/combined_narration.wav"
            
            # BGMとミックス
            if [ -f "$AUDIO_DIR/background_music.wav" ]; then
                sox -m "$AUDIO_DIR/combined_narration.wav" "$AUDIO_DIR/background_music.wav" "$FINAL_AUDIO" norm -3
            else
                cp "$AUDIO_DIR/combined_narration.wav" "$FINAL_AUDIO"
            fi
        else
            # macOS標準ツールでの簡易結合
            cat $NARRATION_FILES > "$FINAL_AUDIO"
        fi
        
        echo "✅ Final audio mix created: $FINAL_AUDIO"
    fi
}

# メイン処理
main() {
    create_narration_scripts
    create_professional_audio
    prepare_background_music
    create_final_audio_mix
    
    echo ""
    echo "🎉 Professional narration creation completed!"
    echo "📁 Audio files location: $AUDIO_DIR"
    echo ""
    echo "📋 Created files:"
    ls -la "$AUDIO_DIR"/*.wav 2>/dev/null || echo "  No audio files found"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Review and test audio quality"
    echo "2. Combine with high-quality visuals"  
    echo "3. Create professional video edit"
}

# SoXの確認・インストール
check_sox() {
    if ! command -v sox &> /dev/null; then
        echo "📦 Installing SoX for audio processing..."
        brew install sox
    fi
}

# 実行
check_sox
main