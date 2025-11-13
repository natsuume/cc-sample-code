import { searchQiita, QiitaArticle } from './qiita.js';

const sleep = (ms: number): Promise<void> =>
  new Promise((resolve) => setTimeout(resolve, ms));

const validateArticle = (article: QiitaArticle): boolean => {
  const requiredFields = [
    'id',
    'title',
    'url',
    'body',
    'created_at',
    'updated_at',
    'likes_count',
    'stocks_count',
    'user',
    'tags'
  ];

  for (const field of requiredFields) {
    if (!(field in article)) {
      console.error(`❌ 必須フィールド "${field}" が存在しません`);

      return false;
    }
  }

  if (typeof article.id !== 'string') {
    console.error('❌ id が文字列ではありません');

    return false;
  }

  if (typeof article.title !== 'string') {
    console.error('❌ title が文字列ではありません');

    return false;
  }

  if (typeof article.likes_count !== 'number') {
    console.error('❌ likes_count が数値ではありません');

    return false;
  }

  if (!article.user || typeof article.user.id !== 'string') {
    console.error('❌ user.id が不正です');

    return false;
  }

  if (!Array.isArray(article.tags)) {
    console.error('❌ tags が配列ではありません');

    return false;
  }

  return true;
};

const runIntegrationTest = async (): Promise<void> => {
  console.log('=== Qiita API 結合テスト開始 ===\n');

  let successCount = 0;
  let failureCount = 0;

  // テストケース1: 単一キーワード検索
  console.log('テストケース1: 単一キーワード検索');
  console.log('キーワード: ["TypeScript"]');

  try {
    const articles1 = await searchQiita(['TypeScript'], 5, 1);

    console.log(`✅ APIリクエスト成功: ${articles1.length}件の記事を取得`);

    if (!Array.isArray(articles1)) {
      console.error('❌ レスポンスが配列ではありません');
      failureCount++;
    } else if (articles1.length === 0) {
      console.log('⚠️  検索結果が0件でした');
    } else {
      console.log('\n記事情報:');

      for (const article of articles1.slice(0, 2)) {
        console.log(`  - タイトル: ${article.title}`);
        console.log(`    URL: ${article.url}`);
        console.log(`    いいね: ${article.likes_count}, ストック: ${article.stocks_count}`);
        console.log(`    タグ: ${article.tags.map((t) => t.name).join(', ')}`);
        console.log('');

        if (!validateArticle(article)) {
          failureCount++;

          break;
        }
      }

      successCount++;
    }
  } catch (error) {
    console.error('❌ エラーが発生しました:', error);
    failureCount++;
  }

  console.log('\n--- 3秒待機中... ---\n');
  await sleep(3000);

  // テストケース2: 複数キーワード検索
  console.log('テストケース2: 複数キーワード検索');
  console.log('キーワード: ["MCP", "API"]');

  try {
    const articles2 = await searchQiita(['MCP', 'API'], 3, 1);

    console.log(`✅ APIリクエスト成功: ${articles2.length}件の記事を取得`);

    if (!Array.isArray(articles2)) {
      console.error('❌ レスポンスが配列ではありません');
      failureCount++;
    } else if (articles2.length === 0) {
      console.log('⚠️  検索結果が0件でした');
    } else {
      console.log('\n記事情報:');

      for (const article of articles2.slice(0, 2)) {
        console.log(`  - タイトル: ${article.title}`);
        console.log(`    投稿者: ${article.user.name}`);
        console.log('');

        if (!validateArticle(article)) {
          failureCount++;

          break;
        }
      }

      successCount++;
    }
  } catch (error) {
    console.error('❌ エラーが発生しました:', error);
    failureCount++;
  }

  // 結果サマリー
  console.log('\n=== テスト結果 ===');
  console.log(`成功: ${successCount} / 2`);
  console.log(`失敗: ${failureCount} / 2`);

  if (failureCount === 0) {
    console.log('\n✅ 全てのテストが成功しました！');
  } else {
    console.log('\n❌ 一部のテストが失敗しました');
    process.exit(1);
  }
};

runIntegrationTest().catch((error) => {
  console.error('テスト実行中にエラーが発生しました:', error);
  process.exit(1);
});
