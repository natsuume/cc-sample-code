---
description: "ルートブランチの最新変更をrebaseで反映"
argument-hint: "[--abort-on-conflict]"
allowed-tools: Bash(git status:*), Bash(git stash:*), Bash(git switch:*), Bash(git pull:*), Bash(git rebase:*), Bash(git symbolic-ref:*), Bash(git branch:*), Bash(git diff:*), Bash(sed:*)
---

ワーキングブランチにルートブランチの最新変更をrebaseで反映してください。

以下の手順で実行してください：

1. 現在のブランチ名を取得してください。
  - !`git branch --show-current`
2. ルートブランチ名を取得してください（origin/HEADから判定）。
  - !`git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`
3. 未コミットの変更があるか確認してください。
  - !`git status --porcelain`
4. 変更がある場合は stash で退避してください。
  - git stash
5. ルートブランチに切り替えてください。
  - git switch <ルートブランチ名>
6. リモートから最新の変更を取得してください。
  - git pull origin <ルートブランチ名>
7. 元のワーキングブランチに戻ってください。
  - git switch <元のブランチ名>
8. ルートブランチから rebase を実行してください。
  - git rebase <ルートブランチ名>
9. stash していた場合は復元してください。
  - git stash pop

## オプション引数

`$1` が `--abort-on-conflict` の場合：
コンフリクト発生時は自動で git rebase --abort を実行し、元の状態に戻してください。

## 注意事項

- rebase中にコンフリクトが発生した場合は、その旨をユーザーに報告してください
- stash pop でコンフリクトが発生した場合も同様に報告してください
- ルートブランチがローカルに存在しない場合は、まず fetch してから処理を続行してください
