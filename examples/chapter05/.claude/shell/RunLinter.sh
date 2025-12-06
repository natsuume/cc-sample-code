#!/bin/bash

# stdin から JSON を読み取り
HOOK_DATA=$(cat)

# ファイルパスを抽出
FILE_PATH=$(echo "$HOOK_DATA" | jq -r '.tool_input.file_path // empty')

# .pyファイルでなければスキップ
if [[ -z "$FILE_PATH" || "$FILE_PATH" != *.py ]]; then
  exit 0
fi

# ファイルが存在しなければスキップ
if [[ ! -f "$FILE_PATH" ]]; then
  exit 0
fi

# ruff check と format を実行
uvx ruff check --fix "$FILE_PATH" 2>&1
uvx ruff format "$FILE_PATH" 2>&1

exit 0