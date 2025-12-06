#!/bin/bash
set -euo pipefail

# stdin から JSON を読み取り
HOOK_DATA=$(cat)

# ファイルパスを抽出
FILE_PATH=$(echo "$HOOK_DATA" | jq -r '.tool_input.file_path // empty')

# ファイルパスを正規化し、想定ディレクトリ内か確認
SRC_DIR="$(pwd)"  # 必要に応じて適切なディレクトリに変更
FILE_PATH=$(realpath -m "$FILE_PATH" 2>/dev/null)
if [[ -z "$FILE_PATH" || "${FILE_PATH:0:${#SRC_DIR}}" != "$SRC_DIR" ]]; then
  echo "不正なファイルパス: $FILE_PATH"
  exit 0
fi
# .pyファイルでなければスキップ
if [[ -z "$FILE_PATH" || "$FILE_PATH" != *.py ]]; then
  exit 0
fi

# ファイルが存在しなければスキップ
if [[ ! -f "$FILE_PATH" ]]; then
  exit 0
fi

# ruff check と format を実行
if ! uvx ruff check --fix "$FILE_PATH" 2>&1; then
  echo "警告: ruff check でエラーが発生しました" >&2
fi
uvx ruff format "$FILE_PATH"

exit 0