---
description: サンプルコマンドA
allowed-tools: SlashCommand
---

# Context

- 1～50までの数字からランダムに2つ選び、その小さい方を<BEGIN>, 大きい方を<END>としてください。
- 現在のパスを取得してください。
  - !`pwd`
  - 取得したパスは<PATH>としてください。

# 実行手順

1. SlashCommandツールで、以下のスラッシュコマンドを実行してください。

```
/sample-B <BEGIN> <END> <PATH>
```

2. 実行した結果返ってきたひらがな2文字について、それぞれA,Bとし「^A.*B$」の正規表現で表せる単語を1つ出力してください。