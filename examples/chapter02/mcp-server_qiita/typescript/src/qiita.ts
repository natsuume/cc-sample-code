const QIITA_API_URL = 'https://qiita.com/api/v2/items';

export interface QiitaArticle {
  id: string;
  title: string;
  url: string;
  body: string;
  created_at: string;
  updated_at: string;
  likes_count: number;
  stocks_count: number;
  user: {
    id: string;
    name: string;
    profile_image_url: string;
  };
  tags: {
    name: string;
    versions: string[];
  }[];
}

interface QiitaApiResponse {
  id: string;
  title: string;
  url: string;
  body: string;
  created_at: string;
  updated_at: string;
  likes_count: number;
  stocks_count: number;
  user: {
    id: string;
    name: string;
    profile_image_url: string;
  };
  tags: {
    name: string;
    versions: string[];
  }[];
}

const buildSearchQuery = (keywords: string[]): string => {
  const keywordQueries = keywords.map((keyword) => {
    const escaped = keyword.trim();

    return `title:${escaped} OR body:${escaped}`;
  });

  return keywordQueries.join(' ');
};

export const searchQiita = async (
  keywords: string[],
  perPage: number,
  page: number
): Promise<QiitaArticle[]> => {
  const query = buildSearchQuery(keywords);

  const params = new URLSearchParams({
    query,
    per_page: perPage.toString(),
    page: page.toString()
  });

  const url = `${QIITA_API_URL}?${params.toString()}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Qiita API request failed: ${response.statusText}`);
  }

  const articles = await response.json() as QiitaApiResponse[];

  return articles.map((article) => ({
    id: article.id,
    title: article.title,
    url: article.url,
    body: article.body,
    created_at: article.created_at,
    updated_at: article.updated_at,
    likes_count: article.likes_count,
    stocks_count: article.stocks_count,
    user: article.user,
    tags: article.tags
  }));
};
