#!/bin/bash
# PreToolUse hook: gh pr create コマンドをドラフトPRに強制する

# jqコマンドの存在確認
if ! command -v jq &> /dev/null; then
  exit 0
fi

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
command=$(echo "$input" | jq -r '.tool_input.command')

# Bashツール以外は無視
if [ "$tool_name" != "Bash" ]; then
  exit 0
fi

# gh pr create コマンドでない場合は無視
if ! echo "$command" | grep -qE '\bgh\s+pr\s+create\b'; then
  exit 0
fi

# 既に -d または --draft が含まれている場合はそのまま
if echo "$command" | grep -qE '(\s|^)(-d|--draft)(\s|$)'; then
  exit 0
fi

# --draft フラグを追加
updated_command=$(echo "$command" | sed -E 's/(gh\s+pr\s+create)(\s|$)/\1 --draft\2/')

# JSON出力（jqで安全にエスケープ）
jq -n \
  --arg cmd "$updated_command" \
  '{
    continue: true,
    systemMessage: "Draft flag added automatically to gh pr create command",
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "allow",
      permissionDecisionReason: "Automatically enforcing draft PR creation",
      updatedInput: {
        command: $cmd
      }
    }
  }'

exit 0
