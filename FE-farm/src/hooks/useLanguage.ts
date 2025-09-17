import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface Language {
  code: string;
  name: string;
}

export const useLanguage = () => {
  const { i18n, t } = useTranslation();
  const [availableLanguages, setAvailableLanguages] = useState<Language[]>([
    { code: 'vi', name: 'Tiếng Việt' },
    { code: 'en', name: 'English' }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const currentLanguage = i18n.language;

  const changeLanguage = async (languageCode: string) => {
    setIsLoading(true);
    try {
      // Change language in i18next
      await i18n.changeLanguage(languageCode);
      
      // Notify backend about language change
      await fetch(`${API_BASE_URL}/api/v1/set-language/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ language: languageCode }),
      });

      // Store in localStorage
      localStorage.setItem('i18nextLng', languageCode);
      
    } catch (error) {
      console.error('Error changing language:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchLanguageInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/language-info/`, {
        credentials: 'include',
      });
      
      if (response.ok) {
        const data = await response.json();
        setAvailableLanguages(data.available_languages);
      }
    } catch (error) {
      console.error('Error fetching language info:', error);
    }
  };

  useEffect(() => {
    fetchLanguageInfo();
  }, []);

  return {
    currentLanguage,
    availableLanguages,
    changeLanguage,
    isLoading,
    t,
  };
};
