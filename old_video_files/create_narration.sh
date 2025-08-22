#!/bin/bash

# ナレーション作成スクリプト
cd /Users/kamechan/claude_code/circuit/videos/raw

echo "Creating narration audio files..."

# シーン1: オープニング (0:00-0:15)
say -v Kyoko -r 150 -o narration_1.aiff "こんにちは！今日は筋トレ初心者でも続けやすい、F1テーマの筋トレアプリ『CIRCUIT』をご紹介します。たった4分で効果的な全身トレーニングができる、タバタ式ワークアウトアプリです。"

# シーン2: コンセプト説明 (0:15-0:45)
say -v Kyoko -r 150 -o narration_2.aiff "CIRCUITという名前には3つの意味が込められています。タバタ式サーキットトレーニング、F1サーキットのような継続的な周回、そして運動→食事→記録の循環する仕組み。F1レースのように、毎日のトレーニングを楽しく続けられるよう設計されています。"

# シーン3: ワークアウト (0:45-2:30)
say -v Kyoko -r 150 -o narration_3.aiff "メインとなるタバタワークアウトは、20秒の運動と10秒の休憩を8セット、合計4分間で行います。プッシュアップ、スクワット、シットアップなど6種類のエクササイズがランダムで選ばれ、飽きることなく全身を鍛えることができます。"

# シーン4: 習慣化 (2:30-3:00)
say -v Kyoko -r 150 -o narration_4.aiff "継続こそが筋トレ成功の鍵。CIRCUITでは連続完走日数を大きく表示し、F1レーサーのように毎日完走を目指すモチベーションを維持できます。"

# シーン5: 記録機能 (3:00-3:30)
say -v Kyoko -r 150 -o narration_5.aiff "食事と運動の記録も簡単。摂取カロリーと消費カロリーを管理し、週間の進捗もグラフで確認できます。タバタ完了時には自動で50kcalの消費カロリーが記録されます。"

# シーン6: クロージング (3:30-4:00)
say -v Kyoko -r 150 -o narration_6.aiff "時間がない現代人でも、たった4分で効果的なトレーニングができるCIRCUIT。F1レースのように毎日の完走を目指して、楽しく健康的な体作りを始めてみませんか？アプリはWebブラウザですぐに利用できます。"

echo "Narration files created successfully!"
echo "Files saved to: $(pwd)"
ls -la narration_*.aiff