#!/bin/sh

# 1～5秒のランダムな秒数を生成
sleep_time=$(
  od -An -N2 -tu2 /dev/urandom | awk '{print 1 + ($1 % 5)}'
)

echo "sleep 時間: ${sleep_time}秒"

  # 開始時刻（秒）を取得
  start=$(date +%s)

# ランダム秒数だけ sleep
sleep "${sleep_time}"

# 終了時刻（秒）を取得
end=$(date +%s)

# 経過時間を計算
elapsed=$((end - start))

# 実行時間を標準出力に表示
echo "実行時間: ${elapsed}秒"
