# cc-sample-code

「Claude Code開発体系 拡張・制御・運用の手引き」書籍のサンプルコードリポジトリです。

## 概要

このリポジトリには、Claude Code（Anthropic公式CLI）の拡張・制御・運用に関するサンプルコードが含まれています。

## ディレクトリ構成

### examples/

チャプター別のサンプルコード

| チャプター | 内容 | 主なファイル |
|-----------|------|-------------|
| chapter01 | Attribution設定 | `.claude/settings.json` |
| chapter02 | MCP Server実装 | `mcp-server_minimal/typescript/` |
| chapter03 | Agent定義 | `.claude/agents/multi-perspective-analyzer.md` |
| chapter04 | Commands & Skills | `.claude/commands/`, `.claude/skills/` |
| chapter05 | Hooks | `.claude/hooks.json`, `shell/` |

### plugins/

マーケットプレイスプラグインのサンプル

| プラグイン | 機能 |
|-----------|------|
| auto-ruff | Write/Edit後にRuffを自動実行 |
| force-draft-pr | PRを自動的にDraft化 |

### .github/workflows/

GitHub Actions設定

| ワークフロー | 機能 |
|-------------|------|
| claude.yml | @claudeメンション応答 |
| claude-code-review.yml | PR自動レビュー |
