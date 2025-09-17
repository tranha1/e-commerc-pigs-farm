import { useState, useEffect } from 'react';
import { apiService, NewsArticle, NewsCategory } from '@/services/api';

export const useNews = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [categories, setCategories] = useState<{ [key: number]: string }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch articles and categories in parallel
        const [articlesResponse, categoriesResponse] = await Promise.all([
          apiService.getNewsArticles({ 
            published: true, 
            page_size: 10,
            page: 1
          }),
          apiService.getNewsCategories()
        ]);

        if (articlesResponse.status === 'success') {
          setArticles(articlesResponse.data);
        }

        if (categoriesResponse.status === 'success') {
          // Convert categories array to lookup object
          const categoryLookup: { [key: number]: string } = {};
          categoriesResponse.data.forEach((cat: NewsCategory) => {
            categoryLookup[cat.id] = cat.name;
          });
          setCategories(categoryLookup);
        }

      } catch (err) {
        console.error('Error fetching news data:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { articles, categories, loading, error };
};